"""
simulate.py 
(adm1_dae_ss)
python -m adm1dae.simulate --influ src/adm1dae/AD_constinfluent_bsm2.npz --t_end 10 --dt 0.1 --out src/adm1dae/adm1_dae_test.npz

ADM1_DAE2_bsm2 with pHsolv_bsm2 and Sh2solv_adm1 (ADM1 DAE2, BSM2).

Mapping:
- pHsolv_bsm2 and Sh2solv_adm1 have direct feedthrough = 0; their outputs are their discrete states.
- Their Newton updates occur at each "major step" boundary.
- During a major step interval, discrete states are held constant.
- adm1_DAE2_bsm2 continuous states are integrated over each interval with a stiff solver.

Input data:
- AD_constinfluent_bsm2.npz containing either:
    (n, 94)  = time + 93 influent columns, OR
    (n, 93)  = 93 influent columns aligned to the simulation time grid

Outputs (saved as NPZ):
- times:      (N,)
- digesterin: (N, 101)  adm1 input vector u
- digesterout:(N, 150)  adm1 output vector y
- x_adm1:     (N, 105)  adm1 continuous states
- x_ph:       (N, 7)    pH solver discrete states
- x_sh2:      (N, 1)    Sh2 solver discrete state
- PAR, V:     parameter and dimension vectors (from init_adm1_bsm2.py)

"""

import sys
from pathlib import Path
import argparse
import numpy as np

# --- sizes (match S-functions) ---
NU_ADM1 = 101
NY_ADM1 = 150
NX_ADM1 = 105
NX_PH = 7
NX_SH2 = 1
NU_INFL = 93  # mux: 93 (influent) + 1 (Sh2) + 7 (pH) = 101

def _ensure_import_paths():
    """
    Ensure:
    - project root is on sys.path so compiled .pyd modules can be imported
    - this script's folder is on sys.path so init_adm1_bsm2.py can be imported
    """
    here = Path(__file__).resolve()
    py_dir = here.parent
    root = here.parents[1]

    if str(py_dir) not in sys.path:
        sys.path.insert(0, str(py_dir))
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

_ensure_import_paths()

# compiled extension modules (built at project root)
from . import adm1_DAE2_bsm2
from . import pHsolv_bsm2
from . import Sh2solv_adm1
from .init_adm1_bsm2 import get_init, get_constants_from_par


def _load_influent_array(npz_path: Path) -> np.ndarray:
    """
    Loads a 2D influent array from an NPZ.
    Prefers key 'AD_constinfluent_bsm2' if present; otherwise chooses the first 2D array.
    """
    with np.load(npz_path, allow_pickle=False) as npz:
        if "AD_constinfluent_bsm2" in npz.files:
            arr = np.asarray(npz["AD_constinfluent_bsm2"])
            if arr.ndim == 2:
                return arr
        # find any 2D array
        for k in npz.files:
            a = np.asarray(npz[k])
            if a.ndim == 2:
                return a
    raise ValueError(f"{npz_path.name}: no 2D array found in NPZ.")


class Influent93:
    """Linear interpolator for the 93-element influent vector (From Workspace)."""

    def __init__(self, path_npz: Path, t_end: float):
        arr = np.asarray(_load_influent_array(path_npz), dtype=float)

        if arr.shape[1] == 1 + NU_INFL:
            self.t_src = arr[:, 0].copy()
            self.u_src = arr[:, 1:].copy()
        elif arr.shape[1] == NU_INFL:
            # aligned data (no time); synthesize time over [0, t_end]
            n = arr.shape[0]
            self.t_src = np.linspace(0.0, float(t_end), n, dtype=float)
            self.u_src = arr.copy()
        else:
            raise ValueError(
                f"{path_npz.name}: expected (n,94)=time+93 or (n,93)=aligned, got {arr.shape}"
            )

        if np.any(np.diff(self.t_src) < 0):
            raise ValueError(f"{path_npz.name}: time column must be non-decreasing")

    def eval(self, t: float) -> np.ndarray:
        """
        Returns u_infl(t) as (93,) float64 using exact linear interpolation.
        Boundary behavior: clamp to first/last sample.
        """
        t = float(t)
        if t <= self.t_src[0]:
            return self.u_src[0].astype(np.float64, copy=True)
        if t >= self.t_src[-1]:
            return self.u_src[-1].astype(np.float64, copy=True)

        out = np.empty((NU_INFL,), dtype=np.float64)
        for j in range(NU_INFL):
            out[j] = np.interp(t, self.t_src, self.u_src[:, j])
        return out


def mux_u(infl93: np.ndarray, x_sh2: np.ndarray, x_ph: np.ndarray) -> np.ndarray:
    """Build u (101) = [infl93(93), Sh2(1), pHstate(7)]."""
    u = np.empty((NU_ADM1,), dtype=np.float64)
    u[:NU_INFL] = infl93
    u[93] = float(x_sh2[0])
    u[94:101] = x_ph[:7]
    return u


def _summary_at_final(digesterin: np.ndarray, digesterout: np.ndarray, PAR: np.ndarray):
    """
    Minimal analogue of plotting_results.m: prints final-state values and gas KPI.
    """
    m = digesterout.shape[0] - 1
    const = get_constants_from_par(PAR)
    R_cte = const["R_cte"]
    T_op = const["T_op"]
    P_atm = const["P_atm"]

    print("\nFinal influent conditions (at last logged time)")
    print("************************************************")
    print(f"Qin = {digesterin[m, 24]:.6g} m3/d")
    print(f"S_su={digesterin[m,0]:.6g}, S_aa={digesterin[m,1]:.6g}, S_fa={digesterin[m,2]:.6g}, "
          f"S_va={digesterin[m,3]:.6g}, S_bu={digesterin[m,4]:.6g}, S_pro={digesterin[m,5]:.6g}, S_ac={digesterin[m,6]:.6g}")

    print("\nFinal digester state (selected)")
    print("********************************")
    print(f"S_su={digesterout[m,0]:.6g}, S_aa={digesterout[m,1]:.6g}, S_fa={digesterout[m,2]:.6g}, "
          f"S_va={digesterout[m,3]:.6g}, S_bu={digesterout[m,4]:.6g}, S_pro={digesterout[m,5]:.6g}, S_ac={digesterout[m,6]:.6g}")
    print(f"S_h2={digesterout[m,7]:.6g}, S_ch4={digesterout[m,8]:.6g}, S_IC={digesterout[m,9]:.6g}, S_IN={digesterout[m,10]:.6g}")

    # indices used in your MATLAB plotting_results.m (1-based):
    # p_gas_h2 -> 41, p_gas_ch4 -> 42, p_gas_co2 -> 43, P_gas -> 52, q_gas_norm -> 53
    p_h2  = digesterout[m, 42-1]  # p_gas_h2
    p_ch4 = digesterout[m, 43-1]  # p_gas_ch4
    p_co2 = digesterout[m, 44-1]  # p_gas_co2
    P_gas = digesterout[m, 53-1]  # total headspace pressure
    Qgas_norm = digesterout[m, 54-1]  # q_gas normalized to P_atm
    if P_gas <= 0.0:
        print("\nWarning: P_gas <= 0 encountered in outputs; gas KPI cannot be computed reliably.")
        methane_kg_d = float('nan')
        hydrogen_kg_d = float('nan')
        co2_kg_d = float('nan')
    else:
        if P_gas <= 0.0:
            print("\nWarning: P_gas <= 0 encountered in outputs; gas KPI cannot be computed reliably.")
            methane_kg_d = float('nan')
            hydrogen_kg_d = float('nan')
            co2_kg_d = float('nan')
        else:
            methane_kg_m3 = p_ch4 / P_gas * P_atm * 16.0 / (R_cte * T_op)
            methane_kg_d = methane_kg_m3 * Qgas_norm
        
            hydrogen_kg_m3 = p_h2 / P_gas * P_atm * 2.0 / (R_cte * T_op)
            hydrogen_kg_d = hydrogen_kg_m3 * Qgas_norm
        
            co2_kg_m3 = p_co2 / P_gas * P_atm * 44.0 / (R_cte * T_op)
            co2_kg_d = co2_kg_m3 * Qgas_norm

    print("\nGas production (normalized to P_atm)")
    print("***********************************")
    print(f"Q_gas_norm = {Qgas_norm:.6g} m3/d")
    print(f"CH4 = {methane_kg_d:.6g} kg/d = {methane_kg_d * 50.014 / 3.6:.6g} kWh/d")
    print(f"H2  = {hydrogen_kg_d:.6g} kg/d")
    print(f"CO2 = {co2_kg_d:.6g} kg/d")

    # H+ and pH outputs are y[28]=pH, y[29]=SH+ in adm1_DAE2_bsm2 outputs (0-based 27 and 28)
    print("\nAcid-base outputs")
    print("*****************")
    print(f"pH   = {digesterout[m, 27]:.6g}")
    print(f"S_H+ = {digesterout[m, 28]:.6g} mol/L")


def simulate(
    influ_npz: Path,
    t_end: float = 300.0,
    dt: float = 0.1,
    rtol: float = 1e-6,
    atol: float = 1e-8,
    out_npz: Path | None = None,
    do_plot: bool = False,
) -> dict:
    """
    Piecewise integration over fixed major-step grid (dt) with discrete pH/Sh2 updates at each boundary.
    """
    try:
        from scipy.integrate import solve_ivp
    except Exception as e:
        raise RuntimeError("SciPy is required: pip install scipy") from e

    DIGESTERINIT, SH2SOLVINIT, PHSOLVINIT, PAR, V = get_init()

    infl = Influent93(influ_npz, t_end=float(t_end))

    times = np.arange(0.0, float(t_end) + 0.5 * float(dt), float(dt), dtype=np.float64)
    nT = times.size

    x_adm1 = DIGESTERINIT.copy()
    x_sh2 = SH2SOLVINIT.copy()
    x_ph = PHSOLVINIT.copy()

    digesterin = np.empty((nT, NU_ADM1), dtype=np.float64)
    digesterout = np.empty((nT, NY_ADM1), dtype=np.float64)
    x_adm1_log = np.empty((nT, NX_ADM1), dtype=np.float64)
    x_ph_log = np.empty((nT, NX_PH), dtype=np.float64)
    x_sh2_log = np.empty((nT, NX_SH2), dtype=np.float64)

    # --- Initial snapshot (t0) ---
    t0 = float(times[0])
    infl0 = infl.eval(t0)
    u0 = mux_u(infl0, x_sh2, x_ph)
    y0 = np.empty((NY_ADM1,), dtype=np.float64)
    adm1_DAE2_bsm2.outputs(y0, x_adm1, u0, PAR, V)

    # Discrete updates at t0 (Simulink major step)
    # pHsolv uses XINIT for its Newton initial guess in the original S-function:
    pHsolv_bsm2.update(x_ph, y0, PAR, PHSOLVINIT)
    Sh2solv_adm1.update(x_sh2, y0, PAR, V)

    # Consistent snapshot after discrete updates
    u0b = mux_u(infl0, x_sh2, x_ph)
    adm1_DAE2_bsm2.outputs(y0, x_adm1, u0b, PAR, V)

    digesterin[0, :] = u0b
    digesterout[0, :] = y0
    x_adm1_log[0, :] = x_adm1
    x_ph_log[0, :] = x_ph
    x_sh2_log[0, :] = x_sh2

    # --- Main loop over major steps ---
    for k in range(nT - 1):
        t0 = float(times[k])
        t1 = float(times[k + 1])

        # Hold discrete states constant over (t0, t1]
        x_ph_hold = x_ph.copy()
        x_sh2_hold = x_sh2.copy()

        def rhs(t, x):
            # SciPy may pass non-contiguous views during Jacobian estimation.
            # The Cython wrappers require C-contiguous 1D arrays.
            x_c = np.ascontiguousarray(x, dtype=np.float64)
            infl_t = infl.eval(t)
            u = mux_u(infl_t, x_sh2_hold, x_ph_hold)
            u_c = np.ascontiguousarray(u, dtype=np.float64)
            dx = np.empty((NX_ADM1,), dtype=np.float64)
            adm1_DAE2_bsm2.derivatives(dx, x_c, u_c, PAR, V)
            return dx

        sol = solve_ivp(
            rhs,
            t_span=(t0, t1),
            y0=x_adm1,
            method="BDF",
            rtol=float(rtol),
            atol=float(atol),
            t_eval=(t1,),
        )
        if not sol.success:
            raise RuntimeError(f"Integration failed at step {k} [{t0},{t1}]: {sol.message}")

        x_adm1 = sol.y[:, -1].astype(np.float64, copy=True)

        # Outputs at t1 using held discrete states
        infl1 = infl.eval(t1)
        u1_hold = mux_u(infl1, x_sh2_hold, x_ph_hold)
        y1 = np.empty((NY_ADM1,), dtype=np.float64)
        adm1_DAE2_bsm2.outputs(y1, x_adm1, u1_hold, PAR, V)

        # Discrete updates at t1 using y1 bus
        pHsolv_bsm2.update(x_ph, y1, PAR, PHSOLVINIT)
        Sh2solv_adm1.update(x_sh2, y1, PAR, V)

        # Consistent snapshot at t1 after discrete updates
        u1 = mux_u(infl1, x_sh2, x_ph)
        adm1_DAE2_bsm2.outputs(y1, x_adm1, u1, PAR, V)

        digesterin[k + 1, :] = u1
        digesterout[k + 1, :] = y1
        x_adm1_log[k + 1, :] = x_adm1
        x_ph_log[k + 1, :] = x_ph
        x_sh2_log[k + 1, :] = x_sh2

    result = dict(
        times=times,
        digesterin=digesterin,
        digesterout=digesterout,
        x_adm1=x_adm1_log,
        x_ph=x_ph_log,
        x_sh2=x_sh2_log,
        PAR=PAR,
        V=V,
    )

    if out_npz is not None:
        out_npz = Path(out_npz)
        out_npz.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(out_npz, **result)

    _summary_at_final(digesterin, digesterout, PAR)

    if do_plot:
        _plot_basic(times, digesterout, PAR)

    return result


def _plot_basic(times: np.ndarray, digesterout: np.ndarray, PAR: np.ndarray):
    """
    Basic plots to match common ADM1 review:
    - pH
    - total VFA (S_va+S_bu+S_pro+S_ac)
    - normalized gas flow
    """
    import matplotlib.pyplot as plt

    pH = digesterout[:, 27]
    vfa = digesterout[:, 3] + digesterout[:, 4] + digesterout[:, 5] + digesterout[:, 6]
    qgas = digesterout[:, 54-1]

    plt.figure()
    plt.plot(times, pH)
    plt.xlabel("Time (d)")
    plt.ylabel("pH")
    plt.title("ADM1: pH")
    plt.grid(True)

    plt.figure()
    plt.plot(times, vfa)
    plt.xlabel("Time (d)")
    plt.ylabel("VFA (kg COD/m3)")
    plt.title("ADM1: Total VFA")
    plt.grid(True)

    plt.figure()
    plt.plot(times, qgas)
    plt.xlabel("Time (d)")
    plt.ylabel("Qgas (m3/d, normalized)")
    plt.title("ADM1: Gas flow (normalized)")
    plt.grid(True)

    plt.show()


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--influ", type=str, required=True, help="Path to AD_constinfluent_bsm2.npz")
    p.add_argument("--t_end", type=float, default=300.0, help="Simulation stop time (days)")
    p.add_argument("--dt", type=float, default=0.1, help="Major step size (days)")
    p.add_argument("--rtol", type=float, default=1e-6, help="BDF relative tolerance")
    p.add_argument("--atol", type=float, default=1e-8, help="BDF absolute tolerance")
    p.add_argument("--out", type=str, default="python/adm1_dae_ss_results.npz", help="Output NPZ path")
    p.add_argument("--plot", action="store_true", help="Show basic plots (matplotlib)")
    return p.parse_args()


def main():
    args = parse_args()
    simulate(
        influ_npz=Path(args.influ),
        t_end=args.t_end,
        dt=args.dt,
        rtol=args.rtol,
        atol=args.atol,
        out_npz=Path(args.out),
        do_plot=bool(args.plot),
    )
    print(f"\nSaved results to: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

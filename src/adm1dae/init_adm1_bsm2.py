"""
init_adm1_bsm2.py

Exact transcription of adm1_init.m (BSM2 ADM1-DAE2 initial conditions and parameters).
No alterations; values and ordering match the MATLAB script you provided.

All arrays are returned as float64 NumPy arrays.
"""

from __future__ import annotations
import numpy as np

def get_init():
    # --- Initial conditions (exact) ---
    S_su =  0.0124
    S_aa =  0.0055
    S_fa =  0.1074
    S_va =  0.0123
    S_bu =  0.0140
    S_pro = 0.0176
    S_ac =  0.0893
    S_h2 =  2.5055e-7
    S_ch4 = 0.0555
    S_IC = 0.0951
    S_IN = 0.0945
    S_I = 0.1309
    X_xc = 0.0
    X_ch = 0.0205
    X_pr = 0.0842
    X_li = 0.0436
    X_su = 0.3122
    X_aa = 0.9317
    X_fa = 0.3384
    X_c4 = 0.3258
    X_pro = 0.1011
    X_ac = 0.6772
    X_h2 =  0.2848
    X_I =  17.2162

    S_gas_h2 = 1.1032e-5
    S_gas_ch4 = 1.6535
    S_gas_co2 = 0.0135
    S_gas_D2 = 0.0
    S_gas_D3 = 0.0
    S_gas_D4 = 0.0
    S_gas_D5 = 0.0
    S_gas_D6 = 0.0
    S_gas_D7 = 0.0
    S_gas_D8 = 0.0
    S_gas_D9 = 0.0
    S_gas_D10 = 0.0

    S_P1_D = 0.0
    S_P2_D = 0.0
    S_P3_D = 0.0
    S_P4_D = 0.0
    S_P5_D = 0.0
    S_P6_D = 0.0
    S_P7_D = 0.0
    S_P8_D = 0.0
    S_P9_D = 0.0
    S_P10_D = 0.0

    S_S1_D = 0.0
    S_S2_D = 0.0
    S_S3_D = 0.0
    S_S4_D = 0.0
    S_S5_D = 0.0
    S_S6_D = 0.0
    S_S7_D = 0.0
    S_S8_D = 0.0
    S_S9_D = 0.0
    S_S10_D = 0.0

    ION_D1_D = 0.0
    ION_D2_D = 0.0
    ION_D3_D = 0.0052
    ION_D4_D = 0.0
    ION_D5_D = 0.0
    ION_D6_D = 0.0
    ION_D7_D = 0.0
    ION_D8_D = 0.0
    ION_D9_D = 0.0
    ION_D10_D = 0.0
    ION_D11_D = 0.0
    ION_D12_D = 0.0
    ION_D13_D = 0.0
    ION_D14_D = 0.0
    ION_D15_D = 0.0
    ION_D16_D = 0.0
    ION_D17_D = 0.0
    ION_D18_D = 0.0
    ION_D19_D = 0.0
    ION_D20_D = 0.0

    DIGESTERINIT = np.concatenate([
        np.array([

        S_su, S_aa, S_fa, S_va, S_bu, S_pro, S_ac, S_h2, S_ch4, S_IC, S_IN, S_I,
        X_xc, X_ch, X_pr, X_li, X_su, X_aa, X_fa, X_c4, X_pro, X_ac, X_h2, X_I,
        S_gas_h2, S_gas_ch4, S_gas_co2, S_gas_D2, S_gas_D3, S_gas_D4, S_gas_D5, S_gas_D6,
        S_gas_D7, S_gas_D8, S_gas_D9, S_gas_D10,
        S_P1_D, S_P2_D, S_P3_D, S_P4_D, S_P5_D, S_P6_D, S_P7_D, S_P8_D, S_P9_D, S_P10_D,
        S_S1_D, S_S2_D, S_S3_D, S_S4_D, S_S5_D, S_S6_D, S_S7_D, S_S8_D, S_S9_D, S_S10_D,
        ION_D1_D, ION_D2_D, ION_D3_D, ION_D4_D, ION_D5_D, ION_D6_D, ION_D7_D, ION_D8_D,
        ION_D9_D, ION_D10_D, ION_D11_D, ION_D12_D, ION_D13_D, ION_D14_D, ION_D15_D,
        ION_D16_D, ION_D17_D, ION_D18_D, ION_D19_D, ION_D20_D
    
        ], dtype=np.float64),
        # Multiple minerals (states 76..104 in the S-function): 29 dummy states (set to zero)
        np.zeros(29, dtype=np.float64)
    ])
    SH2SOLVINIT = np.array([S_h2], dtype=np.float64)

    # --- Parameters (exact) ---
    f_sI_xc = 0.1
    f_xI_xc = 0.2
    f_ch_xc = 0.2
    f_pr_xc = 0.2
    f_li_xc = 0.3
    N_xc = 0.0376/14.0
    N_I = 0.06/14.0
    N_aa = 0.007
    C_xc = 0.02786
    C_sI = 0.03
    C_ch = 0.0313
    C_pr = 0.03
    C_li = 0.022
    C_xI = 0.03
    C_su = 0.0313
    C_aa = 0.03
    f_fa_li = 0.95
    C_fa = 0.0217
    f_h2_su = 0.19
    f_bu_su = 0.13
    f_pro_su = 0.27
    f_ac_su = 0.41
    N_bac = 0.08/14.0
    C_bu = 0.025
    C_pro = 0.0268
    C_ac = 0.0313
    C_bac = 0.0313
    Y_su = 0.1
    f_h2_aa = 0.06
    f_va_aa = 0.23
    f_bu_aa = 0.26
    f_pro_aa = 0.05
    f_ac_aa = 0.40
    C_va = 0.024
    Y_aa = 0.08
    Y_fa = 0.06
    Y_c4 = 0.06
    Y_pro = 0.04
    C_ch4 = 0.0156
    Y_ac = 0.05
    Y_h2 = 0.06
    k_dis = 0.5
    k_hyd_ch = 0.3
    k_hyd_pr = 0.3
    k_hyd_li = 0.3
    K_S_IN = 1.0e-4
    k_m_su = 30.0
    K_S_su = 0.5
    pH_UL_aa = 5.5
    pH_LL_aa = 4.0
    k_m_aa = 50.0
    K_S_aa = 0.3
    k_m_fa = 6.0
    K_S_fa = 0.4
    K_Ih2_fa = 5.0e-6
    k_m_c4 = 20.0
    K_S_c4 = 0.2
    K_Ih2_c4 = 1.0e-5
    k_m_pro = 13.0
    K_S_pro = 0.1
    K_Ih2_pro = 3.5e-6
    k_m_ac = 8.0
    K_S_ac = 0.15
    K_I_nh3 = 0.0018
    pH_UL_ac = 7.0
    pH_LL_ac = 6.0
    k_m_h2 = 35.0
    K_S_h2 = 7.0e-6
    pH_UL_h2 = 6.0
    pH_LL_h2 = 5.0
    k_dec_Xsu = 0.02
    k_dec_Xaa = 0.02
    k_dec_Xfa = 0.02
    k_dec_Xc4 = 0.02
    k_dec_Xpro = 0.02
    k_dec_Xac = 0.02
    k_dec_Xh2 = 0.02
    R_cte = 0.083145
    T_base = 298.15
    T_op = 308.15
    pK_w_base = 14.0
    pK_a_va_base = 4.86
    pK_a_bu_base = 4.82
    pK_a_pro_base = 4.88
    pK_a_ac_base = 4.76
    pK_a_co2_base = 6.35
    pK_a_IN_base = 9.25
    k_A_Bva = 1.0e10
    k_A_Bbu = 1.0e10
    k_A_Bpro = 1.0e10
    k_A_Bac = 1.0e10
    k_A_Bco2 = 1.0e10
    k_A_BIN = 1.0e10
    P_atm = 1.013
    kLa = 200.0
    K_H_h2o_base = 0.0313
    K_H_co2_base = 0.035
    K_H_ch4_base = 0.0014
    K_H_h2_base = 7.8e-4
    k_P = 5.0e4

    DIGESTERPAR = np.array([
        f_sI_xc, f_xI_xc, f_ch_xc, f_pr_xc, f_li_xc, N_xc, N_I, N_aa, C_xc, C_sI, C_ch, C_pr, C_li, C_xI, C_su, C_aa,
        f_fa_li, C_fa, f_h2_su, f_bu_su, f_pro_su, f_ac_su, N_bac, C_bu, C_pro, C_ac, C_bac, Y_su, f_h2_aa, f_va_aa,
        f_bu_aa, f_pro_aa, f_ac_aa, C_va, Y_aa, Y_fa, Y_c4, Y_pro, C_ch4, Y_ac, Y_h2, k_dis, k_hyd_ch, k_hyd_pr, k_hyd_li,
        K_S_IN, k_m_su, K_S_su, pH_UL_aa, pH_LL_aa, k_m_aa, K_S_aa, k_m_fa, K_S_fa, K_Ih2_fa, k_m_c4, K_S_c4, K_Ih2_c4,
        k_m_pro, K_S_pro, K_Ih2_pro, k_m_ac, K_S_ac, K_I_nh3, pH_UL_ac, pH_LL_ac, k_m_h2, K_S_h2, pH_UL_h2, pH_LL_h2,
        k_dec_Xsu, k_dec_Xaa, k_dec_Xfa, k_dec_Xc4, k_dec_Xpro, k_dec_Xac, k_dec_Xh2, R_cte, T_base, T_op, pK_w_base,
        pK_a_va_base, pK_a_bu_base, pK_a_pro_base, pK_a_ac_base, pK_a_co2_base, pK_a_IN_base,
        k_A_Bva, k_A_Bbu, k_A_Bpro, k_A_Bac, k_A_Bco2, k_A_BIN, P_atm, kLa, K_H_h2o_base, K_H_co2_base, K_H_ch4_base,
        K_H_h2_base, k_P
    ], dtype=np.float64)

    V_liq = 3400.0
    V_gas = 300.0
    DIM_D = np.array([V_liq, V_gas], dtype=np.float64)

    S_H_ion = 5.4562e-8
    S_hva = 0.0123
    S_hbu = 0.0140
    S_hpro = 0.0175
    S_hac = 0.0890
    S_hco3 = 0.0857
    S_nh3 = 0.0019
    PHSOLVINIT = np.array([S_H_ion, S_hva, S_hbu, S_hpro, S_hac, S_hco3, S_nh3], dtype=np.float64)

    return DIGESTERINIT, SH2SOLVINIT, PHSOLVINIT, DIGESTERPAR, DIM_D

def get_constants_from_par(par: np.ndarray):
    """
    Convenience: returns a small dict of constants used in the MATLAB plotting_results.m.
    Values are read from the parameter vector by fixed index (MATLAB ordering).
    """
    return {
        "C_su": float(par[14]),
        "C_aa": float(par[15]),
        "C_fa": float(par[17]),
        "C_va": float(par[33]),
        "C_bu": float(par[23]),
        "C_pro": float(par[24]),
        "C_ac": float(par[25]),
        "C_ch4": float(par[38]),
        "C_xI": float(par[13]),
        "C_bac": float(par[26]),
        "C_ch": float(par[10]),
        "C_pr": float(par[11]),
        "C_li": float(par[12]),
        "N_aa": float(par[7]),
        "N_bac": float(par[22]),
        "N_I": float(par[6]),
        "P_atm": float(par[93]),
        "R_cte": float(par[77]),
        "T_op": float(par[79]),
    }

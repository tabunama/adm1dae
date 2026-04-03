# adm1dae

Python package for ADM1 DAE process modeling with BSM2 algebraic pH and H2 solvers.

## Overview

`adm1dae` packages a compiled ADM1 implementation derived from the BSM2 ADM1 DAE workflow, together with:

- `adm1_DAE2_bsm2` : main ADM1 DAE reactor kernel
- `pHsolv_bsm2` : algebraic pH solver
- `Sh2solv_adm1` : algebraic dissolved hydrogen solver

The package also provides a Python simulation driver that reproduces the Simulink-style execution pattern with:

- continuous ADM1 state integration
- discrete pH solver updates
- discrete H2 solver updates
- influent interpolation
- result export to NPZ

## Installation

Install from PyPI:

```bash
pip install adm1dae
```

[project.urls]
Homepage = "https://github.com/tabunama/adm1dae"
Repository = "https://github.com/tabunama/adm1dae"
Documentation = "https://tabunama.github.io/adm1dae/"


### Current release

The current PyPI release is distributed as a compiled wheel for:

- Windows x64
- CPython 3.12

If your environment does not match that platform and Python version, `pip install adm1dae` may not find a compatible wheel.

## Import

```python
from adm1dae import simulate
```

## Command-line usage

```bash
python -m adm1dae.simulate --influ path/to/AD_constinfluent_bsm2.npz --t_end 300 --dt 0.1 --out adm1_dae_results.npz
```

## Input

The simulation expects an influent NPZ containing either:

- `(n, 94)` = time + 93 influent columns
- `(n, 93)` = 93 influent columns aligned to the simulation grid

## Output

The simulation saves NPZ output containing:

- `times`
- `digesterin`
- `digesterout`
- `x_adm1`
- `x_ph`
- `x_sh2`
- `PAR`
- `V`


## License and attribution

See:

- `LICENSE`
- `THIRD_PARTY_NOTICES.md`

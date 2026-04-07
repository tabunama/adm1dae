# adm1dae

Python package for ADM1 DAE process modeling with BSM2 algebraic pH and H2 solvers.

## Overview

`adm1dae` packages a compiled ADM1 implementation derived from the BSM2 ADM1 DAE workflow, together with:

- `adm1_DAE2_bsm2` : main ADM1 DAE reactor kernel
- `pHsolv_bsm2` : algebraic pH solver
- `Sh2solv_adm1` : algebraic dissolved hydrogen solver


## Installation

Install from PyPI:

```bash
pip install adm1dae
```

## Links

[PyPI](https://pypi.org/project/adm1dae/) 
[GitHub](https://github.com/tabunama/adm1dae) 
[Documentation](https://tabunama.github.io/adm1dae/)

### Current release

The current PyPI release is distributed as a compiled wheel for:

- Windows x64
- CPython 3.12


## Import

```python
from adm1dae import simulate
```


## License and attribution

See:

- `LICENSE`
- `THIRD_PARTY_NOTICES.md`

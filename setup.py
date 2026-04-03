from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

PKG = "src/adm1dae"

extensions = [
    Extension(
        name="adm1dae.adm1_DAE2_bsm2",
        sources=[
            f"{PKG}/cython/adm1_DAE2_bsm2.pyx",
            f"{PKG}/c_core/adm1_DAE2_bsm2.c",
        ],
        include_dirs=[
            f"{PKG}/c_core",
            f"{PKG}",
            np.get_include(),
        ],
        language="c",
    ),
    Extension(
        name="adm1dae.pHsolv_bsm2",
        sources=[
            f"{PKG}/cython/pHsolv_bsm2.pyx",
            f"{PKG}/c_core/pHsolv_bsm2.c",
        ],
        include_dirs=[
            f"{PKG}/c_core",
            f"{PKG}",
            np.get_include(),
        ],
        language="c",
    ),
    Extension(
        name="adm1dae.Sh2solv_adm1",
        sources=[
            f"{PKG}/cython/Sh2solv_adm1.pyx",
            f"{PKG}/c_core/Sh2solv_adm1.c",
        ],
        include_dirs=[
            f"{PKG}/c_core",
            f"{PKG}",
            np.get_include(),
        ],
        language="c",
    ),
]

setup(
    ext_modules=cythonize(
        extensions,
        compiler_directives={"language_level": "3"},
    ),
    zip_safe=False,
)
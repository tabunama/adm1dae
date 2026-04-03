import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

project = "adm1dae"
author = "Taher Abunama"
copyright = "2026"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

autodoc_mock_imports = [
    "adm1dae.adm1_DAE2_bsm2",
    "adm1dae.pHsolv_bsm2",
    "adm1dae.Sh2solv_adm1",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
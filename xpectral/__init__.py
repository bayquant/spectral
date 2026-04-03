# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

# Standard library imports
from pathlib import Path

# Other imports
from dotenv import load_dotenv
from . import charts
from . import data
from . import quant
from .charts.accessors import PandasBokehAccessor
from .charts.accessors import PolarsBokehAccessor
from ._typing import PandasDataFrame
from ._typing import PolarsDataFrame

# -----------------------------------------------------------------------------
# Globals and constants
# -----------------------------------------------------------------------------

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

# -----------------------------------------------------------------------------
# General API
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Private API
# -----------------------------------------------------------------------------

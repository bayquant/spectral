#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
from pathlib import Path
from typing import Protocol

# Other imports
from dotenv import load_dotenv
from . import charts
from . import data
from . import quant
from .charts.accessors import PandasBokehAccessor
from .charts.accessors import PolarsBokehAccessor

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

load_dotenv(
    dotenv_path=Path(__file__).resolve().parent / ".env"
)

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

class PolarsDataFrame(Protocol):
    @property
    def bokeh(self) -> PolarsBokehAccessor:
        """Bokeh accessor for Polars DataFrames.

        Call the accessor to create a figure, then chain glyph methods to build the plot.

        >>> fig = df.bokeh(...).line(...)
        """
        ...

class PandasDataFrame(Protocol):
    @property
    def bokeh(self) -> PandasBokehAccessor:
        """Bokeh accessor for Pandas DataFrames.

        Call the accessor to create a figure, then chain glyph methods to build the plot.

        >>> fig = df.bokeh(...).line(...)
        """
        ...

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

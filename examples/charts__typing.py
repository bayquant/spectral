#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports

# Other imports
from bokeh.io import show
from bokeh.plotting import figure
import pandas as pd
import polars as pl
from xpectral import PandasDataFrame
from xpectral import PolarsDataFrame

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

figure()

pl_df: PolarsDataFrame = pl.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})  # type: ignore[assignment]
fig = pl_df.bokeh(title="Polars Example", width=600, height=400)
fig.line(x="x", y="y", line_width=2)

pd_df: PandasDataFrame = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})  # type: ignore[assignment]
fig = pd_df.bokeh(title="Pandas Example", width=600, height=400)
fig.line(x="x", y="y", line_width=2)

show(fig)

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

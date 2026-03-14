#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
from __future__ import annotations

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
import warnings
from typing import Any

# Other imports
from bokeh.io import show
from bokeh.models import ColumnDataSource
from bokeh.models import glyphs
from bokeh.models.renderers import GlyphRenderer
import polars as pl
from bokeh.util.warnings import BokehUserWarning

from ._decorators import glyph_method
from ._figure import Figure
from spectral.charts.theme_manager import theme

warnings.simplefilter("ignore", BokehUserWarning)


@pl.api.register_dataframe_namespace("bokeh")
class BokehAccessor(Figure):

    __view_model__ = "Figure"
    __view_module__ = "bokeh.plotting.figure"

    def __init__(self, df: pl.DataFrame) -> None:
        self._df = df

    @property
    def source(self) -> ColumnDataSource:
        if not hasattr(self, "_source"):
            self._source = ColumnDataSource(self._df.to_dict(as_series=False))
        return self._source

    def __call__(self, *args, **kwargs) -> "BokehAccessor":
        super().__init__(*args, **kwargs)
        return self.plot

    @glyph_method(glyphs.Line)
    def line(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass


if __name__ == "__main__":
    theme.set("dark_minimal")
    df = pl.DataFrame({"x": [1, 2, 3], "y": [1, 4, 9]})
    fig = df.bokeh(title="My plot", width=700, height=300, tools="pan,wheel_zoom,reset")
    fig.line(x="x", y="y", line_width=2)
    show(fig)


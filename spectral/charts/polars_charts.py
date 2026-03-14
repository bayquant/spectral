from __future__ import annotations

import warnings
import polars as pl

from bokeh.models import ColumnDataSource, glyphs
from ._decorators import glyph_method
from bokeh.io import show
from bokeh.models.renderers import GlyphRenderer
from typing import Any
from spectral.charts.theme_manager import theme

from typing import Any
import polars as pl
from bokeh.io import show
from bokeh.plotting._figure import FigureOptions
from bokeh.plotting._plot import get_range, get_scale, process_axis_and_grid
from bokeh.plotting._tools import process_active_tools, process_tools_arg
from bokeh.models import Plot
from bokeh.models.renderers import GlyphRenderer
from typing import Any
from bokeh.models import glyphs
from bokeh.models import ColumnDataSource
from bokeh.util.warnings import BokehUserWarning

warnings.simplefilter("ignore", BokehUserWarning)


class Figure(Plot):

    def __init__(self, *arg, **kw) -> None:
        opts = FigureOptions(kw)

        names = self.properties()
        for name in kw.keys():
            if name not in names:
                self._raise_attribute_error_with_matches(name, names | opts.properties())

        super().__init__(*arg, **kw)

        self.x_range = get_range(opts.x_range)
        self.y_range = get_range(opts.y_range)

        self.x_scale = get_scale(self.x_range, opts.x_axis_type)
        self.y_scale = get_scale(self.y_range, opts.y_axis_type)

        process_axis_and_grid(self, opts.x_axis_type, opts.x_axis_location, opts.x_minor_ticks, opts.x_axis_label, self.x_range, 0)
        process_axis_and_grid(self, opts.y_axis_type, opts.y_axis_location, opts.y_minor_ticks, opts.y_axis_label, self.y_range, 1)

        tool_objs, tool_map = process_tools_arg(self, opts.tools, opts.tooltips)
        self.add_tools(*tool_objs)
        process_active_tools(
            self.toolbar,
            tool_map,
            opts.active_drag,
            opts.active_inspect,
            opts.active_scroll,
            opts.active_tap,
            opts.active_multi,
        )

    @property
    def plot(self):
        return self

    @property
    def coordinates(self):
        return None


@pl.api.register_dataframe_namespace("bokeh")
class BokehAccessor(Figure):

    __view_model__ = "Figure"
    __view_module__ = "bokeh.plotting.figure"

    def __init__(self, df: pl.DataFrame) -> None:
        self._df = df

    @property
    def source(self) -> ColumnDataSource:
        return ColumnDataSource(self._df.to_dict(as_series=False))

    def __call__(self, *args, **kwargs) -> "BokehAccessor":
        super().__init__(*args, **kwargs)
        return self.plot
    
    @glyph_method(glyphs.Line)
    def _line(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        raise NotImplementedError

    def line(self, x: str, y: str, **kwargs):
        return self._line(x, y, source=self.source, **kwargs)

    
if __name__ == "__main__":
    theme.set("dark_minimal")
    df = pl.DataFrame({"x": [1, 2, 3], "y": [1, 4, 9]})
    fig = df.bokeh(title="My plot", width=700, height=300, tools="pan,wheel_zoom,reset")
    fig.line(x="x", y="y", line_width=2)
    show(fig)

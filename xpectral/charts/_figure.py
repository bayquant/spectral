#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
from __future__ import annotations

# Other imports
from bokeh.models import Plot
from bokeh.plotting._figure import FigureOptions
from bokeh.plotting._plot import get_range
from bokeh.plotting._plot import get_scale
from bokeh.plotting._plot import process_axis_and_grid
from bokeh.plotting._tools import process_active_tools
from bokeh.plotting._tools import process_tools_arg

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

__all__ = ["Figure"]

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

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

        process_axis_and_grid(
            self,
            opts.x_axis_type,
            opts.x_axis_location,
            opts.x_minor_ticks,
            opts.x_axis_label,
            self.x_range,
            0,
        )
        process_axis_and_grid(
            self,
            opts.y_axis_type,
            opts.y_axis_location,
            opts.y_minor_ticks,
            opts.y_axis_label,
            self.y_range,
            1,
        )

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

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

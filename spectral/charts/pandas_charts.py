import pandas as pd
from itertools import cycle
from bokeh.plotting import figure
from bokeh.plotting import show
from bokeh.io import output_notebook
from bokeh.models import HoverTool 
from bokeh.models import NumeralTickFormatter
from bokeh.models import DatetimeTickFormatter
from bokeh.palettes import Category10

output_notebook(hide_banner=True)

@pd.api.extensions.register_dataframe_accessor('bokeh')
class BokehAccessor:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def plot(self, title=None, xaxis_label='', yaxis_label='', width=900, height=450):
        df = self._obj.copy()

        if 'timestamp' in df.columns:
            df = df.set_index('timestamp')
        if not isinstance(df.index, pd.DatetimeIndex):
            raise ValueError("DataFrame must have a DatetimeIndex or 'timestamp' column.")

        p = figure(
            active_drag='auto',
            title=title,
            x_axis_type='datetime',
            width=width,
            height=height,
            # toolbar_location=None
        )

        hover = HoverTool(
            tooltips=[
                ('Date', '@x{%F}'), 
                ('Return', '@y{0.00%}')
                ],
            formatters={'@x': 'datetime'},
            mode='vline'
        )
        p.add_tools(hover)

        color_cycle = cycle(Category10[10])
        for col, color in zip(df.columns, color_cycle):
            p.line(x=df.index, y=df[col], line_width=2, color=color, legend_label=str(col))

        p.xaxis.formatter = DatetimeTickFormatter(days='%b %d', months='%b %Y', years='%Y')
        p.yaxis.formatter = NumeralTickFormatter(format='0%')
        # p.legend.click_policy = 'hide'
        p.xaxis.axis_label = xaxis_label
        p.yaxis.axis_label = yaxis_label

        return show(p)

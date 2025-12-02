import polars as pl
import json
from itertools import cycle

from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.models import HoverTool, NumeralTickFormatter, DatetimeTickFormatter, ColumnDataSource, Legend
from bokeh.palettes import Category10

output_notebook(hide_banner=True)


@pl.api.register_dataframe_namespace("bokeh")
class BokehAccessor:
    def __init__(self, df: pl.DataFrame):
        self._df = df

    def plot(
        self,
        title: str | None = None,
        x_col: str = "timestamp",
        xaxis_label: str = "",
        yaxis_label: str = "",
        width: int = 700,
        height: int = 350,
        percent: bool = True,  # keep your 0.00% formatting behaviour
    ):
        df = self._df

        if x_col not in df.columns:
            raise ValueError(f"DataFrame must have a '{x_col}' column.")

        # All value columns except x
        value_cols = [c for c in df.columns if c != x_col]
        if not value_cols:
            raise ValueError("DataFrame must have at least one value column besides the time column.")

        # Ensure x_col is Datetime
        if not isinstance(df[x_col].dtype, pl.Datetime):
            raise ValueError(f"Column '{x_col}' must be a Datetime type, got {df[x_col].dtype!r}")

        # Sort by time just in case
        df = df.sort(x_col)

        # (Optional) strip timezone for Bokeh if you want to avoid any tz quirks
        if isinstance(df[x_col].dtype, pl.Datetime) and df[x_col].dtype.time_zone is not None:
            df = df.with_columns(pl.col(x_col).dt.replace_time_zone(None))

        # Convert to pandas for ColumnDataSource convenience
        pdf = df.select([x_col] + value_cols).to_pandas()
        source = ColumnDataSource(pdf)

        p = figure(
            active_drag="auto",
            title=title,
            x_axis_type="datetime",
            width=width,
            height=height,
        )

        hover = HoverTool(
            tooltips=[
                ("Date", f"@{{{x_col}}}" + "{%F}"),
                ("Series", "$name"),
                ("Value", "@$name{0.00%}" if percent else "@$name"),
            ],
            formatters={f"@{{{x_col}}}": "datetime"},
            mode="mouse",
        )
        p.add_tools(hover)

        color_cycle = cycle(Category10[10])
        legend_items = []
        for col, color in zip(value_cols, color_cycle):
            renderer = p.line(
                x=x_col,
                y=col,
                source=source,
                line_width=2,
                color=color,
                name=str(col),  # used by $name in tooltip
            )
            legend_items.append((str(col), [renderer]))

        legend = Legend(items=legend_items, click_policy="hide", background_fill_alpha=0.1, background_fill_color="#c2dce3")
        p.add_layout(legend, "right")

        p.xaxis.formatter = DatetimeTickFormatter(
            days="%b %d",
            months="%b %Y",
            years="%Y",
        )

        if percent:
            p.yaxis.formatter = NumeralTickFormatter(format="0%")

        p.xaxis.axis_label = xaxis_label
        p.yaxis.axis_label = yaxis_label

        p.toolbar.logo = None

        return show(p)

"""Polars DataFrame -> Bokeh chart helpers."""

from typing import ClassVar

import polars as pl
from bokeh.models import glyphs
from bokeh.models.glyphs import Line
from bokeh.plotting import figure

# TODO: add colors parameter with cycler
# TODO: handle name and legend_label the right way

class BasePolarsChart:
    """Base class for building Bokeh charts from a Polars DataFrame."""
    glyph_model: ClassVar[type[glyphs.Glyph] | None] = None

    def __init__(
        self,
        df: pl.DataFrame,
        *,
        x: str | None = None,
        y: list[str] | None = None,
        figure=None,
        figure_kwargs: dict | None = None,
        glyph_kwargs: dict | None = None,
    ):
        self._df = df
        self.x = x
        self.y = self._normalize_list(y)
        self._figure = figure
        self._figure_kwargs = figure_kwargs or {}
        self._glyph_kwargs = glyph_kwargs or {}
        
    @staticmethod
    def _normalize_list(values: str | list[str] | None) -> list[str]:
        """Normalize a str/list/None input into a list of strings."""
        if values is None:
            return []
        if isinstance(values, str):
            return [values]
        return list(values)

    def prepare_data(self) -> pl.DataFrame:
        """Validate inputs and ensure required columns exist."""
        if self.x is None:
            self.x = "__index"
        if self.x not in self._df.columns:
            if self.x == "__index":
                self._df = self._df.with_row_index(name=self.x)
            else:
                raise ValueError(f"Column '{self.x}' not found in DataFrame.")
        if not self.y:
            self.y = [col for col in self._df.columns if col != self.x]
        if not self.y:
            raise ValueError("No y columns to plot.")
        missing_y = [col for col in self.y if col not in self._df.columns]
        if missing_y:
            missing = ", ".join(missing_y)
            raise ValueError(f"y column(s) not found in DataFrame: {missing}")
        return self._df

    def build_figure(self) -> figure:
        """Create a new Bokeh figure from figure kwargs unless one is provided."""
        return self._figure or figure(**self._figure_kwargs)

    def add_glyphs(self, figure: figure) -> None:
        raise NotImplementedError

    def build(self):
        """Prepare data, build the figure, and add glyphs."""
        self.prepare_data()
        figure = self.build_figure()
        self.add_glyphs(figure)
        return figure


class LineGlyphChart(BasePolarsChart):
    """Line chart for one or more y columns."""
    glyph_model: ClassVar[type[glyphs.Line]] = Line

    def add_glyphs(self, figure: figure) -> None:
        for col in self.y:
            figure.line(
                x=self.x,
                y=col,
                source=self._df,
                **self._glyph_kwargs,
            )


@pl.api.register_dataframe_namespace("bokeh")
class BokehAccessor:
    def __init__(self, df: pl.DataFrame):
        self._df = df

    def line(
        self,
        x: str | None = None,
        y: str | list[str] | None = None,
        figure=None,
        figure_kwargs: dict | None = None,
        glyph_kwargs: dict | None = None,
    ):
        """Create a Bokeh line chart from the Polars DataFrame."""
        chart = LineGlyphChart(
            self._df,
            x=x,
            y=y,
            figure=figure,
            figure_kwargs=figure_kwargs,
            glyph_kwargs=glyph_kwargs,
        )
        return chart.build()

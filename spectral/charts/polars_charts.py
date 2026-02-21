import polars as pl
from bokeh.models.glyphs import Line
from bokeh.plotting import figure

# TODO: add colors parameter with cycler
# TODO: handle name and legend_label the right way

class BasePolarsChart:
    glyph_model = None

    def __init__(
        self,
        df: pl.DataFrame,
        *,
        x: str | None = None,
        y: list[str] | None = None,
        figure=None,
        **kwargs,
    ):
        self._df = df
        self.x = x
        self.y = self._normalize_y(y)
        self._figure = figure
        self._kwargs = kwargs
        
    @staticmethod
    def _normalize_y(y: str | list[str] | None) -> list[str]:
        if y is None:
            return []
        if isinstance(y, str):
            return [y]
        return list(y)

    def prepare_data(self) -> pl.DataFrame:
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
        return self._df

    def build_figure(self):
        figure_kwargs, _ = self._split_kwargs()
        return self._figure or figure(**figure_kwargs)

    def _split_kwargs(self):
        figure_props = set(figure().properties())
        glyph_props = set(self.glyph_model.properties()) if self.glyph_model else set()
        figure_kwargs = {k: v for k, v in self._kwargs.items() if k in figure_props}
        glyph_kwargs = {k: v for k, v in self._kwargs.items() if k in glyph_props}
        return figure_kwargs, glyph_kwargs

    def add_glyphs(self, figure):
        raise NotImplementedError

    def build(self):
        self.prepare_data()
        figure = self.build_figure()
        self.add_glyphs(figure)
        return figure


class LineGlyphChart(BasePolarsChart):
    glyph_model = Line

    def add_glyphs(self, figure):
        _, glyph_kwargs = self._split_kwargs()
        print(glyph_kwargs)
        for col in self.y:
            figure.line(
                x=self.x,
                y=col,
                source=self._df,
                **glyph_kwargs,
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
        **kwargs,
    ):
        chart = LineGlyphChart(
            self._df,
            x=x,
            y=y,
            figure=figure,
            **kwargs,
        )
        return chart.build()

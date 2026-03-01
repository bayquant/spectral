"""Polars DataFrame -> Bokeh chart helpers."""

from typing import Any

import polars as pl
from bokeh.plotting import figure


class BasePolarsChart:
    """Build Bokeh charts from a Polars DataFrame using a direct figure glyph."""

    glyph: str

    def __init__(
        self,
        df: pl.DataFrame,
        *,
        glyph: str,
        glyph_params: dict[str, Any] | None = None,
        figure=None,
        figure_params: dict[str, Any] | None = None,
    ):
        self._df = df
        self.glyph = glyph
        self._figure = figure
        self._glyph_params = glyph_params or {}
        self._figure_params = figure_params or {}
        self._validate_glyph(self.glyph)
        self._validate_params(
            name="figure_params",
            values=self._figure_params,
            accepted=self.accepted_figure_params(),
        )

    def build_figure(self) -> figure:
        """Return the target figure, applying figure params to existing figures too."""
        if self._figure is not None:
            if self._figure_params:
                self._figure.update(**self._figure_params)
            return self._figure
        return figure(**self._figure_params)

    def add_glyph(self, figure: figure) -> None:
        glyph_method = getattr(figure, self.glyph)
        glyph_method(
            source=self._df,
            **self._glyph_params,
        )

    def build(self):
        """Build the figure and add the glyph."""
        figure = self.build_figure()
        self.add_glyph(figure)
        return figure

    @staticmethod
    def _validate_glyph(glyph: str) -> None:
        pass
        if not hasattr(figure(), glyph):
            raise ValueError(f"Unknown glyph '{glyph}'")

    @staticmethod
    def _validate_params(name: str, values: dict[str, Any], accepted: set[str]) -> None:
        unknown = sorted(set(values) - accepted)
        if not unknown:
            return
        unknown_text = ", ".join(unknown)
        raise ValueError(
            f"Unsupported {name}: {unknown_text}. "
            f"Use `.accepted_{name}()` to inspect valid keys."
        )

    @staticmethod
    def accepted_figure_params() -> set[str]:
        """Get accepted params for bokeh.plotting.figure()."""
        return set(figure().properties())


@pl.api.register_dataframe_namespace(name="bokeh")
class BokehAccessor:
    def __init__(self, df: pl.DataFrame):
        self._df = df

    def glyph(
        self,
        glyph: str,
        *,
        glyph_params: dict[str, Any] | None = None,
        figure=None,
        figure_params: dict[str, Any] | None = None,
    ):
        """Create a Bokeh chart using a direct figure glyph method."""
        chart = BasePolarsChart(
            self._df,
            glyph=glyph,
            glyph_params=glyph_params,
            figure=figure,
            figure_params=figure_params,
        )
        return chart.build()

    def accepted_figure_params(self, pattern: str = "") -> set[str]:
        """Return accepted Bokeh figure property names for `figure_params`."""
        params = BasePolarsChart.accepted_figure_params()
        if pattern:
            return {arg for arg in params if pattern in arg}
        return params

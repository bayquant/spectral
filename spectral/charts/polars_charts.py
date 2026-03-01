"""Polars DataFrame -> Bokeh chart helpers."""

from typing import Any

import polars as pl
from bokeh.plotting import figure


class BasePolarsChart:
    """Build Bokeh charts from a Polars DataFrame using a direct glyph method."""

    method: str

    def __init__(
        self,
        df: pl.DataFrame,
        *,
        method: str,
        data: dict[str, str] | None = None,
        figure=None,
        figure_kwargs: dict[str, Any] | None = None,
        glyph_kwargs: dict[str, Any] | None = None,
    ):
        self._df = df
        self.method = method
        self.data = data or {}
        self._figure = figure
        self._figure_kwargs = figure_kwargs or {}
        self._glyph_kwargs = glyph_kwargs or {}
        self._validate_method(self.method)
        self._validate_kwargs(
            name="figure_kwargs",
            values=self._figure_kwargs,
            accepted=self.accepted_figure_kwargs(),
        )

    @staticmethod
    def _validate_method(method: str) -> None:
        if not hasattr(figure(), method):
            raise ValueError(f"Unknown method '{method}'")

    @staticmethod
    def _validate_kwargs(name: str, values: dict[str, Any], accepted: set[str]) -> None:
        unknown = sorted(set(values) - accepted)
        if not unknown:
            return
        unknown_text = ", ".join(unknown)
        raise ValueError(
            f"Unsupported {name}: {unknown_text}. "
            f"Use `.accepted_{name}()` to inspect valid keys."
        )

    @staticmethod
    def accepted_figure_kwargs() -> set[str]:
        """Get accepted kwargs for bokeh.plotting.figure()."""
        return set(figure().properties())

    def prepare_data(self) -> pl.DataFrame:
        """Validate inputs and ensure referenced columns exist."""
        if "x" not in self.data:
            self.data["x"] = "__index"

        for key, column in self.data.items():
            if not isinstance(column, str):
                raise ValueError(f"Data parameter '{key}' must be a single column name.")
            if column not in self._df.columns:
                if column == "__index":
                    self._df = self._df.with_row_index(name=column)
                else:
                    raise ValueError(f"Column '{column}' not found in DataFrame.")
        return self._df

    def build_figure(self) -> figure:
        """Return the target figure, applying figure kwargs to existing figures too."""
        if self._figure is not None:
            if self._figure_kwargs:
                self._figure.update(**self._figure_kwargs)
            return self._figure
        return figure(**self._figure_kwargs)

    def add_glyph(self, fig: figure) -> None:
        glyph_method = getattr(fig, self.method)
        glyph_method(
            source=self._df,
            **self.data,
            **self._glyph_kwargs,
        )

    def build(self):
        """Prepare data, build the figure, and add the glyph."""
        self.prepare_data()
        fig = self.build_figure()
        self.add_glyph(fig)
        return fig


@pl.api.register_dataframe_namespace(name="bokeh")
class BokehAccessor:
    def __init__(self, df: pl.DataFrame):
        self._df = df

    def glyph(
        self,
        method: str,
        *,
        data: dict[str, str] | None = None,
        figure=None,
        figure_kwargs: dict[str, Any] | None = None,
        glyph_kwargs: dict[str, Any] | None = None,
    ):
        """Create a Bokeh chart using a direct figure glyph method."""
        chart = BasePolarsChart(
            self._df,
            method=method,
            data=data,
            figure=figure,
            figure_kwargs=figure_kwargs,
            glyph_kwargs=glyph_kwargs,
        )
        return chart.build()

    def accepted_figure_kwargs(self, pattern: str = "") -> set[str]:
        """Return accepted Bokeh figure property names for `figure_kwargs`."""
        kwargs = BasePolarsChart.accepted_figure_kwargs()
        if pattern:
            return {arg for arg in kwargs if pattern in arg}
        return kwargs

    def accepted_glyph_kwargs(self, *, method: str, pattern: str = "") -> set[str]:
        """Return accepted Bokeh glyph property names for a given chart method."""
        BasePolarsChart._validate_method(method)
        kwargs: set[str] = set()
        if pattern:
            return {arg for arg in kwargs if pattern in arg}
        return kwargs

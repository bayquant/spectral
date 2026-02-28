"""Polars DataFrame -> Bokeh chart helpers."""

from dataclasses import dataclass
from typing import Any

import polars as pl
from bokeh.models import glyphs
from bokeh.models.glyphs import Line
from bokeh.models.glyphs import Scatter
from bokeh.models.glyphs import VArea
from bokeh.plotting import figure

# TODO: add colors parameter with cycler
# TODO: handle name and legend_label the right way


@dataclass(frozen=True)
class GlyphSpec:
    method: str
    model: type[glyphs.Glyph]
    required: tuple[str, ...]
    multi: frozenset[str] = frozenset()


GLYPH_REGISTRY: dict[str, GlyphSpec] = {
    "line": GlyphSpec(method="line", model=Line, required=("x", "y"), multi=frozenset({"y"})),
    "scatter": GlyphSpec(method="scatter", model=Scatter, required=("x", "y"), multi=frozenset({"y"})),
    "varea": GlyphSpec(method="varea", model=VArea, required=("x", "y1", "y2")),
}


class BasePolarsChart:
    """Build Bokeh charts from a Polars DataFrame using a glyph spec."""

    glyph_spec: GlyphSpec

    def __init__(
        self,
        df: pl.DataFrame,
        *,
        glyph_spec: GlyphSpec,
        data: dict[str, str | list[str]] | None = None,
        figure=None,
        figure_kwargs: dict[str, Any] | None = None,
        glyph_kwargs: dict[str, Any] | None = None,
    ):
        self._df = df
        self.glyph_spec = glyph_spec
        self.data = data or {}
        self._figure = figure
        self._figure_kwargs = figure_kwargs or {}
        self._glyph_kwargs = glyph_kwargs or {}
        self._validate_kwargs(
            name="figure_kwargs",
            values=self._figure_kwargs,
            accepted=self.accepted_figure_kwargs(),
        )
        self._validate_kwargs(
            name="glyph_kwargs",
            values=self._glyph_kwargs,
            accepted=self.accepted_glyph_kwargs(),
        )

    @staticmethod
    def _normalize_list(values: str | list[str] | None) -> list[str]:
        """Normalize a str/list/None input into a list of strings."""
        if values is None:
            return []
        if isinstance(values, str):
            return [values]
        return list(values)

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

    def accepted_glyph_kwargs(self) -> set[str]:
        """Get accepted kwargs for the active glyph model."""
        return set(self.glyph_spec.model.properties())

    def prepare_data(self) -> pl.DataFrame:
        """Validate inputs and ensure required columns exist."""
        if "x" in self.glyph_spec.required and not self.data.get("x"):
            self.data["x"] = "__index"
        missing = [key for key in self.glyph_spec.required if key not in self.data or self.data[key] is None]
        if missing:
            missing_text = ", ".join(missing)
            raise ValueError(f"Missing required data parameters: {missing_text}")
        for key in self.glyph_spec.required:
            value = self.data[key]
            values = self._normalize_list(value) if key in self.glyph_spec.multi else [value]
            for column in values:
                if not isinstance(column, str):
                    raise ValueError(f"Data parameter '{key}' must be a column name.")
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

    def add_glyphs(self, figure: figure) -> None:
        multi_key = next(iter(self.glyph_spec.multi), None)
        series = self._normalize_list(self.data[multi_key]) if multi_key else [None]

        for series_col in series:
            glyph_args = {
                key: (series_col if key == multi_key else self.data[key])
                for key in self.glyph_spec.required
            }
            getattr(figure, self.glyph_spec.method)(
                source=self._df,
                **glyph_args,
                **self._glyph_kwargs,
            )

    def build(self):
        """Prepare data, build the figure, and add glyphs."""
        self.prepare_data()
        fig = self.build_figure()
        self.add_glyphs(fig)
        return fig


class GlyphChart(BasePolarsChart):
    """Generic chart using a glyph spec."""

    glyph_spec: GlyphSpec


@pl.api.register_dataframe_namespace(name="bokeh")
class BokehAccessor:
    def __init__(self, df: pl.DataFrame):
        self._df = df
        self._glyph_registry = GLYPH_REGISTRY

    def glyph(
        self,
        method: str,
        *,
        data: dict[str, str | list[str]] | None = None,
        figure=None,
        figure_kwargs: dict[str, Any] | None = None,
        glyph_kwargs: dict[str, Any] | None = None,
    ):
        """Create a Bokeh chart using a registered glyph method."""
        glyph_spec = self._glyph_registry.get(method)
        if glyph_spec is None:
            available = ", ".join(sorted(self._glyph_registry))
            raise ValueError(f"Unknown method '{method}'. Available methods: {available}")
        chart = GlyphChart(
            self._df,
            glyph_spec=glyph_spec,
            data=data,
            figure=figure,
            figure_kwargs=figure_kwargs,
            glyph_kwargs=glyph_kwargs,
        )
        return chart.build()

    def accepted_figure_kwargs(self) -> set[str]:
        """Return accepted Bokeh figure property names for `figure_kwargs`."""
        return BasePolarsChart.accepted_figure_kwargs()

    def accepted_glyph_kwargs(self, *, method: str) -> set[str]:
        """Return accepted Bokeh glyph property names for a given chart method."""
        glyph_spec = self._glyph_registry.get(method)
        if glyph_spec is None:
            available = ", ".join(sorted(self._glyph_registry))
            raise ValueError(f"Unknown method '{method}'. Available methods: {available}")
        return set(glyph_spec.model.properties())

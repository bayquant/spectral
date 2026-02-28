from __future__ import annotations

from typing import Any
from typing import Protocol

from bokeh.plotting._figure import figure as Figure
from polars import *  # noqa: F403
from polars.dataframe.frame import DataFrame as _PolarsDataFrame


class BokehNamespace(Protocol):
    def glyph(
        self,
        method: str,
        *,
        data: dict[str, str | list[str]] | None = None,
        figure: Figure | None = None,
        figure_kwargs: dict[str, Any] | None = None,
        glyph_kwargs: dict[str, Any] | None = None,
    ) -> Figure: ...

    def accepted_figure_kwargs(self) -> set[str]: ...
    def accepted_glyph_kwargs(self, *, method: str) -> set[str]: ...


class DataFrame(_PolarsDataFrame):
    @property
    def bokeh(self) -> BokehNamespace: ...

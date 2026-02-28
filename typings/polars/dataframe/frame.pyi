from __future__ import annotations

from typing import Any

from spectral.charts.polars_charts import BokehAccessor


class DataFrame:
    bokeh: BokehAccessor

    def __getattr__(self, name: str) -> Any: ...

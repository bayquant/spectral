from . import charts as charts, data as data, quant as quant
from .charts.accessors import PandasBokehAccessor, PolarsBokehAccessor
from typing import Protocol

class PolarsDataFrame(Protocol):
    @property
    def bokeh(self) -> PolarsBokehAccessor: ...

class PandasDataFrame(Protocol):
    @property
    def bokeh(self) -> PandasBokehAccessor: ...

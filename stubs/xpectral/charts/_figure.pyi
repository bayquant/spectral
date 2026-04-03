from _typeshed import Incomplete
from bokeh.models import Plot

__all__ = ['Figure']

class Figure(Plot):
    x_range: Incomplete
    y_range: Incomplete
    x_scale: Incomplete
    y_scale: Incomplete
    def __init__(self, *arg, **kwargs) -> None: ...
    @property
    def plot(self): ...
    @property
    def coordinates(self) -> None: ...

from typing import Any
from typing import Protocol


class _BokehAccessor(Protocol):
    def glyph(
        self,
        method: str,
        *args: Any,
        data: dict[str, str | list[str]] | None = ...,
        figure: Any = ...,
        figure_kwargs: dict[str, Any] | None = ...,
        glyph_kwargs: dict[str, Any] | None = ...,
        **kwargs: Any,
    ) -> Any: ...

    def plot(self, *args: Any, **kwargs: Any) -> Any: ...
    def accepted_figure_kwargs(self) -> set[str]: ...
    def accepted_glyph_kwargs(self, *, method: str) -> set[str]: ...
    def __getattr__(self, name: str) -> Any: ...


class DataFrame:
    @property
    def bokeh(self) -> _BokehAccessor: ...

    def __getattr__(self, name: str) -> Any: ...

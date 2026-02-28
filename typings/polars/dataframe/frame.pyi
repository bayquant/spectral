from typing import Any


class BokehAccessor:
    def glyph(
        self,
        method: str,
        *,
        data: dict[str, str | list[str]] | None = None,
        figure: Any = None,
        figure_kwargs: dict[str, Any] | None = None,
        glyph_kwargs: dict[str, Any] | None = None,
    ) -> Any: ...
    def accepted_figure_kwargs(self) -> set[str]: ...
    def accepted_glyph_kwargs(self, *, method: str) -> set[str]: ...


class DataFrame:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    bokeh: BokehAccessor

    def __getattr__(self, name: str) -> Any: ...

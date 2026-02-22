"""Central theme management for Bokeh apps."""

from __future__ import annotations

from bokeh.io import curdoc
from bokeh.themes import Theme, built_in_themes


THEMES = {
    "caliber": built_in_themes["caliber"],
    "carbon": built_in_themes["carbon"],
    "light_minimal": built_in_themes["light_minimal"],
    "dark_minimal": built_in_themes["dark_minimal"],
    "night_sky": built_in_themes["night_sky"],
    "contrast": built_in_themes["contrast"],
    "light": Theme(
        json={
            "attrs": {
                "Figure": {
                    "background_fill_color": "#ffffff",
                    "border_fill_color": "#ffffff",
                    "outline_line_color": "#d0d7de",
                },
                "Grid": {
                    "grid_line_alpha": 0.2,
                    "grid_line_color": "#8c959f",
                },
                "Axis": {
                    "major_label_text_color": "#24292f",
                    "axis_label_text_color": "#24292f",
                    "major_tick_line_color": "#57606a",
                    "minor_tick_line_color": "#57606a",
                    "axis_line_color": "#57606a",
                },
                "Title": {
                    "text_font_size": "14pt",
                    "text_color": "#24292f",
                },
            }
        }
    ),
}


class ThemeAccessor:
    """Small accessor around a named collection of Bokeh themes."""

    def __init__(self, default: str = "light") -> None:
        if default not in THEMES:
            raise ValueError(f"Unknown default theme '{default}'")
        self._name = default

    @property
    def name(self) -> str:
        return self._name

    @property
    def current(self):
        return THEMES[self._name]

    def set(self, name: str) -> None:
        if name not in THEMES:
            raise ValueError(f"Unknown theme '{name}'. Options: {list(THEMES)}")
        self._name = name
        curdoc().theme = self.current


# Global accessor for app/notebook code.
theme = ThemeAccessor(default="light_minimal")

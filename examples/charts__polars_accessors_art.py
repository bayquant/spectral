#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
from __future__ import annotations
import math

# Other imports
from bokeh.colors import groups
from bokeh.io import output_file
from bokeh.io import show
import polars as pl
from xpectral.charts.theme_manager import theme

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

def build_data(points: int = 120) -> pl.DataFrame:
    x = list(range(points))
    base = [
        22
        + math.sin(i / 5.2) * 5.8
        + math.cos(i / 2.7) * 2.1
        + math.sin((i + 4) / 8.0) * 1.8
        for i in x
    ]

    surface = [value + 1.6 * math.sin(i / 3.2 + 0.8) for i, value in enumerate(base)]
    surface2 = [value + 1.1 * math.cos(i / 2.9 + 1.2) for i, value in enumerate(base)]
    trough = [value - 3.2 + 0.4 * math.cos(i / 2.0) for i, value in enumerate(base)]
    crest = [value + 2.3 + 0.4 * math.sin(i / 1.7) for i, value in enumerate(base)]

    return pl.DataFrame(
        {
            "x": x,
            "y": base,
            "surface": surface,
            "surface2": surface2,
            "depth_low": [value - 2.6 - math.sin(i / 2.4) * 0.8 for i, value in enumerate(base)],
            "depth_high": [value + 3.6 + math.cos(i / 2.2) * 1.1 for i, value in enumerate(base)],
            "wave_width": [0.72 + (i % 7) * 0.015 for i in x],
            "ripple": [2.0 + ((i + 4) % 7) * 0.03 for i in x],
            "left": [i - 0.38 for i in x],
            "right": [i + 0.38 for i in x],
            "crest": crest,
            "trough": trough,
            "r": [0.45 + 0.45 * (i % 6) / 5 for i in x],
            "outer_radius": [0.45 + 0.45 * (i % 6) / 5 + 0.3 for i in x],
            "start_angle": [i * 0.16 + (i % 4) * 0.1 for i in x],
            "end_angle": [i * 0.16 + (i % 4) * 0.1 + 1.15 + (i % 3) * 0.28 for i in x],
        }
    )


def build_art_plot() -> None:
    theme.set("ocean")
    output_file("charts_polars_accessors_ocean_waves.html", title="Accessor Ocean Waves")

    df = build_data()
    fig = df.bokeh(
        title="Ocean Waves",
        width=1000,
        height=560,
        tools="pan,wheel_zoom,box_zoom,reset",
    )

    # Deep water body.
    fig.varea(
        x="x",
        y1="depth_low",
        y2="depth_high",
        fill_color=groups.blue[8],
        fill_alpha=0.75,
        hatch_alpha=0.22,
        hatch_color=groups.blue[4],
        hatch_pattern="cross",
        hatch_scale=8,
    )

    # Surface wash layer.
    fig.varea(
        x="x",
        y1="surface2",
        y2="surface",
        fill_color=groups.blue[6],
        fill_alpha=0.35,
    )

    # Main wave crest path.
    fig.line(
        x="x",
        y="y",
        line_width=2.2,
        line_color=groups.blue[1],
        line_dash="dashdot",
    )

    # Crest and trough strokes.
    fig.line(
        x="x",
        y="crest",
        line_width=1.8,
        line_color=groups.blue[2],
        line_alpha=0.9,
        line_dash="dotted",
    )
    fig.line(
        x="x",
        y="trough",
        line_width=1.4,
        line_color=groups.blue[9],
        line_alpha=0.45,
        line_dash="dashed",
    )

    # Foam and spray dots.
    fig.scatter(
        x="x",
        y="surface",
        size="ripple",
        marker="cross",
        fill_color="white",
        line_color=groups.blue[1],
        line_width=1,
        fill_alpha=0.88,
    )

    # Vertical light shafts between trough and crest.
    fig.segment(
        x0="x",
        y0="trough",
        x1="x",
        y1="crest",
        line_width=1,
        line_color=groups.blue[4],
        line_alpha=0.4,
    )

    # Perspective ridges.
    fig.vbar(
        x="x",
        top="crest",
        bottom="surface",
        width="wave_width",
        fill_alpha=0.18,
        fill_color=groups.blue[0],
    )

    # Drift cells for subtle shimmer.
    fig.rect(
        x="x",
        y="y",
        width="wave_width",
        height="ripple",
        fill_alpha=0.07,
        fill_color=groups.blue[3],
        line_alpha=0,
        angle=0.42,
    )

    # Layered light slices.
    fig.quad(
        left="left",
        right="right",
        top="surface",
        bottom="surface2",
        fill_color=groups.blue[5],
        fill_alpha=0.12,
        line_color=groups.blue[7],
        line_width=1,
    )

    # Curved swell outlines.
    fig.arc(
        x="x",
        y="y",
        radius="r",
        start_angle="start_angle",
        end_angle="end_angle",
        line_width=1,
        line_color=groups.blue[2],
        line_alpha=0.35,
    )
    fig.wedge(
        x="x",
        y="surface2",
        radius="r",
        start_angle="start_angle",
        end_angle="end_angle",
        fill_alpha=0.18,
        fill_color=groups.blue[4],
    )
    fig.annular_wedge(
        x="x",
        y="y",
        inner_radius="r",
        outer_radius="outer_radius",
        start_angle="start_angle",
        end_angle="end_angle",
        fill_alpha=0.07,
        fill_color=groups.blue[1],
        line_alpha=0,
    )

    show(fig)

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

if __name__ == "__main__":
    build_art_plot()

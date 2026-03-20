#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
from __future__ import annotations
import warnings
from typing import Any

# Other imports
from bokeh.io import show
from bokeh.models import ColumnDataSource
from bokeh.models import glyphs
from bokeh.models.renderers import GlyphRenderer
from bokeh.util.warnings import BokehUserWarning
import polars as pl
from ._decorators import glyph_method
from ._figure import Figure
from spectral.charts.theme_manager import theme

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

warnings.simplefilter("ignore", BokehUserWarning)

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

@pl.api.register_dataframe_namespace("bokeh")
class BokehAccessor(Figure):

    __view_model__ = "Figure"
    __view_module__ = "bokeh.plotting.figure"

    def __init__(self, df: pl.DataFrame) -> None:
        self._df = df

    @property
    def source(self) -> ColumnDataSource:
        if not hasattr(self, "_source"):
            self._source = ColumnDataSource(self._df.to_dict(as_series=False))
        return self._source

    def __call__(self, *args, **kwargs) -> "BokehAccessor":
        super().__init__(*args, **kwargs)
        return self.plot

    # Glyph methods with both x and y parameters
    @glyph_method(glyphs.AnnularWedge)
    def annular_wedge(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.Annulus)
    def annulus(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.Arc)
    def arc(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.Block)
    def block(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.Ellipse)
    def ellipse(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.Image)
    def image(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.ImageRGBA)
    def image_rgba(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.ImageStack)
    def image_stack(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.ImageURL)
    def image_url(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.Line)
    def line(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.MathMLGlyph)
    def mathml_glyph(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.Ngon)
    def ngon(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.Patch)
    def patch(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.Ray)
    def ray(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.Rect)
    def rect(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.Scatter)
    def scatter(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.Step)
    def step(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.TeXGlyph)
    def tex_glyph(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.Text)
    def text(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.Wedge)
    def wedge(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    # Vertical glyph methods (have parameter x but not y)
    @glyph_method(glyphs.VArea)
    def varea(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.VAreaStep)
    def varea_step(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.VBar)
    def vbar(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.VSpan)
    def vspan(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    # Horizontal glyph methods (have parameter y but not x)
    @glyph_method(glyphs.HArea)
    def harea(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.HAreaStep)
    def harea_step(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.HBar)
    def hbar(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.HSpan)
    def hspan(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    # Glyph methods without x nor y parameters
    @glyph_method(glyphs.Bezier)
    def bezier(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.HStrip)
    def hstrip(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.HexTile)
    def hextile(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.MultiLine)
    def multi_line(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.MultiPolygons)
    def multipolygons(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.Patches)
    def patches(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.Quad)
    def quad(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.Quadratic)
    def quadratic(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.Segment)
    def segment(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

    @glyph_method(glyphs.VStrip)
    def vstrip(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        pass

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

if __name__ == "__main__":
    theme.set("dark_minimal")
    df = pl.DataFrame({"x": [1, 2, 3], "y": [1, 4, 9]})
    fig = df.bokeh(title="My plot", width=700, height=300, tools="pan,wheel_zoom,reset")
    fig.line(x="x", y="y", line_width=2)
    show(fig)

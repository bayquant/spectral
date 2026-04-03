#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
from __future__ import annotations
import warnings
from typing import Any
from typing import Sequence

# Other imports
from bokeh.models import ColumnDataSource
from bokeh.models import glyphs
from bokeh.models.renderers import GlyphRenderer
from bokeh.plotting._stack import double_stack
from bokeh.plotting._stack import single_stack
from bokeh.util.warnings import BokehUserWarning
import pandas as pd
import polars as pl
from ._decorators import glyph_method
from ._figure import Figure

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

warnings.simplefilter("ignore", BokehUserWarning)

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

class BokehAccessor(Figure):

    def __init__(self, df) -> None:
        self._df = df

    def __call__(self, *args, **kwargs) -> "BokehAccessor":
        super().__init__(*args, **kwargs)
        return self.plot

    #-------------------------------------------
    # Glyph methods with both x and y parameters
    @glyph_method(glyphs.AnnularWedge)
    def annular_wedge(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.Annulus)
    def annulus(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.Arc)
    def arc(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.Block)
    def block(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.Ellipse)
    def ellipse(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.Image)
    def image(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.ImageRGBA)
    def image_rgba(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.ImageStack)
    def image_stack(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.ImageURL)
    def image_url(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.Line)
    def line(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.MathMLGlyph)
    def mathml_glyph(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.Ngon)
    def ngon(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.Patch)
    def patch(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.Ray)
    def ray(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.Rect)
    def rect(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.Scatter)
    def scatter(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.Step)
    def step(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.TeXGlyph)
    def tex_glyph(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.Text)
    def text(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.Wedge)
    def wedge(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    #----------------------------------------------------
    # Vertical glyph methods (have parameter x but not y)
    @glyph_method(glyphs.VArea)
    def varea(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.VAreaStep)
    def varea_step(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.VBar)
    def vbar(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.VSpan)
    def vspan(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    #------------------------------------------------------
    # Horizontal glyph methods (have parameter y but not x)
    @glyph_method(glyphs.HArea)
    def harea(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.HAreaStep)
    def harea_step(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.HBar)
    def hbar(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.HSpan)
    def hspan(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    #-----------------------------------------
    # Glyph methods without x nor y parameters
    @glyph_method(glyphs.Bezier)
    def bezier(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.HStrip)
    def hstrip(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.HexTile)
    def hextile(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.MultiLine)
    def multi_line(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.MultiPolygons)
    def multipolygons(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.Patches)
    def patches(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.Quad)
    def quad(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.Quadratic)
    def quadratic(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.Segment)
    def segment(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    @glyph_method(glyphs.VStrip)
    def vstrip(self, *args: Any, **kwargs: Any) -> GlyphRenderer:
        ...

    #-----------------------------------------
    # Glyph stack methods 
    def harea_stack(self, stackers: Sequence[str], **kwargs: Any) -> list[GlyphRenderer]:
        result = []
        for kwarg in double_stack(stackers=stackers, spec0="x1", spec1="x2", **kwargs):
            result.append(self.harea(**kwarg))
        return result

    def hbar_stack(self, stackers: Sequence[str], **kwargs: Any) -> list[GlyphRenderer]:
        result = []
        for kwarg in double_stack(stackers=stackers, spec0="left", spec1="right", **kwargs):
            result.append(self.hbar(**kwarg))
        return result

    def hline_stack(self, stackers: Sequence[str], **kwargs: Any) -> list[GlyphRenderer]:
        result = []
        for kwarg in single_stack(stackers=stackers, spec="x", **kwargs):
            result.append(self.line(**kwarg))
        return result

    def varea_stack(self, stackers: Sequence[str], **kwargs: Any) -> list[GlyphRenderer]:
        result = []
        for kwarg in double_stack(stackers=stackers, spec0="y1", spec1="y2", **kwargs):
            result.append(self.varea(**kwarg))
        return result

    def vbar_stack(self, stackers: Sequence[str], **kwargs: Any) -> list[GlyphRenderer]:
        result = []
        for kwarg in double_stack(stackers=stackers, spec0="bottom", spec1="top", **kwargs):
            result.append(self.vbar(**kwarg))
        return result

    def vline_stack(self, stackers: Sequence[str], **kwargs: Any) -> list[GlyphRenderer]:
        result = []
        for kwarg in single_stack(stackers=stackers, spec="y", **kwargs):
            result.append(self.line(**kwarg))
        return result


@pl.api.register_dataframe_namespace("bokeh")
class PolarsBokehAccessor(BokehAccessor):

    __view_model__ = "Figure"
    __view_module__ = "bokeh.plotting.figure"

    @property
    def source(self) -> ColumnDataSource:
        if not hasattr(self, "_source"):
            self._source = ColumnDataSource(self._df.to_dict(as_series=False))
        return self._source
    
@pd.api.extensions.register_dataframe_accessor("bokeh")
class PandasBokehAccessor(BokehAccessor):

    __view_model__ = "Figure"
    __view_module__ = "bokeh.plotting.figure"

    @property
    def source(self) -> ColumnDataSource:
        if not hasattr(self, "_source"):
            self._source = ColumnDataSource(self._df.to_dict(orient="list"))
        return self._source


#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

# Polars' NameSpace descriptor caches the accessor on the DataFrame instance
# via setattr, causing the same BokehAccessor to be returned on repeated
# accesses of df.bokeh. Replacing the descriptor with a non-caching property
# ensures each access produces a fresh instance.
pl.DataFrame.bokeh = property(lambda self: PolarsBokehAccessor(self))  # type: ignore[assignment]

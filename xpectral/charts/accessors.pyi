#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
from typing import Any, Literal, Sequence, TypeAlias, Unpack

# Other imports
from bokeh._specs import (
    AngleArg,
    DistanceArg,
    FloatArg,
    Image2dArg,
    Image3dArg,
    MarkerArg,
    NullDistanceArg,
    Number1dArg,
    Number3dArg,
    NumberArg,
    SizeArg,
    StringArg,
)
from bokeh._types import (
    Datetime,
    TextLike,
    TimeDelta,
)
from bokeh._types import Color
from bokeh.core.enums import (
    AutoType as Auto,
    DirectionType as Direction,
    HorizontalLocationType as HorizontalLocation,
    LocationType as Location,
    SizingModeType as SizingMode,
    VerticalLocationType as VerticalLocation,
)
from bokeh.models import ColumnDataSource
from bokeh.models import glyphs
from bokeh.models.dom import Template
from bokeh.models.ranges import Range
from bokeh.models.renderers import GlyphRenderer
from bokeh.models.tools import (
    Drag,
    GestureTool,
    InspectTool,
    Scroll,
    Tap,
    Tool,
)
from bokeh.plotting.glyph_api import (
    AnnularWedgeArgs,
    AnnulusArgs,
    ArcArgs,
    BezierArgs,
    BlockArgs,
    EllipseArgs,
    HAreaArgs,
    HAreaStepArgs,
    HBarArgs,
    HSpanArgs,
    HStripArgs,
    HexTileArgs,
    ImageArgs,
    ImageRGBAArgs,
    ImageStackArgs,
    ImageURLArgs,
    LineArgs,
    MathMLArgs,
    MultiLineArgs,
    MultiPolygonsArgs,
    NgonArgs,
    PatchArgs,
    PatchesArgs,
    QuadArgs,
    QuadraticArgs,
    RayArgs,
    RectArgs,
    ScatterArgs,
    SegmentArgs,
    StepArgs,
    TeXArgs,
    TextArgs,
    VAreaArgs,
    VAreaStepArgs,
    VBarArgs,
    VSpanArgs,
    VStripArgs,
    WedgeArgs,
)
import pandas as pd
import polars as pl
from ._figure import Figure

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

RangeLike: TypeAlias = (
    Range
    | tuple[float, float]
    | tuple[Datetime, Datetime]
    | tuple[TimeDelta, TimeDelta]
    | Sequence[str]
)

AxisType: TypeAlias = Auto | Literal["linear", "log", "datetime", "timedelta", "mercator"] | None

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

class BokehAccessor(Figure):

    def __init__(self, df: pd.DataFrame | pl.DataFrame) -> None: ...

    def __call__(self,
        *,
        # Figure options
        x_range: RangeLike = ...,
        y_range: RangeLike = ...,
        x_axis_type: AxisType = ...,
        y_axis_type: AxisType = ...,
        tools: str | Sequence[str | Tool] = ...,
        x_minor_ticks: Auto | int = ...,
        y_minor_ticks: Auto | int = ...,
        x_axis_location: VerticalLocation | None = ...,
        y_axis_location: HorizontalLocation | None = ...,
        x_axis_label: TextLike | None = ...,
        y_axis_label: TextLike | None = ...,
        active_drag: Auto | str | Drag | None = ...,
        active_inspect: Auto | str | InspectTool | Sequence[InspectTool] | None = ...,
        active_scroll: Auto | str | Scroll | None = ...,
        active_tap: Auto | str | Tap | None = ...,
        active_multi: Auto | str | GestureTool | None = ...,
        tooltips: Template | str | list[tuple[str, str]] | None = ...,
        # Plot dimensions
        width: int = ...,
        height: int = ...,
        frame_width: int = ...,
        frame_height: int = ...,
        min_width: int = ...,
        max_width: int = ...,
        min_height: int = ...,
        max_height: int = ...,
        sizing_mode: SizingMode = ...,
        aspect_ratio: float | Auto = ...,
        match_aspect: bool = ...,
        # Plot title and toolbar
        title: str | None = ...,
        title_location: Location = ...,
        toolbar_location: Location | None = ...,
        toolbar_inner: bool = ...,
        toolbar_sticky: bool = ...,
        # Plot background and border
        background_fill_color: Color = ...,
        background_fill_alpha: float = ...,
        border_fill_color: Color = ...,
        border_fill_alpha: float = ...,
        outline_line_color: Color | None = ...,
        outline_line_alpha: float = ...,
        outline_line_width: float = ...,
        # Plot spacing
        min_border: int = ...,
        min_border_top: int = ...,
        min_border_bottom: int = ...,
        min_border_left: int = ...,
        min_border_right: int = ...,
        **kwargs: Any,
    ) -> BokehAccessor: ...

    # Glyph methods with both x and y parameters

    def annular_wedge(self,
        x: NumberArg = ...,
        y: NumberArg = ...,
        inner_radius: DistanceArg = ...,
        outer_radius: DistanceArg = ...,
        start_angle: AngleArg = ...,
        end_angle: AngleArg = ...,
        direction: Direction = ...,
        **kwargs: Unpack[AnnularWedgeArgs],
    ) -> GlyphRenderer[glyphs.AnnularWedge]: ...

    def annulus(self,
        x: NumberArg = ...,
        y: NumberArg = ...,
        inner_radius: DistanceArg = ...,
        outer_radius: DistanceArg = ...,
        **kwargs: Unpack[AnnulusArgs],
    ) -> GlyphRenderer[glyphs.Annulus]: ...

    def arc(self,
        x: NumberArg = ...,
        y: NumberArg = ...,
        radius: DistanceArg = ...,
        start_angle: AngleArg = ...,
        end_angle: AngleArg = ...,
        direction: Direction = ...,
        **kwargs: Unpack[ArcArgs],
    ) -> GlyphRenderer[glyphs.Arc]: ...

    def block(self,
        x: NumberArg = ...,
        y: NumberArg = ...,
        width: DistanceArg = ...,
        height: DistanceArg = ...,
        **kwargs: Unpack[BlockArgs],
    ) -> GlyphRenderer[glyphs.Block]: ...

    def ellipse(self,
        x: NumberArg = ...,
        y: NumberArg = ...,
        width: DistanceArg = ...,
        height: DistanceArg = ...,
        angle: AngleArg = ...,
        **kwargs: Unpack[EllipseArgs],
    ) -> GlyphRenderer[glyphs.Ellipse]: ...

    def image(self,
        image: Image2dArg = ...,
        x: NumberArg = ...,
        y: NumberArg = ...,
        dw: DistanceArg = ...,
        dh: DistanceArg = ...,
        dilate: bool = ...,
        **kwargs: Unpack[ImageArgs],
    ) -> GlyphRenderer[glyphs.Image]: ...

    def image_rgba(self,
        image: Image2dArg = ...,
        x: NumberArg = ...,
        y: NumberArg = ...,
        dw: DistanceArg = ...,
        dh: DistanceArg = ...,
        dilate: bool = ...,
        **kwargs: Unpack[ImageRGBAArgs],
    ) -> GlyphRenderer[glyphs.ImageRGBA]: ...

    def image_stack(self,
        image: Image3dArg = ...,
        x: NumberArg = ...,
        y: NumberArg = ...,
        dw: DistanceArg = ...,
        dh: DistanceArg = ...,
        dilate: bool = ...,
        **kwargs: Unpack[ImageStackArgs],
    ) -> GlyphRenderer[glyphs.ImageStack]: ...

    def image_url(self,
        url: StringArg = ...,
        x: NumberArg = ...,
        y: NumberArg = ...,
        w: NullDistanceArg = ...,
        h: NullDistanceArg = ...,
        angle: AngleArg = ...,
        dilate: bool = ...,
        **kwargs: Unpack[ImageURLArgs],
    ) -> GlyphRenderer[glyphs.ImageURL]: ...

    def line(self,
        x: NumberArg = ...,
        y: NumberArg = ...,
        **kwargs: Unpack[LineArgs],
    ) -> GlyphRenderer[glyphs.Line]: ...

    def mathml_glyph(self,
        x: NumberArg = ...,
        y: NumberArg = ...,
        text: StringArg = ...,
        angle: AngleArg = ...,
        x_offset: FloatArg = ...,
        y_offset: FloatArg = ...,
        **kwargs: Unpack[MathMLArgs],
    ) -> GlyphRenderer[glyphs.MathMLGlyph]: ...

    def ngon(self,
        x: NumberArg = ...,
        y: NumberArg = ...,
        radius: DistanceArg = ...,
        **kwargs: Unpack[NgonArgs],
    ) -> GlyphRenderer[glyphs.Ngon]: ...

    def patch(self,
        x: NumberArg = ...,
        y: NumberArg = ...,
        **kwargs: Unpack[PatchArgs],
    ) -> GlyphRenderer[glyphs.Patch]: ...

    def ray(self,
        x: NumberArg = ...,
        y: NumberArg = ...,
        length: DistanceArg = ...,
        angle: AngleArg = ...,
        **kwargs: Unpack[RayArgs],
    ) -> GlyphRenderer[glyphs.Ray]: ...

    def rect(self,
        x: NumberArg = ...,
        y: NumberArg = ...,
        width: DistanceArg = ...,
        height: DistanceArg = ...,
        angle: AngleArg = ...,
        dilate: bool = ...,
        **kwargs: Unpack[RectArgs],
    ) -> GlyphRenderer[glyphs.Rect]: ...

    def scatter(self,
        x: NumberArg = ...,
        y: NumberArg = ...,
        size: SizeArg = ...,
        angle: AngleArg = ...,
        marker: MarkerArg = ...,
        **kwargs: Unpack[ScatterArgs],
    ) -> GlyphRenderer[glyphs.Scatter]: ...

    def step(self,
        x: NumberArg = ...,
        y: NumberArg = ...,
        **kwargs: Unpack[StepArgs],
    ) -> GlyphRenderer[glyphs.Step]: ...

    def tex_glyph(self,
        x: NumberArg = ...,
        y: NumberArg = ...,
        text: StringArg = ...,
        angle: AngleArg = ...,
        x_offset: FloatArg = ...,
        y_offset: FloatArg = ...,
        **kwargs: Unpack[TeXArgs],
    ) -> GlyphRenderer[glyphs.TeXGlyph]: ...

    def text(self,
        x: NumberArg = ...,
        y: NumberArg = ...,
        text: StringArg = ...,
        angle: AngleArg = ...,
        x_offset: FloatArg = ...,
        y_offset: FloatArg = ...,
        **kwargs: Unpack[TextArgs],
    ) -> GlyphRenderer[glyphs.Text]: ...

    def wedge(self,
        x: NumberArg = ...,
        y: NumberArg = ...,
        radius: DistanceArg = ...,
        start_angle: AngleArg = ...,
        end_angle: AngleArg = ...,
        direction: Direction = ...,
        **kwargs: Unpack[WedgeArgs],
    ) -> GlyphRenderer[glyphs.Wedge]: ...

    # Vertical glyph methods (have parameter x but not y)

    def varea(self,
        x: NumberArg = ...,
        y1: NumberArg = ...,
        y2: NumberArg = ...,
        **kwargs: Unpack[VAreaArgs],
    ) -> GlyphRenderer[glyphs.VArea]: ...

    def varea_step(self,
        x: NumberArg = ...,
        y1: NumberArg = ...,
        y2: NumberArg = ...,
        **kwargs: Unpack[VAreaStepArgs],
    ) -> GlyphRenderer[glyphs.VAreaStep]: ...

    def vbar(self,
        x: NumberArg = ...,
        width: DistanceArg = ...,
        top: NumberArg = ...,
        bottom: NumberArg = ...,
        **kwargs: Unpack[VBarArgs],
    ) -> GlyphRenderer[glyphs.VBar]: ...

    def vspan(self,
        x: NumberArg = ...,
        **kwargs: Unpack[VSpanArgs],
    ) -> GlyphRenderer[glyphs.VSpan]: ...

    # Horizontal glyph methods (have parameter y but not x)

    def harea(self,
        x1: NumberArg = ...,
        x2: NumberArg = ...,
        y: NumberArg = ...,
        **kwargs: Unpack[HAreaArgs],
    ) -> GlyphRenderer[glyphs.HArea]: ...

    def harea_step(self,
        x1: NumberArg = ...,
        x2: NumberArg = ...,
        y: NumberArg = ...,
        **kwargs: Unpack[HAreaStepArgs],
    ) -> GlyphRenderer[glyphs.HAreaStep]: ...

    def hbar(self,
        y: NumberArg = ...,
        height: DistanceArg = ...,
        right: NumberArg = ...,
        left: NumberArg = ...,
        **kwargs: Unpack[HBarArgs],
    ) -> GlyphRenderer[glyphs.HBar]: ...

    def hspan(self,
        y: NumberArg = ...,
        **kwargs: Unpack[HSpanArgs],
    ) -> GlyphRenderer[glyphs.HSpan]: ...

    # Glyph methods without x nor y parameters

    def bezier(self,
        x0: NumberArg = ...,
        y0: NumberArg = ...,
        x1: NumberArg = ...,
        y1: NumberArg = ...,
        cx0: NumberArg = ...,
        cy0: NumberArg = ...,
        cx1: NumberArg = ...,
        cy1: NumberArg = ...,
        **kwargs: Unpack[BezierArgs],
    ) -> GlyphRenderer[glyphs.Bezier]: ...

    def hstrip(self,
        y0: NumberArg = ...,
        y1: NumberArg = ...,
        **kwargs: Unpack[HStripArgs],
    ) -> GlyphRenderer[glyphs.HStrip]: ...

    def hextile(self,
        q: NumberArg = ...,
        r: NumberArg = ...,
        **kwargs: Unpack[HexTileArgs],
    ) -> GlyphRenderer[glyphs.HexTile]: ...

    def multi_line(self,
        xs: Number1dArg = ...,
        ys: Number1dArg = ...,
        **kwargs: Unpack[MultiLineArgs],
    ) -> GlyphRenderer[glyphs.MultiLine]: ...

    def multipolygons(self,
        xs: Number3dArg = ...,
        ys: Number3dArg = ...,
        **kwargs: Unpack[MultiPolygonsArgs],
    ) -> GlyphRenderer[glyphs.MultiPolygons]: ...

    def patches(self,
        xs: Number1dArg = ...,
        ys: Number1dArg = ...,
        **kwargs: Unpack[PatchesArgs],
    ) -> GlyphRenderer[glyphs.Patches]: ...

    def quad(self,
        left: NumberArg = ...,
        right: NumberArg = ...,
        top: NumberArg = ...,
        bottom: NumberArg = ...,
        **kwargs: Unpack[QuadArgs],
    ) -> GlyphRenderer[glyphs.Quad]: ...

    def quadratic(self,
        x0: NumberArg = ...,
        y0: NumberArg = ...,
        x1: NumberArg = ...,
        y1: NumberArg = ...,
        cx: NumberArg = ...,
        cy: NumberArg = ...,
        **kwargs: Unpack[QuadraticArgs],
    ) -> GlyphRenderer[glyphs.Quadratic]: ...

    def segment(self,
        x0: NumberArg = ...,
        y0: NumberArg = ...,
        x1: NumberArg = ...,
        y1: NumberArg = ...,
        **kwargs: Unpack[SegmentArgs],
    ) -> GlyphRenderer[glyphs.Segment]: ...

    def vstrip(self,
        x0: NumberArg = ...,
        x1: NumberArg = ...,
        **kwargs: Unpack[VStripArgs],
    ) -> GlyphRenderer[glyphs.VStrip]: ...

    # Stack methods

    def harea_stack(self, stackers: Sequence[str], **kwargs) -> list[GlyphRenderer[glyphs.HArea]]: ...

    def hbar_stack(self, stackers: Sequence[str], **kwargs) -> list[GlyphRenderer[glyphs.HBar]]: ...

    def hline_stack(self, stackers: Sequence[str], **kwargs) -> list[GlyphRenderer[glyphs.Line]]: ...

    def varea_stack(self, stackers: Sequence[str], **kwargs) -> list[GlyphRenderer[glyphs.VArea]]: ...

    def vbar_stack(self, stackers: Sequence[str], **kwargs) -> list[GlyphRenderer[glyphs.VBar]]: ...

    def vline_stack(self, stackers: Sequence[str], **kwargs) -> list[GlyphRenderer[glyphs.Line]]: ...


class PolarsBokehAccessor(BokehAccessor):

    @property
    def source(self) -> ColumnDataSource: ...


class PandasBokehAccessor(BokehAccessor):

    @property
    def source(self) -> ColumnDataSource: ...

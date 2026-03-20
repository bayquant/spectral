#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
from __future__ import annotations
from functools import wraps
from inspect import Parameter
from inspect import Signature
from inspect import signature

# Other imports
from bokeh.plotting._docstring import generate_docstring
from bokeh.plotting._renderer import create_renderer

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

def glyph_method(glyphclass):
    def decorator(func):
        parameters = glyphclass.parameters()

        # TODO: send issue so that this signature only takes glyphclass.args instead of [x[0] for x in parameters]
        sigparams = (
            [Parameter("self", Parameter.POSITIONAL_OR_KEYWORD)]
            + [x[0] for x in parameters]
            + [Parameter("source", Parameter.KEYWORD_ONLY, default=None)]
            + [Parameter("kwargs", Parameter.VAR_KEYWORD)]
        )

        @wraps(func)
        def wrapped(self, *args, **kwargs):
            # Validate positional arguments against the glyph's declared positional field order.
            if len(args) > len(glyphclass._args):
                raise TypeError(f"{func.__name__} takes {len(glyphclass._args)} positional argument but {len(args)} were given")
            # Map positional inputs to their corresponding glyph kwargs by param name.
            for arg, param in zip(args, sigparams[1:]):
                kwargs[param.name] = arg
            # Default source comes from the accessor unless explicitly provided.
            kwargs.setdefault("source", self.source)
            # Preserve any coordinate context passed through a custom Figure subclass.
            if self.coordinates is not None:
                kwargs.setdefault("coordinates", self.coordinates)
            # Inspect/create synthetic fields on the source when required by the glyph.
            source = kwargs["source"]
            n = len(next(iter(source.data.values()), ()))
            # If x is required but missing, inject a 1..n index column into source and reference it by name.
            if "x" in glyphclass._args and "x" not in kwargs and "x" not in source.data:
                source.data["x"] = list(range(1, n + 1))
                kwargs["x"] = "x"
            # If y is required but missing, inject a 1..n index column into source and reference it by name.
            if "y" in glyphclass._args and "y" not in kwargs and "y" not in source.data:
                source.data["y"] = list(range(1, n + 1))
                kwargs["y"] = "y"
            # Delegate to Bokeh with normalized kwargs and possibly augmented source columns.
            return create_renderer(glyphclass, self.plot, **kwargs)

        wrapped.__signature__ = Signature(parameters=sigparams, return_annotation=signature(func).return_annotation)

        wrapped.__doc__ = generate_docstring(glyphclass, parameters, func.__doc__)

        return wrapped

    return decorator

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

from __future__ import annotations

# Standard library imports
from functools import wraps
from inspect import Parameter, Signature, signature

# Bokeh imports
from bokeh.util.deprecation import deprecated
from bokeh.plotting._docstring import generate_docstring
from bokeh.plotting._renderer import create_renderer


def glyph_method(glyphclass):
    def decorator(func):
        parameters = glyphclass.parameters()

        # TODO: send issue so that this signature only takes glyphclass.args instead of [x[0] for x in parameters]
        sigparams = [Parameter("self", Parameter.POSITIONAL_OR_KEYWORD)] + [x[0] for x in parameters] + [Parameter("kwargs", Parameter.VAR_KEYWORD)]

        @wraps(func)
        def wrapped(self, *args, **kwargs):
            if len(args) > len(glyphclass._args):
                raise TypeError(f"{func.__name__} takes {len(glyphclass._args)} positional argument but {len(args)} were given")
            for arg, param in zip(args, sigparams[1:]):
                kwargs[param.name] = arg
            kwargs.setdefault("source", self.source)
            if self.coordinates is not None:
                kwargs.setdefault("coordinates", self.coordinates)
            return create_renderer(glyphclass, self.plot, **kwargs)

        wrapped.__signature__ = Signature(parameters=sigparams, return_annotation=signature(func).return_annotation)

        wrapped.__doc__ = generate_docstring(glyphclass, parameters, func.__doc__)

        return wrapped

    return decorator
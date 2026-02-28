import unittest

import polars as pl
from bokeh.plotting import figure

from spectral.charts import polars_charts  # noqa: F401 - ensures namespace registration


class TestPolarsBokehAccessor(unittest.TestCase):
    def setUp(self) -> None:
        self.df = pl.DataFrame(
            {
                "x": [1, 2, 3],
                "y": [10, 20, 30],
                "y2": [12, 18, 36],
                "low": [8, 16, 24],
                "high": [14, 24, 40],
            }
        )

    def test_unknown_glyph_method_raises(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unknown method 'area'"):
            self.df.bokeh.glyph("area", data={"x": "x", "y": "y"})

    def test_missing_required_data_raises(self) -> None:
        with self.assertRaisesRegex(ValueError, "Missing required data parameters: y"):
            self.df.bokeh.glyph("line", data={"x": "x"})

    def test_non_string_data_parameter_raises(self) -> None:
        with self.assertRaisesRegex(ValueError, "Data parameter 'y' must be a column name"):
            self.df.bokeh.glyph("line", data={"x": "x", "y": 123})

    def test_missing_column_raises(self) -> None:
        with self.assertRaisesRegex(ValueError, "Column 'missing' not found in DataFrame"):
            self.df.bokeh.glyph("line", data={"x": "x", "y": "missing"})

    def test_unsupported_figure_kwarg_raises(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unsupported figure_kwargs: not_a_figure_prop"):
            self.df.bokeh.glyph(
                "line",
                data={"x": "x", "y": "y"},
                figure_kwargs={"not_a_figure_prop": 1},
            )

    def test_unsupported_glyph_kwarg_raises(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unsupported glyph_kwargs: not_a_line_prop"):
            self.df.bokeh.glyph(
                "line",
                data={"x": "x", "y": "y"},
                glyph_kwargs={"not_a_line_prop": 1},
            )

    def test_line_with_multiple_y_builds_multiple_renderers(self) -> None:
        fig = self.df.bokeh.glyph(
            "line",
            data={"x": "x", "y": ["y", "y2"]},
            glyph_kwargs={"line_width": 3},
        )

        self.assertEqual(len(fig.renderers), 2)
        self.assertEqual(fig.renderers[0].glyph.x, "x")
        self.assertEqual(fig.renderers[0].glyph.y, "y")
        self.assertEqual(fig.renderers[1].glyph.y, "y2")
        self.assertEqual(fig.renderers[0].glyph.line_width, 3)
        self.assertEqual(fig.renderers[1].glyph.line_width, 3)

    def test_default_x_uses_generated_index_column(self) -> None:
        df = self.df.drop("x")
        fig = df.bokeh.glyph("line", data={"y": "y"})

        self.assertEqual(fig.renderers[0].glyph.x, "__index")
        self.assertIn("__index", fig.renderers[0].data_source.column_names)
        self.assertNotIn("__index", df.columns)

    def test_existing_figure_is_reused_and_updated(self) -> None:
        existing = figure(width=250)
        fig = self.df.bokeh.glyph(
            "scatter",
            data={"x": "x", "y": "y"},
            figure=existing,
            figure_kwargs={"title": "Updated"},
        )

        self.assertIs(fig, existing)
        self.assertEqual(existing.title.text, "Updated")
        self.assertEqual(len(existing.renderers), 1)

    def test_accepted_kwargs_apis(self) -> None:
        fig_keys = self.df.bokeh.accepted_figure_kwargs()
        glyph_keys = self.df.bokeh.accepted_glyph_kwargs(method="line")

        self.assertIn("title", fig_keys)
        self.assertIn("line_width", glyph_keys)


if __name__ == "__main__":
    unittest.main()

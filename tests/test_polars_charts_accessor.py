import unittest

import polars as pl
from bokeh.plotting import figure

from spectral.charts import polars_accessors


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

    def test_unknown_glyph_raises(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unknown glyph 'area'"):
            self.df.bokeh.plot("area", glyph_params={"x": "x", "y": "y"})

    def test_missing_column_fails_through_bokeh_validation(self) -> None:
        with self.assertRaisesRegex(Exception, "missing"):
            self.df.bokeh.plot("line", glyph_params={"x": "x", "y": "missing"})

    def test_unsupported_figure_param_raises(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unsupported figure_params: not_a_figure_prop"):
            self.df.bokeh.plot(
                "line",
                glyph_params={"x": "x", "y": "y"},
                figure_params={"not_a_figure_prop": 1},
            )

    def test_default_x_uses_generated_index_column(self) -> None:
        df = self.df.drop("x")
        fig = df.bokeh.plot("line", glyph_params={"y": "y"})

        self.assertEqual(fig.renderers[0].glyph.x, "__index")
        self.assertIn("__index", fig.renderers[0].data_source.column_names)
        self.assertNotIn("__index", df.columns)

    def test_existing_figure_is_reused_and_updated(self) -> None:
        existing = figure(width=250)
        fig = self.df.bokeh.plot(
            "scatter",
            glyph_params={"x": "x", "y": "y"},
            figure=existing,
            figure_params={"title": "Updated"},
        )

        self.assertIs(fig, existing)
        self.assertEqual(existing.title.text, "Updated")
        self.assertEqual(len(existing.renderers), 1)

    def test_accepted_figure_params_api(self) -> None:
        fig_keys = self.df.bokeh.accepted_figure_params()
        self.assertIsInstance(fig_keys, set)
        self.assertIn("title", fig_keys)

    def test_accepted_figure_params_pattern_filter_returns_set(self) -> None:
        fig_keys = self.df.bokeh.accepted_figure_params(pattern="title")
        self.assertIsInstance(fig_keys, set)
        self.assertTrue(fig_keys)
        self.assertTrue(all("title" in key for key in fig_keys))


if __name__ == "__main__":
    unittest.main()

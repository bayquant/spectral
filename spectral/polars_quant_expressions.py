import polars as pl

@pl.api.register_expr_namespace("quant")
class QuantNamespace:
    def __init__(self, expr: pl.Expr):
        self._expr = expr

    def returns(
        self,
        periods: int = 1,
        over: str | None = None
    ) -> pl.Expr:
        """
        Compute simple percentage return for the expression.
        
        Parameters
        ----------
        periods : int
            Number of periods to shift (default is 1).
        over : str | None
            Optional grouping column (e.g. 'ticker'). If None, compute over the full series.
        """
        expr = (self._expr / self._expr.shift(n=periods)) - 1
        return expr.over(over).alias('return') if over is not None else expr.alias('return')

    def rolling_vol(
        self,
        window_size: int,
        weights: list[float] | None = None,
        *,
        min_samples: int | None = None,
        center: bool = False,
        ddof: int = 1,
        over: str | None = None
    ) -> pl.Expr:
        """
        Compute rolling volatility (standard deviation) for the expression.

        Parameters
        ----------
        over : str | None
            Optional grouping column (e.g. 'ticker').
        window_size : int
            Rolling window size.
        weights : list[float] | None
            Optional weights for weighted standard deviation.
        min_samples : int | None
            Minimum number of samples required to compute a value.
        center : bool
            Whether to center the window around the current row.
        ddof : int
            Delta degrees of freedom (default = 1 for sample std).
        """
        expr = self._expr.rolling_std(
            window_size=window_size,
            weights=weights,
            min_samples=min_samples,
            center=center,
            ddof=ddof,
        )
        return expr.over(over).alias('rolling_vol') if over is not None else expr.alias('rolling_vol')

    def rolling_beta(
        self,
        benchmark: pl.Expr,
        window_size: int,
        min_periods: int | None = None,
        ddof: int = 1,
        over: str | list[str] | None = None
    ) -> pl.Expr:
        """
        Compute rolling beta of this expression against a benchmark expression.

        Parameters
        ----------
        benchmark : pl.Expr
            Benchmark return column.
        window : int
            Rolling window size.
        min_periods : int | None
            Minimum number of observations required to compute a value.
        ddof : int
            Delta degrees of freedom for variance (default 1 for sample variance).
        over : str | list[str] | None
            Optional grouping column(s), e.g., "ticker".

        Returns
        -------
        pl.Expr
            Rolling beta expression
        """
        expr = (
            pl.rolling_cov(
                a=self._expr,
                b=benchmark,
                window_size=window_size,
                min_periods=min_periods,
                ddof=ddof
            ) 
            / benchmark.rolling_var(
                window_size=window_size,
                min_periods=min_periods,
                ddof=ddof
            )
        )

        return expr.over(over).alias('rolling_beta') if over is not None else expr.alias('rolling_beta')

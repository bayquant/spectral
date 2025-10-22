import polars as pl
from typing import Dict

class Portfolio:
    def __init__(self, df: pl.DataFrame, portfolio: Dict, benchmark: str):
        """
        Portfolio analytics class for computing total, systematic, and idiosyncratic returns.

        This class takes in a dataset of asset returns (including a benchmark) and a 
        dictionary of portfolio weights, then computes the time series of portfolio-level 
        returns and their decomposition into systematic and idiosyncratic components.

        Parameters
        ----------
        df : pl.DataFrame
            Polars DataFrame containing asset and benchmark data. 
            Must include at least the following columns:
            - 'timestamp' : datetime
            - 'ticker' : str
            - 'return' : float
            - 'beta' : float

        portfolio : Dict[str, float]
            Dictionary mapping asset tickers to their portfolio weights.
            Example: ``{"AAPL": 0.4, "MSFT": 0.6}``.

        benchmark : str
            Ticker symbol identifying the benchmark asset within `df`
        """
        self.df = df

        self.benchmark_df = df.filter(pl.col('ticker') == benchmark).select(
            ['timestamp', pl.col('return').alias('benchmark_return')]
        )
        self.assets_df = df.filter(pl.col('ticker').is_in(list(portfolio.keys())))

        _weights_df = (
            pl.DataFrame({'ticker': list(portfolio.keys()), 'weight': list(portfolio.values())})
        )
        self.assets_df = self.assets_df.join(other=_weights_df, on='ticker', how='inner')

    def compute_returns(self) -> pl.DataFrame:
        """Compute portfolio total, systematic, and idiosyncratic returns."""
        df = self.assets_df.join(self.benchmark_df, on='timestamp', how='inner')

        df = df.with_columns([
            (pl.col('return') * pl.col('weight')).alias('weighted_return'),
            (pl.col('rolling_beta') * pl.col('weight')).alias('weighted_beta')
        ])

        portfolio = (
            df.group_by('timestamp')
            .agg([
                pl.sum('weighted_return').alias('portfolio_return'),
                pl.sum('weighted_beta').alias('portfolio_beta'),
                pl.first('benchmark_return')
            ])
            .with_columns([
                (pl.col('portfolio_beta') * pl.col('benchmark_return')).alias('systematic_return'),
            ])
            .with_columns([
                (pl.col('portfolio_return') - pl.col('systematic_return')).alias('idiosyncratic_return'),
            ])
            .sort('timestamp')
        )


        return portfolio

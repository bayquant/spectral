import polars as pl
from _typeshed import Incomplete

class Portfolio:
    df: Incomplete
    benchmark_df: Incomplete
    assets_df: Incomplete
    def __init__(self, df: pl.DataFrame, portfolio: dict, benchmark: str) -> None: ...
    def compute_returns(self) -> pl.DataFrame: ...

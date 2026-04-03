from ..utils.rate_limiter import RateLimiter as RateLimiter
from _typeshed import Incomplete
from datetime import date, datetime
from massive.rest.models import Sort as Sort

client: Incomplete

def get_aggregate_bars(tickers: list[str], multiplier: int, timespan: str, from_: str | int | datetime | date, to: str | int | datetime | date, adjusted: bool | None = True, sort: str | Sort | None = None, limit: int | None = None): ...

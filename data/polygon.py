from functools import lru_cache
import polars as pl
from polygon import RESTClient
from typing import Optional
from typing import Union
from typing import Tuple
from typing import List
from typing import Dict
from typing import Any
from datetime import datetime
from datetime import date
from polygon.rest.models import Sort
from polygon.rest.models import Order

client = RESTClient(api_key='R4J4ILLkqB3zZedicoVuiyLOE44H_im4', pagination=False, trace=False)

@lru_cache(maxsize=2)
def _get_aggregate_bars(**kwargs):
    # TODO: work on timezone for seconds and minutes
    tickers = list(kwargs.pop('tickers'))
    
    aggs = []
    for ticker in tickers:
        for a in client.list_aggs(ticker=ticker, **kwargs):
            data = a.__dict__
            timestamp = data['timestamp']
            long_format = [
                {'timestamp': timestamp, 'ticker': ticker, 'metric': key, 'value': value}
                for key, value in data.items() if key != 'timestamp'
            ]
            aggs.extend(long_format)

    df = pl.DataFrame(data=aggs)

    # transform unix timestamp to daily format
    df = df.with_columns(
        pl.col("timestamp")
        .cast(pl.Datetime("ms"))
        .dt.replace_time_zone("UTC")
        .dt.convert_time_zone("America/New_York")
        .dt.truncate("1d")
    )

    # pivot polars dataframe to semi-wide format
    df = df.pivot(
        values='value',
        index=['timestamp', 'ticker'],
        on='metric'
    )
    
    return df.lazy()

def get_aggregate_bars( 
        tickers: List[str],
        multiplier: int,
        timespan: str,
        from_: Union[str, int, datetime, date],
        to: Union[str, int, datetime, date],
        adjusted: Optional[bool] = True,
        sort: Optional[Union[str, Sort]] = None,
        limit: Optional[int] = 5000,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False
        ):
    # create kwargs dictionary from local variables (copy to avoid mutating locals directly)
    kwargs = locals().copy()
    # convert tickers to tuple for caching (lru_cache)
    kwargs['tickers'] = tuple(kwargs['tickers'])
    
    df = _get_aggregate_bars(**kwargs)

    return df

import numpy as np
import pandas as pd


def make_bars(trades: pd.DataFrame, book: pd.DataFrame, freq: str = "1s") -> pd.DataFrame:
    """Time bars labelled by their close: the bar at t only holds events received before t."""
    step = pd.Timedelta(freq)

    b = book.assign(t=pd.to_datetime(book["recv_ns"], utc=True).dt.floor(freq) + step)
    quotes = b.groupby("t")[["bid", "bid_qty", "ask", "ask_qty"]].last()

    tr = trades.assign(
        t=pd.to_datetime(trades["recv_ns"], utc=True).dt.floor(freq) + step,
        signed_qty=np.where(trades["buyer_is_maker"], -trades["qty"], trades["qty"]),
        notional=trades["price"] * trades["qty"],
    )
    flow = tr.groupby("t").agg(
        volume=("qty", "sum"),
        signed_volume=("signed_qty", "sum"),
        trades=("qty", "size"),
        notional=("notional", "sum"),
    )

    index = pd.date_range(quotes.index.min(), quotes.index.max(), freq=freq, name="t")
    bars = quotes.reindex(index).ffill()
    bars = bars.join(flow.reindex(index).fillna(0.0))
    bars["trades"] = bars["trades"].astype(int)
    bars["mid"] = (bars["bid"] + bars["ask"]) / 2
    return bars

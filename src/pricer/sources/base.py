from typing import Protocol

import pandas as pd

TRADE_COLUMNS = ["recv_ns", "price", "qty", "buyer_is_maker"]
BOOK_COLUMNS = ["recv_ns", "bid", "bid_qty", "ask", "ask_qty"]


class MarketSource(Protocol):
    """Normalized, exchange-agnostic market data. recv_ns is the local receive time (UTC ns)."""

    def trades(self) -> pd.DataFrame: ...

    def book(self) -> pd.DataFrame: ...

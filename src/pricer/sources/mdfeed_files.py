import gzip
import json
from collections.abc import Iterator
from pathlib import Path

import pandas as pd

from pricer.sources.base import BOOK_COLUMNS, TRADE_COLUMNS


def _open(path: Path):
    return gzip.open(path, "rt") if path.suffix == ".gz" else path.open()


def _records(paths: list[Path]) -> Iterator[tuple[int, dict]]:
    """Yield (recv_ns, data) from mdfeed raw lines: '<recv_ns> {"stream": ..., "data": ...}'."""
    for path in paths:
        with _open(path) as f:
            for line in f:
                head, _, body = line.partition(" ")
                if not body:
                    continue
                yield int(head), json.loads(body)["data"]


class MdfeedFileSource:
    """Reads mdfeed raw capture files (spike format) for one symbol."""

    def __init__(self, data_dir: Path, symbol: str = "btcusdc"):
        self.data_dir = Path(data_dir)
        self.symbol = symbol.lower()

    def _files(self, stream: str) -> list[Path]:
        files = sorted(self.data_dir.rglob(f"{self.symbol}_{stream}*"))
        if not files:
            raise FileNotFoundError(f"no {self.symbol} {stream} files under {self.data_dir}")
        return files

    def trades(self) -> pd.DataFrame:
        rows = [
            (recv, float(d["p"]), float(d["q"]), bool(d["m"]))
            for recv, d in _records(self._files("aggTrade"))
        ]
        return _frame(rows, TRADE_COLUMNS)

    def book(self) -> pd.DataFrame:
        rows = [
            (recv, float(d["b"]), float(d["B"]), float(d["a"]), float(d["A"]))
            for recv, d in _records(self._files("bookTicker"))
        ]
        return _frame(rows, BOOK_COLUMNS)


def _frame(rows: list[tuple], columns: list[str]) -> pd.DataFrame:
    df = pd.DataFrame(rows, columns=columns)
    return df.sort_values("recv_ns", kind="stable").reset_index(drop=True)

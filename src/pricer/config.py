import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    mdfeed_data_dir: Path
    symbol: str
    data_dir: Path

    @property
    def db_path(self) -> Path:
        return self.data_dir / "predictions.sqlite"


def load_settings() -> Settings:
    return Settings(
        mdfeed_data_dir=Path(
            os.environ.get("PRICER_MDFEED_DATA_DIR", "~/code/mdfeed/data")
        ).expanduser(),
        symbol=os.environ.get("PRICER_SYMBOL", "btcusdc").lower(),
        data_dir=Path(os.environ.get("PRICER_DATA_DIR", "data")).expanduser(),
    )

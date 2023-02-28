from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    raw_data: Path
    ingested_train_dir: Path
    ingested_test_dir: Path

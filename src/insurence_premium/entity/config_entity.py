from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    raw_data: Path
    ingested_train_dir: Path
    ingested_test_dir: Path

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    schema_file_path:Path
    report_file_path: Path
    report_page_file_path: Path
    
@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    transformed_train_file_path: Path
    transformed_test_file_path: Path
    preprocessing_dir: Path
    preprocessing_file_path: Path    

@dataclass(frozen=True)
class DataModelTrainerConfig:
    root_dir: Path
    trained_model_file_path: Path
    base_accuracy: float
    model_config_file_path: Path


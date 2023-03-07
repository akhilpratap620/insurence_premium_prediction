from insurence_premium.constant import *
from insurence_premium.util.common import read_yaml, create_directories
import os
from pathlib import Path
from insurence_premium.entity import DataIngestionConfig, DataValidationConfig
from insurence_premium import logger
import sys


class ConfigurationManager:
    def __init__(
        self, config_filepath=CONFIG_FILE_PATH, params_filepath=PARAMS_FILE_PATH
    ):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            ingestion_config = self.config.data_ingestion
            logger.info("start definig data ingestion config")
            data_ingestion_config = DataIngestionConfig(
                root_dir=Path(ingestion_config.root_dir),
                raw_data=Path(ingestion_config.raw_data),
                ingested_train_dir=Path(ingestion_config.ingested_train_dir),
                ingested_test_dir=Path(ingestion_config.ingested_test_dir),
            )
            return data_ingestion_config
            logger.info(
                f"data ingestion config created successfully: [{data_ingestion_config}]"
            )
        except Exception as e:
            raise e

    def get_validation_config(self) -> DataValidationConfig:
        try:
            logger.info("start definig data ingestion validation")
            validation_config = self.config.data_validation

            data_validation_config = DataValidationConfig(
                root_dir=Path(validation_config.root_dir),
                schema_file_path=Path()
                report_file_path=Path(validation_config.report_file_path),
                report_page_file_path=Path(validation_config.report_page_file_path),
            )
            return data_validation_config

        except Exception as e:
            raise e    

from insurence_premium.constant import *
from insurence_premium.util.common import read_yaml, create_directories
from pathlib import Path
from insurence_premium.entity import DataIngestionConfig, DataValidationConfig,DataTransformationConfig ,DataModelTrainerConfig,DataModelEvaluation
from insurence_premium import logger




class ConfigurationManager:
    def __init__(
        self ,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):

        self.config =read_yaml(config_filepath)
        self.params =read_yaml(params_filepath)
        self.time_stamp=CURRENT_TIME_STAMP

        create_directories([self.config.artifacts_root])
    
    def get_data_ingestion_config(self,)->DataIngestionConfig:
        ingestion_config =self.config.data_ingestion
        data_ingestion_config = DataIngestionConfig(
            root_dir=Path(ingestion_config.root_dir),
            raw_data=Path(ingestion_config.raw_data),
            ingested_train_dir=Path(ingestion_config.ingested_train_dir),
            ingested_test_dir =Path(ingestion_config.ingested_test_dir)
        )
        return data_ingestion_config

    
    def get_data_validation_config(self)->DataValidationConfig:
        validation_config =self.config.data_validation

        data_validation_config =DataValidationConfig(
            root_dir=Path(validation_config.root_dir),
            schema_file_path=Path(validation_config.schema_file_path),
            report_file_path=Path(validation_config.report_file_path),
            report_page_file_path=Path(validation_config.report_page_file_path)
            
        )
        return data_validation_config

    def get_data_transformation_config(self)->DataTransformationConfig:
        try:
            transformation_config=self.config.data_transformation
            data_transformation_config =DataTransformationConfig(
                root_dir =Path(transformation_config.root_dir),
                transformed_train_file_path=Path(transformation_config.transformed_train_file_path),
                transformed_test_file_path=Path(transformation_config.transformed_test_file_path),
                preprocessing_dir=Path(transformation_config.preprocessing_dir),
                preprocessing_file_path=Path(transformation_config.preprocessing_file_path)
                )
            return data_transformation_config    
            logging.info(f"return: [{data_ingestion_config}]")
        except Exception as e:
            raise e  
             
    def get_model_trainer_config(self) -> DataModelTrainerConfig:
        try:
            model_trainer_config = self.config.data_model_trainer

            data_model_trainer_config = DataModelTrainerConfig(
                root_dir=Path(model_trainer_config.root_dir),
                trained_model_file_path=
                    model_trainer_config.trained_model_file_path
                ,
                base_accuracy=model_trainer_config.base_accuracy,
                model_config_file_path=Path(
                    model_trainer_config.model_config_file_path
                ),
            )
            return data_model_trainer_config
            logger.info(f"model trainer config : {data_model_trainer_config}")
        except Exception as e:
            raise e 
            
    def get_model_evaluation_config(self):
        try:
            data_evaluation_config=self.config.data_model_evaluation
            model_evaluation_file_path=os.path.join(data_evaluation_config.root_dir ,data_evaluation_config.model_evaluation_file_name)
            model_evaluation_config=DataModelEvaluation(
                root_dir= Path(data_evaluation_config.root_dir),
                model_evaluation_file_path= Path(model_evaluation_file_path),
                time_stamp= self.time_stamp

                
            )
            return model_evaluation_config
        except Exception as e:
            raise e            
from insurence_premium.logger import logging
from insurence_premium.exception import PremiumException
from insurence_premium.constant import *
from insurence_premium.util.util import read_yaml
from insurence_premium.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
import os ,sys

ROOT_DIR = os.getcwd()




class Configuration:
    def __init__(self , config_file_path:str ,current_time_stamp:str = CURRENT_TIME_STAMP)->None:
        
        self.time_stamp=current_time_stamp
        self.config=read_yaml(file_path=config_file_path)
        self.training_pipeline_config = self.get_training_pipeline_config()

        
        

    def get_data_ingestion_config(self,)->DataIngestionConfig:
        try:
            artifact_dir =self.training_pipeline_config.artifact_dir
            data_ingestion_artifact = os.path.join(artifact_dir , DATA_INGESTION_ARTIFACT_DIR , self.time_stamp)
            data_ingestion_info = self.config[DATA_INGESTION_CONFIG_KEY]

            raw_data = os.path.join(data_ingestion_artifact ,data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY])

            data_ingestion_dir =os.path.join(data_ingestion_artifact ,data_ingestion_info[DATA_INGESTION_INGESTED_DIR_NAME_KEY])

            ingested_train_dir=os.path.join(data_ingestion_dir ,data_ingestion_info[DATA_INGESTION_TRAIN_DIR_KEY])
            ingested_test_dir=os.path.join(data_ingestion_dir ,data_ingestion_info[DATA_INGESTION_TEST_DIR_KEY])



            data_ingestion_config=DataIngestionConfig(
                                                    raw_data=raw_data,
                                                    data_ingestion_dir=data_ingestion_dir,
                                                    ingested_train_dir=ingested_train_dir,
                                                    ingested_test_dir=ingested_test_dir
           ) 
            logging.info(f"Data Ingension Config:{data_ingestion_config}") 
            return data_ingestion_config
            
            




        except Exception as e:
            raise PremiumException(e, sys) from e

    def get_data_validation_config(self):
        try:
            pass
        except Exception as e:
            raise PremiumException(e, sys) from e
    def get_data_transformer_config(self):
        try:
            pass
        except Exception as e:
            raise PremiumException(e, sys) from e
    def get_model_trainer_config(self):
        pass
    def get_model_pusher_config(self):
        pass
    def get_training_pipeline_config(self)->TrainingPipelineConfig:
        try:
            config_info=self.config
            training_pipeline_config=config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(ROOT_DIR,training_pipeline_config[TRAINING_PIPELINE_NAME],training_pipeline_config[TRAINING_ARTIFACT_DIR_KEY ])
            training_pipeline_config =TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info("training pipeline config:{training_pipeline_config}")
            return training_pipeline_config
        except Exception as e:
            raise PremiumException(e,sys) from e
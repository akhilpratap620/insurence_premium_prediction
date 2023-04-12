from insurence_premium.entity import DataModelPusher
from insurence_premium.config import ConfigurationManager
from insurence_premium import logger
from insurence_premium.entity.model_entity import ModelEvaluationArtifact 
from insurence_premium.constant import *
from insurence_premium.util.common import read_yaml
from insurence_premium import logger


import os, sys
import shutil


class ModelPusher:

    def __init__(self, config:ConfigurationManager):
        try:
            logger.info(f"{'>>' * 30}Model Pusher log started.{'<<' * 30} ")
            self.config= ConfigurationManager()
            self.model_pusher_config=self.config.get_model_pusher_config()
            self.model_evaluation_config=self.config.get_model_evaluation_config()

        except Exception as e:
            raise e

    def export_model(self):
        try:
            evaluated_model_file_path = str(self.model_evaluation_config.model_evaluation_file_path)
            logger.info(f"{evaluated_model_file_path}")
            export_model_file_path = self.model_pusher_config.model_pusher_file_path

            export_dir=os.path.dirname(export_model_file_path)
            logger.info(f"Exporting model file: [{export_model_file_path}]")
            os.makedirs(export_dir, exist_ok=True)

            shutil.copy(src=evaluated_model_file_path, dst=export_model_file_path)
            #we can call a function to save model to Azure blob storage/ google cloud strorage / s3 bucket
            logger.info(
                f"Trained model: {evaluated_model_file_path} is copied in export dir:[{export_model_file_path}]")

            
            
            return export_model_file_path
        except Exception as e:
            raise e

    

    def __del__(self):
        logger.info(f"{'>>' * 20}Model Pusher log completed.{'<<' * 20} ")
import os
from insurence_premium import logger
from insurence_premium.util import load_object
from insurence_premium.config import ConfigurationManager
import pandas as pd

class PredictPipeline:
    def __init__(self):
        self.config=ConfigurationManager()
        self.model_trainer_config=self.config.get_model_trainer_config()
        self.model_transform_config=self.config.get_data_transformation_config()


    def predict(self,features):
        try:
            model_path=self.model_trainer_config.trained_model_file_path
            preprocessor_path=self.model_transform_config.preprocessing_file_path
            model=load_object(file_path=model_path)
            
            preds=model.predict(features)
            return preds
        except Exception as e:
            raise e    

class CustomData:

    def __init__(self,age: int,sex: str,bmi: float,children: int,smoker: str,region: str):
        self.age=age
        self.sex=sex
        self.bmi=bmi
        self.children=children
        self.smoker=smoker
        self.region=region

    def get_data_as_frame(self):
        try:
            custom_data={
                "age":[self.age],
                "sex":[self.sex],
                "bmi":[self.bmi],
                "children":[self.children],
                "smoker":[self.smoker],
                "region":[self.region]
            }
            return pd.DataFrame(custom_data)
            logger.info(f"age:{type(self.age)} ,bmi:{type(self.bmi)}")
        except Exception as e:
            raise e    
    
    
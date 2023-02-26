from insurence_premium.exception import PremiumException
from insurence_premium.logger import logging
from insurence_premium.entity.config_entity import DataIngestionConfig
import csv
import pandas as pd
from pathlib import Path
from insurence_premium.entity.artifact_entity import DataIngestionArtifact
from insurence_premium.constant import  *
from insurence_premium.cassandra_db.cassandra_db import CassandraDatabaseManager
import sys , os
from insurence_premium.config.configuration import Configuration



class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'='*20} Data Ingestion Log Started.{'='*20}")
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise PremiumException(e,sys) from e

    def download_data(self):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data
            

            os.makedirs(raw_data_dir , exist_ok = True)
            file_name="insurence_premium.csv"
            raw_data_file_path =os.path.join(
                raw_data_dir , file_name
            ) 
            db_file_path="c:\\Users\\somit\\Downloads\\project_ineuron\\insurence_premium_prediction\\config\\cassandra_db.yaml" 

            df=CassandraDatabaseManager(db_file_path=db_file_path).data_finder()
            df.to_csv(raw_data_file_path) 
            return raw_data_file_path


        except Exception as e:
            raise PremiumException(e,sys) from e
    def extract_train_test_split(self):
        try:
            pass
        except Exception as e:
            raise PremiumException(e, sys) from e

    def initiate_data_ingestion(self):
        try:
            pass
        except Exception as e:
            raise PremiumException(e, sys) from e
               
    
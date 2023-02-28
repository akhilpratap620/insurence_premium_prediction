from insurence_premium.exception import PremiumException
from insurence_premium.logger import logger
from insurence_premium.entity import DataIngestionConfig
import csv
import pandas as pd
from pathlib import Path
from insurence_premium.constant import  *
from insurence_premium.cassandra_db.cassandra_db import CassandraDatabaseManager
import sys  
import os
from insurence_premium.config import ConfigurationManager



import os

class DataIngestion:
    def __init__(self , config:DataIngestionConfig):
        self.config =config

    def download_data(self):
        try:
            raw_data = self.config.raw_data
            raw_data_dir ,file_name=os.path.split(raw_data)

            os.makedirs(raw_data_dir , exist_ok = True)
            
            raw_data_file_path =os.path.join(
                raw_data_dir , file_name
            ) 
            db_file_path = DB_FILE_PATH

            df=CassandraDatabaseManager(db_file_path=db_file_path).data_finder()
            df.to_csv(raw_data_file_path) 
            return raw_data_file_path

        except Exception as e:
            raise e

    def clean_data(self):
        try:
            pass
        except Exception as e:
            raise PremiException(e,sys) from e
            
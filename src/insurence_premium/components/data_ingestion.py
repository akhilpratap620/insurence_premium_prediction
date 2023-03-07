from insurence_premium import logger
from insurence_premium.entity import DataIngestionConfig
import csv
import pandas as pd
from pathlib import Path
from insurence_premium.constant import  *
from insurence_premium.cassandra_db.cassandra_db import CassandraDatabaseManager
import sys  
import os
from insurence_premium.config import ConfigurationManager
from sklearn import preprocessing
from sklearn.model_selection import StratifiedShuffleSplit
import numpy as np
from insurence_premium.util import create_directories

import os

class DataIngestion:
    def __init__(self , config:DataIngestionConfig):
        logger.info("_____________data_ingestion_stage start_____________")
        self.config =config

    def download_data(self):
        try:
            logger.info("trying to fetch data from db")
            raw_data = self.config.raw_data
            raw_data_dir ,file_name=os.path.split(raw_data)

            os.makedirs(raw_data_dir , exist_ok = True)
            
            raw_data_file_path =os.path.join(
                raw_data_dir , file_name
            ) 
            db_file_path = DB_FILE_PATH
            logger.info("____start data downloading______")
            df=CassandraDatabaseManager(db_file_path=db_file_path).data_finder()
            df.to_csv(raw_data_file_path) 
            logger.info("data download successfully")
            return raw_data_file_path

        except Exception as e:
            raise e

    def split_data_as_train_test(self):
        try:
            data_file_path=self.config.raw_data
            logger.info("start data reading from raw data")
            data=pd.read_csv(data_file_path)
            logger.info("data readed successfully")



            
            label_encoder = preprocessing.LabelEncoder()
            logger.info("label encoding to region column")
            data['region_cat'] =label_encoder.fit_transform(data['region'])
            data['region_cat']=data['region_cat']+1
            data["region_label"] = pd.cut(
            data["region_cat"],
            bins=[0,1,2,3,4],
            labels=[1,2,3,4]
            )
            logger.info("try to do stratified split")
            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

            for train_index,test_index in split.split(data, data["region_label"]):
                strat_train_set = data.loc[train_index].drop(["region_cat","region_label"],axis=1)
                strat_test_set = data.loc[test_index].drop(["region_cat","region_label"],axis=1)
            logger.info("split done successfully")

            train_file_path = self.config.ingested_train_dir

            test_file_path = self.config.ingested_test_dir

            if strat_train_set is not None:
                logger.info("try to create directories with train file path")
                train_dir , file_name=os.path.split(train_file_path)
                create_directories([train_dir])
                strat_train_set.to_csv(train_file_path,index=False)
                logger.info("train data save successfully")
            else:
                logger.info("there is no data in strat_train")    

            if strat_test_set is not None:
                logger.info("try to create test directories")
                test_dir , file_name=os.path.split(test_file_path)

                create_directories([test_dir]) 
                strat_test_set.to_csv(test_file_path ,index=False)
                logger.info("train data save successfully")
            else:
                logger.info("there is no data in strat_test") 

            logger.info(f"train test split done successfully train:{train_file_path} ,test:{test_file_path}")
            logger.info(f"{'>>'*20}Data Ingestion log completed.{'<<'*20} \n\n")   

        except Exception as e:
            raise e

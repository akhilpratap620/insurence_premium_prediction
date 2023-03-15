from insurence_premium.constant import *
from insurence_premium.util.common import read_yaml ,create_directories ,save_json
from insurence_premium import logger
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import json
from insurence_premium.config import ConfigurationManager
import pandas as pd



class DataValidation:
    def __init__(self ,config:ConfigurationManager):
        logger.info("_____________data_validation_start_____________")
        self.config =ConfigurationManager()
        self.data_ingestion_config =ConfigurationManager().get_data_ingestion_config()
        self.data_validation_config=ConfigurationManager().get_data_validation_config()
        

    def get_train_test_data(self):
        try:
            train_file_path=self.data_ingestion_config.ingested_train_dir
            test_file_path=self.data_ingestion_config.ingested_test_dir
            train_df=pd.read_csv(train_file_path ,index_col='Unnamed: 0')
            test_df=pd.read_csv(test_file_path,index_col='Unnamed: 0')

            return train_df ,test_df
            
        except Exception as e:
            raise e    

    def is_train_test_file_exist(self):
        try:
            is_train_file_exist=False
            is_test_file_exist=False

            train_file_path=self.data_ingestion_config.ingested_train_dir
            test_file_path=self.data_ingestion_config.ingested_test_dir
            logger.info("checking if train and test file exists")
            is_train_file_exist=os.path.exists(train_file_path)
            is_test_file_exist=os.path.exists(test_file_path)
            logger.info("Both training and test file path exist")

            return is_train_file_exist and is_test_file_exist

            if not (is_train_file_exist and is_train_file_exist):
                raise Exception(f"train or test file missing")
            logger.info(f"train_file: {train_file_path} ,test_file: {test_file_path}") 


        except Exception as e:
            raise e

    def validate_schema(self):
        try:
            logger.info("laoding train file path")
            train_file_path =self.data_ingestion_config.ingested_train_dir
            logger.info("started reading schema.yaml ")
            schema_file_path=Path(self.data_validation_config.schema_file_path)
            schema=read_yaml(schema_file_path)
            logger.info("read schema.yaml successfully")
            logger.info("reading data as a data frame")
            df =pd.read_csv(train_file_path ,index_col='Unnamed: 0')
            logger.info(" started data validating according to schema data")
            data_type=True
            if data_type:

                for i in df.columns:
                    df[i].dtypes==schema[i]
                    logger.info(f"data column: {i} is matching with schema data set")
            else:
                logger.info(f"datatypes are not maching column:{i} with schema data")  
            logger.info("data validation according to schema data is successfull")          
        except Exception as e:
            raise e        

    def get_and_save_data_drift_report(self):
        try:
            logger.info("initiating profile")
            profile =Profile(sections=[DataDriftProfileSection()])
            logger.info("reading train and test data frame")
            train_df,test_df =self.get_train_test_data()
            profile.calculate(train_df,test_df)
            logger.info("calculating data drifting")
            report=json.loads(profile.json())
            report_file_path = self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir , exist_ok=True) 
            

            save_json(report_file_path,report)
            logger.info("report generated successfully")
            return report
        except Exception as e:
            raise e    

    def save_data_drift_report_page(self):
        try:
            dashboard =Dashboard(tabs=[DataDriftTab()])
            train_df,test_df =self.get_train_test_data()
            dashboard.calculate(train_df,test_df)
            report_page_file_path=self.data_validation_config.report_page_file_path
            report_page_dir =os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir , exist_ok=True)

            dashboard.save(report_page_file_path)
            logger.info("generated successfully")
        except Exception as e:
            raise e        

    def is_data_drift_found(self):
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True
            logger.info("____________Data Validation part Completed ___________")
        except Exception as e:
            raise e   
import os
from datetime import datetime
from pathlib import Path

def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

ROOT_DIR ="C:\\Users\\somit\\Downloads\\project_ineuron\\insurence_premium_prediction"

CONFIG_DIR="config"

CONFIG_FILE_NAME ="config.yaml"
CONFIG_FILE_PATH =Path(os.path.join(CONFIG_DIR , CONFIG_FILE_NAME))

PARAMS_FILE_NAME ="params.yaml"
PARAMS_FILE_PATH =Path(PARAMS_FILE_NAME)

CURRENT_TIME_STAMP=get_current_time_stamp()

#data base varibales 

DB_FILE_NAME ="cassandra_db.yaml"
DB_FILE_PATH =Path(os.path.join(ROOT_DIR ,CONFIG_DIR,DB_FILE_NAME))
CLIENT_ID_KEY = "client_id"
CLIENT_SECRET_KEY ="client_secret"
SECRET_BUNDLE_KEY="secret_bundle_path"

#Training pipeline constant variable

TRAINING_PIPELINE_CONFIG_KEY="training_pipeline_config"
TRAINING_ARTIFACT_DIR_KEY ="artifact_dir"
TRAINING_PIPELINE_NAME="pipeline_name"

#data ingestion constant variable
DATA_INGESTION_CONFIG_KEY= "data_ingestion_config"
DATA_INGESTION_ARTIFACT_DIR = "data_ingestion"
DATA_INGESTION_DOWNLOAD_URL_KEY = "dataset_download_url"
DATA_INGESTION_RAW_DATA_DIR_KEY = "raw_data_dir"
DATA_INGESTION_UNZIPPED_DOWNLOAD_DIR_KEY = "unzipped_download_dir"
DATA_INGESTION_INGESTED_DIR_NAME_KEY = "ingested_dir"
DATA_INGESTION_TRAIN_DIR_KEY = "ingested_train_dir"
DATA_INGESTION_TEST_DIR_KEY = "ingested_test_dir"


#data validation constant variable
DATA_VALIDATION_CONFIG_KEY ="data_validation_config"
DATA_VALIDATION_ARTIFACT_DIR ="data_validation"
DATA_VALIDATION_SCHEMA_DIR_KEY ="schema_dir"
DATA_VALIDATION_REPORT_FILE_NAME_KEY = "report_file_name"
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY = "report_page_file_name"

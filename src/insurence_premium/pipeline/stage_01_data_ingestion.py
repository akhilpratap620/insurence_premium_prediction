import os, sys
from insurence_premium.config import ConfigurationManager
from insurence_premium.components.data_ingestion import DataIngestion
from insurence_premium import logger

def main():
    logger.info("try to get obj of Configuration mannager") 
    con_obj = ConfigurationManager()
    logger.info("loaded successfully obj of Configuration mannager") 
    data_ingestion_config = con_obj.get_data_ingestion_config()
    logger.info("get data ingestion condig obj successfully") 
    data_ingestion = DataIngestion(config=data_ingestion_config)
    logger.info("created obj of data ingestion components") 
    data_ingestion.download_data()
    logger.info("downloaded data successfully")
    data_ingestion.split_data_as_train_test()
    logger.info("data split done successfully")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise e

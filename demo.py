from insurence_premium.exception import PremiumException
from insurence_premium.logger import logging
from insurence_premium.config.configuration import Configuration
import os , sys

def main():
    try:
        logging.info("configuation stage started")
        config_path= os.path.join("config" ,"config.yaml")
        
        data_ingestion_config=Configuration(config_file_path=config_path).get_data_ingestion_config()
        print(data_ingestion_config)
        logging.info("data_ingestion_stage:[{data_ingestion_config}]")


    except Exception as e:
        raise PremiumException(e, sys) from e

if __name__=="__main__":
    main()

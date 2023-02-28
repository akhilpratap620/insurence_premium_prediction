from insurence_premium.exception import PremiumException
import os,sys
from insurence_premium.config import ConfigurationManager
from insurence_premium.components.data_ingestion import DataIngestion
def main():
    
    con_obj=ConfigurationManager()
    data_ingestion_config=con_obj.get_data_ingestion_config()
    data_ingestion =DataIngestion(config=data_ingestion_config)
    data_ingestion.download_data()
    data_ingestion.split_data_as_train_test()


if  __name__=='__main__':
    try:
        
        main()
    except Exception as e:
        raise PremiumException(e,sys) from e    
from insurence_premium.config.configuration import ConfigurationManager
from insurence_premium import logger
from insurence_premium.components import DataValidation 
import pandas as pd

def main():
    config_obj = ConfigurationManager()
    data_validation_config = config_obj.get_data_validation_config()
    data_validation = DataValidation(config=data_validation_config)
    data_validation.get_train_test_data()
    data_validation.is_train_test_file_exist()
    data_validation.validate_schema()
    data_validation.get_and_save_data_drift_report()
    data_validation.save_data_drift_report_page()
    data_validation.is_data_drift_found()

if __name__ =="__main__":
    try:
        main()
    except Exception as e:
        raise e

            


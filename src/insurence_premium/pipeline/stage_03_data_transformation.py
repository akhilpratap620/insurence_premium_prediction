from insurence_premium.config.configuration import ConfigurationManager
from insurence_premium import logger
from insurence_premium.components import DataTransformation
import pandas as pd

def main():
    con_obj = ConfigurationManager()
    data_transformation= DataTransformation()
    data_transformation.get_data_transformer()
    data_transformation.transformed_data()

if __name__ =="__main__":
    try:
        main()
    except Exception as e:
        raise e

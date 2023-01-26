from insurence_premium.exception import PremiumException
from insurence_premium.logger import logging
import yaml ,sys



def read_yaml(file_path:str)->dict:
    try:
        with open(file_path ,'rb') as file:
            return yaml.safe_load(file)
            
            
    except Exception as e:
        raise PremiumException(e,sys) from e 
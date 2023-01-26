from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from insurence_premium.util.util import read_yaml
from insurence_premium.constant import *
from insurence_premium.exception import PremiumException
from insurence_premium.logger import logging
import pandas as pd






class CassandraDatabaseManager:
    """
    CassandraDatabaseManager will provide functionality to perform CRUD operation.
    CassandraDatabaseManager is high level api.
    """

    def __init__(self , db_file_path:str):
        try:

            self.table="insurance"
            self.key_space ="new_row"

            self.db_info=read_yaml(file_path=db_file_path)

        except Exception as e:
            raise PremiumException(e, sys) from e
    def data_finder(self):
        try:
            self.db_info=self.db_info
            cloud_config= {
            'secure_connect_bundle': self.db_info[SECRET_BUNDLE_KEY]
            }
            auth_provider = PlainTextAuthProvider(self.db_info[CLIENT_ID_KEY], self.db_info[CLIENT_SECRET_KEY])
            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            session = cluster.connect("new_row")

            row=session.execute('SELECT * FROM insurance')
            self.a=[]

            if row:
                for i in row:
                    self.a.append(i)
            logging.info("data store in list successfully")
            df=pd.DataFrame(self.a)
            return df.to_csv("insurence_premium")   

            logging.info("df is found ")     

      

                
    

        except Exception as e:

            raise PremiumException(e, sys) from e 

        

 


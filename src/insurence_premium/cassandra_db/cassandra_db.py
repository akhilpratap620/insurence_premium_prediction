from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from insurence_premium.util.common import read_yaml
from insurence_premium.constant import *
from insurence_premium import logger
import pandas as pd
import sys
from pathlib import Path


class CassandraDatabaseManager:
    """
    CassandraDatabaseManager will provide functionality to perform CRUD operation.
    CassandraDatabaseManager is high level api.
    """

    def __init__(self, db_file_path: Path):
        try:

            self.table = "insurance"
            self.key_space = "new_row"

            self.db_info = read_yaml(path_to_yaml=db_file_path)

        except Exception as e:
            raise e

    def data_finder(self):
        """data finder will help to fetch data from cassandra database"""
        try:
            self.db_info = self.db_info
            logger.info("try to connect with db")
            cloud_config = {"secure_connect_bundle": self.db_info[SECRET_BUNDLE_KEY]}
            auth_provider = PlainTextAuthProvider(
                self.db_info[CLIENT_ID_KEY], self.db_info[CLIENT_SECRET_KEY]
            )
            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            logger.info("db connection successfully stablish")
            session = cluster.connect("new_row")

            row = session.execute("SELECT * FROM insurance")
            self.a = []

            if row:
                for i in row:
                    self.a.append(i)
            logger.info("data store in list successfully")
            df = pd.DataFrame(self.a)
            return df

            logger.info("data found successfully")
        except Exception as e:
            raise e

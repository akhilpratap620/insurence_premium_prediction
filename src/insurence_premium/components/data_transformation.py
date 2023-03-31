from insurence_premium import logger
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import pandas as pd
from insurence_premium.constant import *
from insurence_premium.entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
)
from insurence_premium.util.common import (
    read_yaml,
    create_directories,
    save_numpy_data,
    save_object,
)
from insurence_premium.config import ConfigurationManager


class DataTransformation:
    def __init__(self):

        self.config = ConfigurationManager()
        self.data_validation_config = self.config.get_data_validation_config()
        self.data_ingestion_config = self.config.get_data_ingestion_config()
        self.data_transformation_config = self.config.get_data_transformation_config()

    @staticmethod
    def load_data(file_path: str, schema_file_path: str) -> pd.DataFrame:
        try:
            schema = read_yaml(schema_file_path)
            data_frame = pd.read_csv(file_path, index_col="Unnamed: 0")
            error_message = ""

            for column in data_frame.columns:
                if column in list(schema.keys()):
                    data_frame[column].astype(schema[column])
                else:
                    error_message = (
                        f"{error_message} \ncolumn:[{column}] is not in the schema"
                    )
            if len(error_message) > 0:
                raise Exception(error_message)

            return data_frame
        except Exception as e:
            raise e

    def get_data_transformer(self) -> ColumnTransformer:
        try:
            schema_file_path = self.config.get_data_validation_config().schema_file_path
            dataset_schema = read_yaml(schema_file_path)
            numerical_columns = dataset_schema[NUMERICAL_COLUMN_KEY]
            categorical_columns = dataset_schema[CATEGORICAL_COLUMN_KEY]

            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaling", StandardScaler()),
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("encoding", OneHotEncoder()),
                    ("scaling", StandardScaler(with_mean=False)),
                ]
            )

            preprocessing = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns),
                ]
            )
            return preprocessing

        except Exception as e:
            raise e

    def transformed_data(self):
        try:
            train_file_path = self.data_ingestion_config.ingested_train_dir
            test_file_path = self.data_ingestion_config.ingested_test_dir
            schema_file_path = self.data_validation_config.schema_file_path
            logger.info("loading train and test data")
            train_df = DataTransformation.load_data(
                file_path=train_file_path, schema_file_path=schema_file_path
            )
            test_df = DataTransformation.load_data(
                file_path=test_file_path, schema_file_path=schema_file_path
            )
            logger.info("loaded train and test data successfull")

            schema = read_yaml(schema_file_path)
            target_column = schema[TARGET_COLUMN_KEY]
            logger.info("extracting target feature")
            target_feature_train_df = train_df[target_column]
            input_feature_train_df = train_df.drop(columns=target_column, axis=1)
            logger.info("extracting target feature done sucessfully")

            logger.info("extracting target feature from test data")
            target_feature_test_df = test_df[target_column]
            input_feature_test_df = test_df.drop(columns=target_column, axis=1)
            logger.info("extracting target feature from test data is done successfully")

            preprocessing_obj = self.get_data_transformer()
            logger.info("preprocessing obj generated successfully")
            input_feature_train_array = preprocessing_obj.fit_transform(
                input_feature_train_df
            )
            logger.info("train data transformed successfully")

            input_feature_test_array = preprocessing_obj.transform(
                input_feature_test_df
            )
            logger.info("test data transformed successfully")
            logger.info("train and test array concatination with target feature")
            train_array = np.c_[
                input_feature_train_array, np.array(target_feature_train_df)
            ]
            test_array = np.c_[
                input_feature_test_array, np.array(target_feature_test_df)
            ]
            logger.info(
                "train and test array concatination with target feature is done successfully"
            )

            transformed_train_file_path = (
                self.data_transformation_config.transformed_train_file_path
            )
            transformed_test_file_path = (
                self.data_transformation_config.transformed_test_file_path
            )

            train_dir, file_name = os.path.split(transformed_train_file_path)
            os.makedirs(train_dir, exist_ok=True)

            save_numpy_data(file_path=transformed_train_file_path, array=train_array)

            test_dir, file_name = os.path.split(transformed_test_file_path)
            os.makedirs(test_dir, exist_ok=True)

            save_numpy_data(file_path=transformed_test_file_path, array=test_array)
            preprocessing_obj_file_path = (
                self.data_transformation_config.preprocessing_file_path
            )

            save_object(file_path=preprocessing_obj_file_path, obj=preprocessing_obj)
            logger.info("data transformation completed")

        except Exception as e:
            raise e

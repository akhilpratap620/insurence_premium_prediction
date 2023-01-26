from collections import namedtuple

DataIngestionConfig=namedtuple("DataIngestionConfig", ["raw_data","data_ingestion_dir" , "ingested_train_dir" ,"ingested_test_dir"])
TrainingPipelineConfig=namedtuple("TrainingPipelineConfig", ["artifact_dir"])

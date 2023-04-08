from insurence_premium.entity.model_entity import ModelTrainerArtifact
import numpy as np
from insurence_premium.constant import *
from insurence_premium.entity.model_factory import evaluate_regression_model
from insurence_premium.entity.model_entity import ModelEvaluationArtifact
from insurence_premium.config import ConfigurationManager
from insurence_premium.util.common import load_data ,load_object ,read_yaml ,read_yaml_file
from insurence_premium import logger



class ModelEvalution:
    def __init__(self,config:ConfigurationManager() ,model_trainer_artifact:ModelTrainerArtifact):
        self.config=config
        self.model_evaluation_config=self.config.get_model_evaluation_config()
        self.model_trainer_config= self.config.get_model_trainer_config()
        self.model_validation=self.config.get_data_validation_config()
        self.model_ingestion=self.config.get_data_ingestion_config()
        self.model_trainer_artifact=model_trainer_artifact
    def get_best_model(self):
        try:
            
            model = None
            model_evaluation_file_path = self.model_evaluation_config.model_evaluation_file_path

            if not os.path.exists(model_evaluation_file_path):
                write_yaml_file(file_path=model_evaluation_file_path,
                                )
                return model
            model_eval_file_content=read_yaml_file(file_path=model_evaluation_file_path)
            logger.info(f"model_eval_file read successfully")

            eval_content=dict() if model_eval_file_content is None else model_eval_file_content

            if BEST_MODEL_KEY  not in eval_content:
                return model
            model=load_object(file_path=model_eval_file_content[BEST_MODEL_KEY][MODEL_PATH_KEY]) 
            return model
                
        except Exception as e:
            raise e

    def update_evaluation_report(self, model_evaluation_artifact: ModelEvaluationArtifact):
        try:
            eval_file_path = self.model_evaluation_config.model_evaluation_file_path
            model_eval_content = read_yaml_file(file_path=eval_file_path)
            model_eval_content = dict() if model_eval_content is None else model_eval_content
            
            
            previous_best_model = None
            if BEST_MODEL_KEY in model_eval_content:
                previous_best_model = model_eval_content[BEST_MODEL_KEY]

            logger.info(f"Previous eval result: {model_eval_content}")
            eval_result = {
                BEST_MODEL_KEY: {
                    MODEL_PATH_KEY: model_evaluation_artifact.evaluated_model_path,
                }
            }

            if previous_best_model is not None:
                model_history = {self.model_evaluation_config.time_stamp: previous_best_model}
                if HISTORY_KEY not in model_eval_content:
                    history = {HISTORY_KEY: model_history}
                    eval_result.update(history)
                else:
                    model_eval_content[HISTORY_KEY].update(model_history)

            model_eval_content.update(eval_result)
            logger.info(f"Updated eval result:{model_eval_content}")
            write_yaml_file(file_path=eval_file_path, data=model_eval_content)
        except Exception as e:
            raise e    


    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            trained_model_file_path = self.model_trainer_config.trained_model_file_path
            trained_model_object = load_object(file_path=trained_model_file_path)

            train_file_path = self.model_ingestion.ingested_train_dir
            test_file_path = self.model_ingestion.ingested_test_dir

            schema_file_path = self.model_validation.schema_file_path

            train_dataframe = load_data(file_path=train_file_path,
                                                           schema_file_path=schema_file_path,
                                                           )
            test_dataframe = load_data(file_path=test_file_path,
                                                          schema_file_path=schema_file_path,
                                                          )
            schema_content = read_yaml(path_to_yaml=schema_file_path)
            target_column_name = schema_content[TARGET_COLUMN_KEY]

            # target_column
            logger.info(f"Converting target column into numpy array.")
            train_target_arr = np.array(train_dataframe[target_column_name])
            test_target_arr = np.array(test_dataframe[target_column_name])
            logger.info(f"Conversion completed target column into numpy array.")

            # dropping target column from the dataframe
            logger.info(f"Dropping target column from the dataframe.")
            train_dataframe.drop(target_column_name, axis=1, inplace=True)
            test_dataframe.drop(target_column_name, axis=1, inplace=True)
            logger.info(f"Dropping target column from the dataframe completed.")

            model = self.get_best_model()

            if model is None:
                logger.info("Not found any existing model. Hence accepting trained model")
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_file_path,
                                                                    is_model_accepted=True)
                self.update_evaluation_report(model_evaluation_artifact)
                logger.info(f"Model accepted. Model eval artifact {model_evaluation_artifact} created")
                return model_evaluation_artifact

            model_list = [model, trained_model_object]

            metric_info_artifact = evaluate_regression_model(model_list=model_list,
                                                               x_train=train_dataframe,
                                                               y_train=train_target_arr,
                                                               x_test=test_dataframe,
                                                               y_test=test_target_arr,
                                                               base_accuracy=self.model_trainer_artifact.model_accuracy,
                                                               )
            logger.info(f"Model evaluation completed. model metric artifact: {metric_info_artifact}")

            if metric_info_artifact is None:
                response = ModelEvaluationArtifact(is_model_accepted=False,
                                                   evaluated_model_path=trained_model_file_path
                                                   )
                logger.info(response)
                return response

            if metric_info_artifact.index_number == 1:
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_file_path,
                                                                    is_model_accepted=True)
                self.update_evaluation_report(model_evaluation_artifact)
                logger.info(f"Model accepted. Model eval artifact {model_evaluation_artifact} created")

            else:
                logger.info("Trained model is no better than existing model hence not accepting trained model")
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_file_path,
                                                                    is_model_accepted=False)
            return model_evaluation_artifact

            logger.info(f"model evaluated artifact: {model_evaluation_artifact}")
        except Exception as e:
            raise e

    def __del__(self):
        logger.info(f"{'=' * 20}Model Evaluation log completed.{'=' * 20} ")        
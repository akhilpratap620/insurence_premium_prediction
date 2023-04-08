from insurence_premium.config import ConfigurationManager
from insurence_premium.entity.model_entity import MetricInfoArtifact ,BestModel,GridSearchedBestModel,InitialisedModelDetail
from insurence_premium.util import save_object ,load_numpy_array_data ,load_object
from insurence_premium import logger
from insurence_premium.entity.model_factory import ModelFactory ,evaluate_regression_model
from insurence_premium.entity.model_entity import ModelTrainerArtifact



class EstimatorModel:
    def __init__(self, preprocessing_object, trained_model_object):
        """
        TrainedModel constructor
        preprocessing_object: preprocessing_object
        trained_model_object: trained_model_object
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, X):
        """
        function accepts raw inputs and then transformed raw input using preprocessing_object
        which gurantees that the inputs are in the same format as the training data
        At last it perform prediction on transformed features
        """
        transformed_feature = self.preprocessing_object.transform(X)
        return self.trained_model_object.predict(transformed_feature)

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"


        

class ModelTrainer:
    def __init__(self, config: ConfigurationManager):
        self.config = ConfigurationManager()
        self.data_trainer_config = self.config.get_model_trainer_config()
        self.data_transformation_config = self.config.get_data_transformation_config()

    def get_trained_model(self):
        try:
            logger.info("loading training and testing data sets")
            train_file_path = self.data_transformation_config.transformed_train_file_path
            test_file_path = self.data_transformation_config.transformed_test_file_path

            train_data = load_numpy_array_data(file_path=train_file_path)
            test_data = load_numpy_array_data(file_path=test_file_path)
            x_train, y_train = train_data[:, :-1], train_data[:, -1]
            x_test, y_test = test_data[:, :-1], test_data[:, -1]
            logger.info("train and test data generated for data training")

            model_config_file_path = self.data_trainer_config.model_config_file_path
            logger.info("initializing model by using config filepath")

            model_factory = ModelFactory(config_file_path=model_config_file_path)

            base_accuracy = 0.6
            logger.info(f"expected accuracy:{base_accuracy}")

            best_model = model_factory.get_best_model(x=x_train,y=y_train,base_accuracy=base_accuracy)
            
            logger.info(f"Best model found on training dataset: {best_model}")
            
            logger.info(f"Extracting trained model list.")
            grid_searched_best_model_list:List[GridSearchedBestModel]=model_factory.grid_searched_best_model_list

            model_list = [model.best_model for model in grid_searched_best_model_list ]
            logger.info(f"Evaluation all trained model on training and testing dataset both")
            metric_info:MetricInfoArtifact = evaluate_regression_model(model_list=model_list,x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,base_accuracy=base_accuracy)

            logger.info(f"Best found model on both training and testing dataset.")
            preprocessing_obj=  load_object(file_path=self.data_transformation_config.preprocessing_file_path)
            model_object = metric_info.model_object


            trained_model_file_path=self.data_trainer_config.trained_model_file_path
            predictive_model = EstimatorModel(preprocessing_object=preprocessing_obj,trained_model_object=model_object)
            logger.info(f"Saving model at path: {trained_model_file_path}")
            save_object(file_path=trained_model_file_path,obj=predictive_model)
            logger.info(f"Saving model at path: {trained_model_file_path} is successfully done")

            model_trainer_artifact=  ModelTrainerArtifact(is_trained=True,message="Model Trained successfully",
            trained_model_file_path=trained_model_file_path,
            train_rmse=metric_info.train_rmse,
            test_rmse=metric_info.test_rmse,
            train_accuracy=metric_info.train_accuracy,
            test_accuracy=metric_info.test_accuracy,
            model_accuracy=metric_info.model_accuracy
            
            )
            return model_trainer_artifact

            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact





        except Exception as e:
            raise e

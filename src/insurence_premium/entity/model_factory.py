from insurence_premium.constant import *
from cmath import log
import importlib
from pyexpat import model
import numpy as np
import yaml
from typing import List
from insurence_premium import logger
from sklearn.metrics import r2_score,mean_squared_error
from insurence_premium.entity.model_entity import * 



def evaluate_regression_model(model_list: list, x_train:np.ndarray, y_train:np.ndarray, x_test:np.ndarray, y_test:np.ndarray, base_accuracy:float=0.6) -> MetricInfoArtifact:
    """
    Description:
    This function compare multiple regression model return best model
    Params:
    model_list: List of model
    X_train: Training dataset input feature
    y_train: Training dataset target feature
    X_test: Testing dataset input feature
    y_test: Testing dataset input feature
    return
    It retured a named tuple
    
    MetricInfoArtifact = namedtuple("MetricInfo",
                                ["model_name", "model_object", "train_rmse", "test_rmse", "train_accuracy",
                                 "test_accuracy", "model_accuracy", "index_number"])
    """
    try:
        
    
        index_number = 0
        metric_info_artifact = None
        for model in model_list:
            model_name = str(model)  #getting model name based on model object
            logger.info(f"{'>>'*30}Started evaluating model: [{type(model).__name__}] {'<<'*30}")
            
            #Getting prediction for training and testing dataset
            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)

            #Calculating r squared score on training and testing dataset
            train_acc = r2_score(y_train, y_train_pred)
            test_acc = r2_score(y_test, y_test_pred)
            
            #Calculating mean squared error on training and testing dataset
            train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
            test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))

            # Calculating harmonic mean of train_accuracy and test_accuracy
            model_accuracy = (2 * (train_acc * test_acc)) / (train_acc + test_acc)
            diff_test_train_acc = abs(test_acc - train_acc)
            
            #logging all important metric
            logger.info(f"{'>>'*30} Score {'<<'*30}")
            logger.info(f"Train Score\t\t Test Score\t\t Average Score")
            logger.info(f"{train_acc}\t\t {test_acc}\t\t{model_accuracy}")

            logger.info(f"{'>>'*30} Loss {'<<'*30}")
            logger.info(f"Diff test train accuracy: [{diff_test_train_acc}].") 
            logger.info(f"Train root mean squared error: [{train_rmse}].")
            logger.info(f"Test root mean squared error: [{test_rmse}].")


            #if model accuracy is greater than base accuracy and train and test score is within certain thershold
            #we will accept that model as accepted model
            if model_accuracy >= base_accuracy and diff_test_train_acc < 0.05:
                base_accuracy = model_accuracy
                metric_info_artifact = MetricInfoArtifact(model_name=model_name,
                                                        model_object=model,
                                                        train_rmse=train_rmse,
                                                        test_rmse=test_rmse,
                                                        train_accuracy=train_acc,
                                                        test_accuracy=test_acc,
                                                        model_accuracy=model_accuracy,
                                                        index_number=index_number)

                logger.info(f"Acceptable model found {metric_info_artifact}. ")
            index_number += 1
        if metric_info_artifact is None:
            logger.info(f"No model found with higher accuracy than base accuracy")
        return metric_info_artifact
    except Exception as e:
        raise e



class ModelFactory:
    def __init__(self ,config_file_path:str):
        self.config=ModelFactory.read_params(config_file_path)
        self.grid_search_cv_module:str = self.config[GRID_SEARCH_KEY][MODULE_KEY]
        self.grid_search_cv_class:str = self.config[GRID_SEARCH_KEY][CLASS_KEY]
        self.grid_search_cv_property_data:dict = dict(self.config[GRID_SEARCH_KEY][PARAM_KEY])
        self.models_initialization_config: dict = dict(self.config[MODEL_SELECTION_KEY])
        self.initialised_model_list = None
        self.grid_searched_best_model_list = None

    @staticmethod
    def read_params(file_path:str):
        try:
            with open(file_path) as file_obj:
                config:dict =yaml.safe_load(file_obj)
            return config    

        except Exception as e:
            raise e   

    @staticmethod
    def update_property_for_class(instance_obj:object ,property_data:dict):
        try:
            if not isinstance(property_data ,dict):
                raise Exception("property_data required dict formate")
                print(proprty_data)
            for key ,value in property_data.items():
                setattr(instance_obj ,key ,value)
                logger.info(f"Executing:$ {str(instance_obj)}.{key}={value}")
            return instance_obj
        except Exception as e:
            raise e        

    @staticmethod
    def class_for_name(module_name:str ,class_name=str):
        try:
            module=importlib.import_module(module_name)
            logger.info(f"importing module:{module_name} with class:{class_name}")
            class_ref=getattr(module ,class_name)
            return class_ref

        except Exception as e:
            raise e

    def get_initialised_model_list(self)->List[InitialisedModelDetail]:
        try:
            initialised_model_list=[]
            for model_serial_number in self.models_initialization_config.keys():
                model_initialization_config =self.models_initialization_config[model_serial_number]
                model_obj_ref =ModelFactory.class_for_name(
                    model_initialization_config[MODULE_KEY] ,
                    model_initialization_config[CLASS_KEY])
                model=model_obj_ref()

                if PARAM_KEY in model_initialization_config:
                    model_property_data=dict(model_initialization_config[PARAM_KEY]) 
                    model=ModelFactory.update_property_for_class(instance_obj=model ,property_data=model_property_data)
                param_grid_search=model_initialization_config[SEARCH_PARAM_GRID_KEY]

                model_name=f"[{model_initialization_config[MODULE_KEY]}.{model_initialization_config[CLASS_KEY]}]"

                model_initialization_detail=InitialisedModelDetail(
                    model_serial_number=model_serial_number,
                    model=model,
                    param_grid_search=param_grid_search,
                    model_name=model_name,
                    
                )   

                initialised_model_list.append(model_initialization_detail)
            return initialised_model_list        
        except Exception as e:
            raise e
    
    def execute_grid_search_operation(self,

                                    initialised_model:InitialisedModelDetail ,
                                    input_feature ,output_feature)->GridSearchedBestModel:
        try:
            grid_search_cv_ref=ModelFactory.class_for_name(module_name=self.grid_search_cv_module ,class_name=self.grid_search_cv_class)
            grid_search_cv=grid_search_cv_ref(estimator=initialised_model.model ,param_grid=initialised_model.param_grid_search)
            grid_search_cv=ModelFactory.update_property_for_class(instance_obj=grid_search_cv ,property_data=self.grid_search_cv_property_data)
            grid_search_cv.fit(input_feature ,output_feature)

            message = f'{">>"* 30} f"Training {type(initialised_model.model).__name__}" completed {"<<"*30}'
            grid_searched_best_model = GridSearchedBestModel(model_serial_number=initialised_model.model_serial_number,
                                                             model=initialised_model.model,
                                                             best_model=grid_search_cv.best_estimator_,
                                                             best_parameters=grid_search_cv.best_params_,
                                                             best_score=grid_search_cv.best_score_
                                                             )
            
            return grid_searched_best_model
        
        except Exception as e:
            raise e                            
    
    def initiate_best_parameter_search_for_initialised_model(self, initialised_model: InitialisedModelDetail,
                                                             input_feature,
                                                             output_feature) -> GridSearchedBestModel:
        """
        initiate_best_model_parameter_search(): function will perform paramter search operation and
        it will return you the best optimistic  model with best paramter:
        estimator: Model object
        param_grid: dictionary of paramter to perform search operation
        input_feature: your all input features
        output_feature: Target/Dependent features
        ================================================================================
        return: Function will return a GridSearchOperation
        """
        try:
            return self.execute_grid_search_operation(initialised_model=initialised_model,
                                                      input_feature=input_feature,
                                                      output_feature=output_feature)
        except Exception as e:
            raise e
    def initiate_best_parameter_search_for_initialised_models(self,
                                                              initialised_model_list: List[InitialisedModelDetail],
                                                              input_feature,
                                                              output_feature) -> List[GridSearchedBestModel]:

        try:
            self.grid_searched_best_model_list = []
            for initialised_model_list in initialised_model_list:
                grid_searched_best_model = self.initiate_best_parameter_search_for_initialised_model(
                    initialised_model=initialised_model_list,
                    input_feature=input_feature,
                    output_feature=output_feature
                )
                self.grid_searched_best_model_list.append(grid_searched_best_model)
            return self.grid_searched_best_model_list
        except Exception as e:
            raise e
    @staticmethod
    def get_best_model_from_grid_searched_best_model_list(grid_searched_best_model_list:List[GridSearchedBestModel] ,base_accuracy=0.6)->BestModel:
        try:
            best_model=None
            for grid_search_best_model in grid_searched_best_model_list:
                if grid_search_best_model.best_score > base_accuracy:
                    logger.info("Acceptable model found:{grid_search_best_model}")
                    best_model=grid_search_best_model


            if not best_model:
                raise Exception("No better model has accuracy than base model")  
            logger.info(f"best model found:{best_model}")     
        except Exception as e:
            raise e                

    def get_best_model(self ,x,y,base_accuracy=0.6):
        try:
            initialised_model=self.get_initialised_model_list()
            grid_searched_best_model_list = self.initiate_best_parameter_search_for_initialised_models(
                initialised_model_list=initialised_model,
                input_feature=x,
                output_feature=y
            )
            return ModelFactory.get_best_model_from_grid_searched_best_model_list(grid_searched_best_model_list=grid_searched_best_model_list,base_accuracy=0.6)
        except Exception as e:
            raise e    
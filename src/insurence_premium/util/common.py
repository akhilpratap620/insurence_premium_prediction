import os
from box.exceptions import BoxValueError
from insurence_premium import logger
import json
import joblib
import yaml
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import numpy as np
import dill
import pandas as pd


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns
    Args:
        path_to_yaml (str): path like input
    Raises:
        ValueError: if yaml file is empty
        e: empty file
    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories
    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """save json data
    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """load json files data
    Args:
        path (Path): path to json file
    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    with open(path) as f:
        content = json.load(f)

    logger.info(f"json file loaded succesfully from: {path}")
    return ConfigBox(content)



@ensure_annotations
def save_bin(data: Any, path: Path):
    """save binary file
    Args:
        data (Any): data to be saved as binary
        path (Path): path to binary file
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """load binary data
    Args:
        path (Path): path to binary file
    Returns:
        Any: object stored in the file
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data


@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB
    Args:
        path (Path): path of the file
    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"

def save_numpy_data(file_path:str ,array:np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path ,exist_ok=True)
        with open(file_path ,'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise e        



def load_numpy_array_data(file_path:str)->np.array:
    try:
        with open(file_path ,'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise e

def save_object(file_path:str, obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path ,'wb') as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise e

def load_object(file_path:str):
    try:
        with open(file_path,'rb') as obj:
            obj=dill.load(obj)
            return obj
    except Exception as e:
        raise e


            

def write_yaml_file(file_path:str,data:dict=None):
    """
    Create yaml file 
    file_path: str
    data: dict
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,"w") as yaml_file:
            if data is not None:
                yaml.dump(data,yaml_file)
    except Exception as e:
        raise e    


def load_data(file_path:str ,schema_file_path:str)->pd.DataFrame:
        try:
            schema=read_yaml(schema_file_path)
            data_frame=pd.read_csv(file_path,index_col='Unnamed: 0')
            error_message =''

            for column in data_frame.columns:
                if column in list(schema.keys()):
                    data_frame[column].astype(schema[column])
                else:
                    error_message=f"{error_message} \ncolumn:[{column}] is not in the schema"    
            if len(error_message)>0:
                raise Exception(error_message)
            
            return data_frame      
        except Exception as e:
            raise e

def read_yaml_file(file_path:str):
    try:
        with open(file_path ,'r') as f:
            response =yaml.safe_load(f)
            return response

    except Exception as e:
        raise e

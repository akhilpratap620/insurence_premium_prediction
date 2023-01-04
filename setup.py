from setuptools import setup , find_packages
from typing import List

PROJECT_NAME="Insurence_Premium"
VERSION="1.0.0"
AUTHOR="Akhil pratap singh"
DESCRIPTION="this is insurence premium prediction it will help to know insurence status"
REQUIREMENTS_FILE_NAME ="requirements.txt"
HYPHEN_E_DOT="-e ."

def get_requirmenents_list()->List[str]:
    with open(REQUIREMENTS_FILE_NAME) as requiremenets_file:
        requirement_list=requiremenets_file.readlines()
        requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]
        if HYPHEN_E_DOT in requirement_list:
            requirement_list.remove(HYPHEN_E_DOT)
        return requirement_list

setup(
name=PROJECT_NAME,
version=VERSION,
author=AUTHOR,
description=DESCRIPTION ,
packages=find_packages(), 
install_requires=get_requirmenents_list()
)


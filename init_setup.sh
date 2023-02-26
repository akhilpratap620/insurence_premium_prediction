echo [$(date)]:"start"
echo [$(date)]:"creating env with python 3.7 version"
conda create --prefix ./env python=3.7 -y
echo [$(date)]:"actiavting the envirements"
source actiavte ./env
echo [$(date)]:"install all the requirements.txt"
pip install -r requirements_dev.txt
echo [$(date)]:"completed"

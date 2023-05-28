
# Project 
# insurence premium prediction



## Acknowledgements

 - create vertual enviroment and install requirements.txt -[ pip install -r requirements.txt]
 - run app.py 
   


## Authors

- [@sakhilpratap620](https://www.github.com/sakhilpratap620)



## Deployment

This project is deployed in aws and link is

```bash
  1."https://ec2-3-110-121-180.ap-south-1.compute.amazonaws.com"
  2.'https://3.110.121.180:8080"
```
```bash
this link is will be closed because of charges
```
## deployment process
```bash
1.we will use github action for deployment process
2.we use ecr repo and ec2 instance running process
3. for this we use runner option for continuous deployment
4. we have to use some commands for adding runner
#optinal

1.sudo apt-get update -y

2.sudo apt-get upgrade

#required

3.curl -fsSL https://get.docker.com -o get-docker.sh

4.sudo sh get-docker.sh

5.sudo usermod -aG docker ubuntu

6.newgrp docker
```
## Configure EC2 as self-hosted runner
```bash
setup some github secrets
1.AWS_ACCESS_KEY_ID=

2.AWS_SECRET_ACCESS_KEY=

3.AWS_REGION = us-east-1

4.AWS_ECR_LOGIN_URI = demo>> 566373416292.dkr.ecr.ap-south-1.amazonaws.com

5.ECR_REPOSITORY_NAME = 
```
## after successfully adding runner interface will look like this

![added runner for continue deployment](https://github.com/akhilpratap620/ipynb_renderer_pack/assets/95284349/5646d098-bb40-44e0-aa0c-ef90319b4858)

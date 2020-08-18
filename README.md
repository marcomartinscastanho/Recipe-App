# Recipe App Api

Recipe App API source code

## Contents

[[_TOC_]]

## Docker
### Dockerfile
The Dockerfile is a text file that contains all commands, in order, needed to build a given image. It adheres to a specific format and set of instructions which you can find at [Dockerfile reference](https://docs.docker.com/engine/reference/builder/).  
A valid Dockerfile must start with a ```FROM``` instruction. The ```FROM``` instruction initializes a new build stage and sets the Base Image for subsequent instructions. You can find many available Base Images in the [Docker Hub](https://hub.docker.com).  
For this project, we use **Python 3.8 alpine** image.  

Check the comments in the Dockerfile of this project for more detail on each instruction.  

Check also the [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#from) for more info.

### Python Packages
In order to install Python packages needed for each specific project, specify them in a ```requirements.txt``` file that can then be copied to the docker image and used to install the packages with pip.  
For this project, we are using Django 3.0 and djangorestframework 3.11.  
You can Python packages and their version history at [The Python Package Index](https://pypi.org/). 

### Build Image
In order to build the Docker Image, run ```docker build .``` inside the project folder.  
What this does is saying "build whatever Dockerfile is in the root of the project".

#### Certificate Verification Error
If you encounter a ```SSL: CERTIFICATE_VERIFY_FAILED``` error when building the Docker image, check [this workaround](https://stackoverflow.com/a/56131678/1971089) that fixes it.

### Docker Compose
Docker Compose is a tool that allows to run the docker image easily from the project location.
It allows to easily manage the different services that make out the project (e.g. the python applications, the database, etc).

#### Docker Compose file
Docker Compose is ```.yml``` file that contains the configuration for all of the that make out the project.  
Check the comments inside the file for more details.  
After filling the ```docker-compose.yml``` file run ```docker-compose build``` to build the image using the docker-compose configuration.

### Create Django project
After setting the Docker Compose configuration, we can use it to run commands on the docker image.
Therefore we can use it to run commands to create a Django project inside the container.  
Run ```docker-compose run <service> sh -c "<command>"``` where ```<service>``` is the name of the service where we want ot run the command on,
given that the service is on the ```docker-compose.yml``` file, and ```<command>``` is the command you want to run in the service.

In this case, we run ```docker-compose run app sh -c "django-admin startproject app ."```.  
This runs the ```django-admin``` script to start a project called ```app``` and to start the project on the current location.

## Continuous Integration (CI)
In order to have Continuous Integration on the project, create a ```.gitlab-ci.yml``` file in the root of the project.  
The GitLab CI configuration file tells GitLab what to do everytime we push a change in the project.  

For more information check the [GitLab CI/CD pipeline configuration reference](https://docs.gitlab.com/ee/ci/yaml/).

## Flake8
Flake8 is a Python linting tool which verifies pep8, pyflakes and circular complexity.

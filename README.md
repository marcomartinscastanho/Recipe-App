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
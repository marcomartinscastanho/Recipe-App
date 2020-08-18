# Go to https://hub.docker.com/ for images to start your containers from
# We'll start with a Python 3.8 image
FROM python:3.8-alpine

# next line is the maintainer line: who maintains this Docker image
MAINTAINER ALTEN DCX Sophia Antipolis

# ENV for defining Environment Variables
ENV PYTHONUNBUFFERED 1
# Tells Python to run in Unbuffered Mode, which is recommended when running Python within Docker containers.
# Why? It doesn't allow Python to buffer the outputs, it just prints them directly, which avoids complications with Docker.

# copy the requirements file from the current location to the home directory of the Python image
COPY ./requirements.txt /requirements.txt

# install into the docker image all requirements in the requirements file
# RUN pip install -r /requirements.txt
# PS: all the tags in this command were added to ingore a certificate issue
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --no-cache-dir -r /requirements.txt

# create a directory inside the docker image where we'll store the source code
RUN mkdir /app
# makes that directory the default directory, so any app we'll run in the docker image, will run starting from this directory
WORKDIR /app
# copy the app folder from local to the docker image
COPY ./app /app

# create a user called "user" that will run the app using docker
# -D means this user only runs applications, he doesn't have a home directory
RUN adduser -D user
# switch to that user
USER user
# why? Security reasons. If we don't do this, the image will run the application using the root account,
# which is not recomended because, if someone compromises the application, they can then have root access to the whole image
# and they can do other malicions things
# creatring a user limits the scope an attacker would have within the docker container

# Recipe App Api

Recipe App API source code

# Contents

[[_TOC_]]

# Docker
## Dockerfile
The Dockerfile is a text file that contains all commands, in order, needed to build a given image. It adheres to a specific format and set of instructions which you can find at [Dockerfile reference](https://docs.docker.com/engine/reference/builder/).  
A valid Dockerfile must start with a ```FROM``` instruction. The ```FROM``` instruction initializes a new build stage and sets the Base Image for subsequent instructions. You can find many available Base Images in the [Docker Hub](https://hub.docker.com).  
For this project, we use **Python 3.8 alpine** image.  

Check the comments in the Dockerfile of this project for more detail on each instruction.  

Check also the [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#from) for more info.

## Python Packages
In order to install Python packages needed for each specific project, specify them in a ```requirements.txt``` file that can then be copied to the docker image and used to install the packages with pip.  
For this project, we are using Django 3.0 and djangorestframework 3.11.  
You can Python packages and their version history at [The Python Package Index](https://pypi.org/). 

## Build Image
In order to build the Docker Image, run ```docker build .``` inside the project folder.  
What this does is saying "build whatever Dockerfile is in the root of the project".

### Certificate Verification Error
If you encounter a ```SSL: CERTIFICATE_VERIFY_FAILED``` error when building the Docker image, check [this workaround](https://stackoverflow.com/a/56131678/1971089) that ignores SSL errors.

## Docker Compose
Docker Compose is a tool that allows to run the docker image easily from the project location.
It allows to easily manage the different services that make out the project (e.g. the python applications, the database, etc).

### Docker Compose file
Docker Compose is ```.yml``` file that contains the configuration for all of the that make out the project.  
Check the comments inside the file for more details.  
After filling the ```docker-compose.yml``` file run ```docker-compose build``` to build the image using the docker-compose configuration.

## Create Django project
After setting the Docker Compose configuration, we can use it to run commands on the docker image.
Therefore we can use it to run commands to create a Django project inside the container.  
Run ```docker-compose run --rm <service> sh -c "<command>"``` where ```<service>``` is the name of the service where we want ot run the command on,
given that the service is on the ```docker-compose.yml``` file, and ```<command>``` is the command you want to run in the service.  
What this does is run the service ```<service>``` to open a shell (hence the ```sh```) and run the command (hence the ```-c```) ```<command>```.  
The ```--rm``` removes the container after it has ran the command.
You can add this option on commands that you just want to run once and you don't want the docker container to linger on the system after it's run.

In this case, we run ```docker-compose run --rm app sh -c "django-admin startproject app ."```.  
This runs the ```django-admin``` script to start a project called ```app``` and to start the project on the current location.

# Continuous Integration (CI)
In order to have Continuous Integration on the project, create a ```.gitlab-ci.yml``` file in the root of the project.  
The GitLab CI configuration file tells GitLab what to do everytime we push a change in the project.  

For more information check the [GitLab CI/CD pipeline configuration reference](https://docs.gitlab.com/ee/ci/yaml/).

# Flake8
Flake8 is a Python linting tool which verifies pep8, pyflakes and circular complexity.

# Testing
## Test-Driven Development (TDD)
Test-Driven Development is simply writing the test before writing the code, assure the test is failing, and then writing the code to make the test pass.  
One of the benefits is that you know the tests work.
There's often cases in which you write unit test that you think is testing something, but it really isn't.
For example, if you forget to add the ```test``` prefix in the function name, the test is never being picked up by the test runner, and therefore it seems like everything is working fine but in reality the test is just not running.
So TDD helps eliminate false positives.  
Also it helps improve the way you think about code, because before you write the code, you think that you need to write code that we can test.
This means that you have to write testable code, which usually good quality code, easy to test and easy to maintain.

## Mocking
Mocking is when you override or change the behaviour of the dependencies of the code that you're testing.  
Mocking is used to avoid any unintended side-effects and also to isolate specific pieces of code that we want to test.  
For example, when testing a function that sends an email, there are 2 good reasons why you don't actually want to send an email everytime you run the test:
- You should never write tests that depend on external services.  
This is because you cen never guarantee that these services will be available at the point when you run the tests.  
This would make the tests unpredictable and unreliable.
- You don't want to be sending spam emails everytime the test is ran.  
Even if using a fake address, those emails would still be clogging up some server somewhere.

When you write the test, you can use Mocking to avoid sending an actual email.
You could override the function in the dependency that sends the email, and replace it with a mock object.
Using this mock object, you can avoid sending an actual email and instead just check that the function was called with the correct parameters. 

## Testing Manually on Browser
After fully configuring the Database (i.e. after commit [cd4b20bf](https://gitlab.altengroup.net/ska/knowledge-base/python/django/recipe-app-api/-/commit/cd4b20bf4e4caee9a36ed6be6649b727db2e6de1)) we can test the app manually on the browser.  
For that, we must first start the server by running ```docker-compose up```.
This will start the services in the docker-compose file, perform the commands in the command section of each service.
In this example, it will begin by starting the db service (since the app service has a dependency on db) and then start the app service.
When starting the app service, it will run the commands in the command section of the app service, i.e. wait for the db to be ready, apply all existing migrations to the db and run the server on the specified host and port.      
Once the server is running, go to a browser and type ```localhost:8000/admin``` to get the admin portal.
This will show the admin portal login page.
If you haven't created an admin user, you need one.

### Creating superuser
In order to keep the server running on the terminal, open a new terminal, run ```docker-compose run --rm app sh -c "python manage.py createsuperuser"``` and follow the instructions.

# Manage User Endpoints
The Manage User endpoints allow us to create users, update them, change their password and to create authentication tokens,
which can be used to authenticate requests to the other APIs in the projects.  
We create these endpoints in a ```users``` app in the Django project.

Run ```docker-compose run --rm app sh -c "python manage.py startapp user"``` to create a new app called user inside the Django project.  
Once the app users is created, we can do some cleaning, removing files created by default that we're not gonna use since we're probably using them from the ```core``` app.  
Remove the migrations folder, admin.py and modules.py, since we're using the ones in the core app, and tests.py since we're creating a sub-folder for tests.

## Create Token Endpoint
The Create Token endpoint is an endpoint which is used to make HTTP POST requests to generate temporary **auth tokens** that can then be used to authenticate future requests with the API.  
This means that the API uses token authentication, i.e. the way to login is to use this endpoint to generate a token, and then provide that token as the authentication header for future requests that require authentication.  
The benefit of this is not needing to send the user's username and password in every single request made to the API. They're only sent once to create the token and then the token is used for further requests.
Also, if we want to revoke that token, we can do that in the database.          

## Manage User Endpoint
The Manage User endpoint allows the authenticated users to update their own profile.
This includes changing their name and password, and also seeing their user object, so they can see what all the values are currently set to.

### Test Manually on the browser  
In order to test manually on the browser having access to a private endpoint you first need to create a user and obtain an authentication token.  
- To create a user head over to ```http://localhost:8000/api/user/create``` and follow the procedure.
- To obtain an authentication token, head over to ```http://localhost:8000/api/user/token``` and fill in the user information.

Then, in order to access a private endpoint using the authentication token obtained, you need a way to modify the headers in the request.
Browsers don't typically provide this feature by default, but adding some plug-ins or extensions will do it.  
Add a request header called ```Authorization``` with value ```Token <the_token_obtained>``` and then head over to ```http://localhost:8000/api/user/me```.  
You should see the user that is authenticated in the API, and have the fields to update the user's details. 

When updating the user's details, the endpoint provides 2 different methods:
- PUT - replace the entire resource on the db with the one we are sending now.  
This means that you need to provide all the mandatory fields;
- PATCH - only update the fields that we are specifying in the request;

# Recipe API
All Recipe related endpoints are stored in a new app called ```recipe```.  
Examples of such endpoints are endpoints for creating and updating recipes, tags and ingredients.
## Tags Endpoint
The Tags API allows to manage tags that can be assigned to recipes in order to help with sorting and filtering recipes in the system.

## Ingredients Endpoint
The Ingredients endpoint is very similar to the Tags endpoint, in that it allows to create and list ingredients which we can later assign to recipes for the purpose of filtering.  

## Recipes Endpoint
### Recipe List
The Recipe List Endpoint endpoint returns a summary of all the recipes the user has.  

### Recipe Detail
The Recipe List Endpoint endpoint returns all the details of a specific recipe.  
The big difference is that the Recipe List endpoint returns only the ids of the ingredients and tags for each recipe, and the Recipe Detail returns the actual Ingredients and Tags names for the specified recipe.  
This gives the client (e.g. front-end application) to have more flexibility on the ammount of data it receives when they get the recipe list.
The reason for this, is that if you get all the information from each recipe when you just want to list them, the operation may get slow if each recipe has a lot of information (large list of ingredients, photo, etc.).

### Image upload
This endpoint allows to upload images to go along with Recipes.  
In order to do that, an image field must be added to the Recipe model.  

Additionally, in order to use the ImageField in Django, we need to install the Pillow python package, which is used for manipulating images which are uploaded in python.  

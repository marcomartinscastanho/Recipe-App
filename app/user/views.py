from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    # all we need to specify a class variable that points to the serializer we want to use to create the user
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer

    # set the renderer class
    # sets the renderer so we can view this endpoint in the browser, with the browsable api
    # this means we can login in the browser, type username and password, click POST
    # and it should return a token
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    # we are the default renderer classes from api settings, so that
    # if we want to change the renderer class, we can just change them in the settings
    # and it will update in the view automatically

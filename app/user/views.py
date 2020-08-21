from rest_framework import generics, authentication, permissions
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


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer

    # authentication is the mechanism by which the authentication happens
    # can be cookie authentication, token authentication, etc
    authentication_classes = (authentication.TokenAuthentication, )

    # permissions are the level of access that the user has
    # the only permission level we have is that the user must be authenticated to use the app
    # no other levels or special permissions
    permission_classes = (permissions.IsAuthenticated, )

    # we need a get object function in the api view
    # typically what would happen with an api view is that
    # you would link it to a model and it would retrieve database models
    # in this case we're gonna just get the model for the logged in user
    # because we just want to return the user that is authenticated
    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user

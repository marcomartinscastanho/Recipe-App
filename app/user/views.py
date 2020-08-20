from rest_framework import generics
from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    # all we need to specify a class variable that points to the serializer we want to use to create the user
    serializer_class = UserSerializer

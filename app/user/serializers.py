from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        # the fields that are included in the serializer
        # i.e. the fields that are  converted to and from json when we make the HTTP post,
        # and then we retrieve them in the view, and then we save them in the model
        # so basically are the fields we want to make accessible in the API, either to read or write
        fields = ('email', 'password', 'name')

        # define extra rules for some fields
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # overridden from serializers.ModelSerializer
    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""

        # what django rest_framework does is
        # when we're ready to create the user it'll call this create function and it will pass in the validated_data
        # the validated_data will contain all the data that was passed into our serializer
        # which will be the json data that was made in the HTTP POST
        # and we can use it to create the user
        return get_user_model().objects.create_user(**validated_data)

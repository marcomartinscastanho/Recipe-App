from django.contrib.auth import get_user_model, authenticate
# use this whenever you are outputting any message to the user
# it's a good idea to pass them through this translation package to provide support easily for more languages
from django.utils.translation import ugettext_lazy as _
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


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""

    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        # by default django trims leading or trailing whitespaces
        # that would change the password set by the user, therefore we have to force it not to happen
        trim_whitespace=False
    )

    # overridden from the django rest_framework
    # is called automatically when we validate this serializer
    def validate(self, attrs):
        """Validate and authenticate the user"""
        # every field that makes up the serializer (email and password)
        # will be passed to the validate function as fields in the attrs dictionary
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            # the AuthTokenSerializer will be passed in the views
            # and when a request is made, the views pass the request to the serialized inside the context
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            message = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(message, code='authentication')

        attrs['user'] = user
        return attrs

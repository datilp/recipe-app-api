from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _  # Whenever we output
#   a message to the screen by using this we can easily trnasform it to be in
#   another language

from rest_framework import serializers


# by using the rest_framework serializer ModelSerializer we get a build in
# functionality to send objects and read objects from the database.
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        # the class/model this serializer is based on
        model = get_user_model()
        # fields converted to and from json when we do our http request
        # fields we want to make available to the API
        fields = ('email', 'password', 'name')
        # allows to configure extra settings in our model serializer
        # in this case we make it to ensure the password:
        #  .- has the correct length
        #  .- can it is write only can not be read
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # we rest_framework specify the functions you can override, create is
    # one of them. We override
    def create(self, validated_data):
        """Create a new user with encrypted password and returns the user"""
        # we want to use our model create user as it will make sure the
        # password is encrypted
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()  # make sure it is character field
    password = serializers.CharField(  # no trimming and type is password
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        # in the validation we need to return the attributes back with the
        # user in it
        attrs['user'] = user
        return attrs

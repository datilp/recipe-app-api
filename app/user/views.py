from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


# this view will interact with the database back and forth
# for a given web request/response

# by using the generic CreateAPIView we use a bunch of functionality
# to deal with db interaction
# This view is based on the UserSerializer so it knows what DB object
# and fields it is using
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for the user"""
    serializer_class = AuthTokenSerializer
    # sets the renderer so we can use the this view in the HTML/browser
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

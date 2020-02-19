from rest_framework import generics, authentication, permissions
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


# note we are basing this on the RetrieveUpdateAPIView which already provides
# a bunch of functionality
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer  # serializer class attribute
    # the authentication class type is going to be token base
    authentication_classes = (authentication.TokenAuthentication,)
    # the permissions are going to be just that it is authenticated
    permission_classes = (permissions.IsAuthenticated,)

    # with a view since it is linked to a model it will return the database
    # object corresponding to that model.
    # In this case we just want to return the user, so we override the
    # get_object method to do just that.
    def get_object(self):
        """Retrieve and return authentication user"""
        # the authentication_classes will make sure to attach to the request
        # the authenticated user. It is done automatically.
        return self.request.user

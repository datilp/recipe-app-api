from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse  # generates API URL

from rest_framework.test import APIClient  # test client
from rest_framework import status  # module containing status codes in
#     humanreadible strings


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')  # URL we are going to use to make the
#   the API user token request


# helper function use in other test methods below
# **params is a dynamic list of arguments we can pass directly
# to our create_user model function.
#
def create_user(**params):
    """Helper function to create new user"""
    return get_user_model().objects.create_user(**params)


# we create two APIs one called public and the other called private
# The public one will not be authenticated yet, like create user
# The private one will be authenticated already and will allow things
# like modify user details
class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating a user with a valid payload is successful"""
        # The payload is the object we pass to the API
        payload = {
            'email': 'isuarezsolatest@gmail.com',
            'password': 'testpass',
            'name': 'name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # The response should return the user object in the data
        user = get_user_model().objects.get(**res.data)
        # we can check if this is the user by checking if the password
        # is correct
        self.assertTrue(
            user.check_password(payload['password'])
        )
        # We want to make sure 'password' is not return on the user object
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {'email': 'isolasuarezsolatest@gmail.com',
                   'password': 'testpass'}
        # we use the helper function created above to create the user
        # note the user is created first via the model using the helper
        # function and then we try to create it again using the API.
        # Each test is unique, meaning users created in the above test method
        # wont appear in the system when this method runs.
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 5 characters"""
        payload = {'email': 'test@londonappdev.com', 'password': 'pw'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # note
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'isuarezsolatest@gmail.com',
                   'password': 'testpass'}
        create_user(**payload)  # we create the user first
        #   and then we create a token for that user
        res = self.client.post(TOKEN_URL, payload)

        # let check that the data return contains a token
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        # create a user first using the model
        create_user(email='isuaresolatest@gmail.com', password='testpass')
        # while passing a payload to the API with the wrong password
        payload = {'email': 'isuarezsolatest@gmail.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doens't exist"""
        # note that here we are not creating the user prehand
        payload = {'email': 'isuarezsolatest@gmail.com',
                   'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        # very similar to invalid credentials just that one field is empty
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

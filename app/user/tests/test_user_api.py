from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


# reverse creates the user:create url and assigns it to the variable
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


# helper function, since we'll be creating users quite often in the tests
def create_user(**params):
    return get_user_model().objects.create_user(**params)


# Public because it's good to separate the API tests into public and private tests
# This keeps the code clean because then in the setUp you can have one that authenticates and one that doesn't
# Public API - non authenticated - anyone can make a request
#   e.g. create_user: when you create a user is usually because you don't have an account yet, so you don't have auth
# Private API - authenticated - only authenticated users can make a request
#   e.g. change_pass: only authenticated users should be able to do this
class PublicUserApiTests(TestCase):
    """Tests the users API (public)"""

    def setUp(self):
        # set an API client reusable for all tests
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@fake.com',
            'password': 'fake-123',
            'name': 'Test McTestington'
        }

        response = self.client.post(CREATE_USER_URL, payload)
        # the created user is expected to be returned in the payload of the response

        # assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test that the object is actually created
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        # test the password is not returned in the response
        self.assertNotIn('password', response.data)

    def test_user_exists(self):
        """Tests creating a user that already exists fails"""
        payload = {
            'email': 'test@fake.com',
            'password': 'fake-123',
            'name': 'Test McTestington'
        }
        # we create the user calling the function directly
        create_user(**payload)

        # then we try to create it again through the API
        response = self.client.post(CREATE_USER_URL, payload)

        # assertions
        # that user already exists
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'test@fake.com',
            'password': 'fake',
            'name': 'Test McTestington'
        }

        response = self.client.post(CREATE_USER_URL, payload)

        # assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # make sure the user was not created
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        )
        self.assertFalse(user_exists)

    # we don't need to have authentication in the create tokens API,
    # given that the purpose of the API is to start the authentication
    # hence the create tokens endpoint is public, so we can add the tests for it under this class

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {
            'email': 'test@fake.com',
            'password': 'fake-123'
        }
        # we create the user calling the function directly
        create_user(**payload)

        # and then we try to obtain an authentication token for this user,
        # in order to use it in future requests that need authentication
        response = self.client.post(TOKEN_URL, payload)

        # assertion
        self.assertIn('token', response.data)
        # we only need to assert that the token is returned
        # no need to assert that the token works, since it is obtained from the built-in django authentication system
        # which is already extensively tested, so no need to test the tokens further
        # don't overtest

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""

        # we create the user calling the function directly
        create_user(email='test@fake.com', password='fake-123')

        payload = {
            'email': 'test@fake.com',
            'password': 'wr0ng-p@55w0rd'
        }
        response = self.client.post(TOKEN_URL, payload)

        # assertions
        # since we provided a wrong password for this user when requesting the authentication token,
        # we expect that the token was not provided
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {
            'email': 'test@fake.com',
            'password': 'fake-123'
        }
        # we don't create the user this time!
        # db is reset between each test, so the previously run tests have no effect on this one

        response = self.client.post(TOKEN_URL, payload)

        # assertions
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""

        response = self.client.post(TOKEN_URL, {'email': 'test@fake.com', 'password': ''})

        # assertions
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # even though this test tests a private endpoint (one that needs authentication)
    # we are testing a case in which a non-authenticated user is trying to access it
    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""

        response = self.client.post(ME_URL)

        # assertions
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# Private means that authentication is required before using these endpoints
class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@fake.com',
            password='fake-123',
            name='Test McTestington'
        )
        self.client = APIClient()
        # force_authenticate is a helper function that makes it easy to simulate authenticated requests
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""

        # we don't need to create or authenticate the user, since that was done already in the setUp
        response = self.client.get(ME_URL)

        # assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """Test that POST is note allowed on the me url"""

        response = self.client.post(ME_URL, {})

        # assertions
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {
            'name': 'Fake McFakington',
            'password': 'fake-456'
        }

        response = self.client.patch(ME_URL, payload)

        # update the user object with the latest values from the db
        self.user.refresh_from_db()

        # assertions
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

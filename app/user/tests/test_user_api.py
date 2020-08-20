from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


# reverse creates the user:create url and assigns it to the variable
CREATE_USER_URL = reverse('user:create')


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
        create_user(**payload)

        response = self.client.post(CREATE_USER_URL, payload)

        # assertions
        # that user already exists
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'test@fake.com',
            'password': 'fake'
        }

        response = self.client.post(CREATE_USER_URL, payload)

        # assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # make sure the user was not created
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        )
        self.assertFalse(user_exists)

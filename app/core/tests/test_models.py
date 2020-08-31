from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test"fake.com', password='test-123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an e-mail is successful"""

        email = 'test@fake.com'
        password = "test-123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        # assertions
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""

        email = 'test@FAKE.COM'
        user = get_user_model().objects.create_user(email, 'test-123')

        # assertions
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""

        # assertions
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test-123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""

        user = get_user_model().objects.create_superuser(
            'test@fake.com',
            "test-123"
        )

        # assertions
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""

        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        # assertions
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""

        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        # assertions
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )

        # assertions
        self.assertEqual(str(recipe), recipe.title)

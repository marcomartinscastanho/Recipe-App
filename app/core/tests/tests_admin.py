from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    # overridden form TestCase
    # runs before every test
    def setUp(self):
        # create a client
        self.client = Client()
        # create an admin user
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@fake.com',
            password='test-123'
        )
        # admin is logged in to the client
        self.client.force_login(self.admin_user)
        # create a spare normal user
        self.user = get_user_model().objects.create_user(
            email='test@fake.com',
            password='test-123',
            name='Test McTestington'
        )

    def test_users_listed(self):
        """Test that users are listed on the users page"""

        # core_user_changelist generates a url for our user list page and is defined in the django documentation
        # the reason to use the reverse function instead of typing the url manually is because
        # if we ever change the url in the future we don't have to change it everywhere in the tests because
        # it should update automatically with reverse
        url = reverse('admin:core_user_changelist')
        # uses the test client makes a HTTP get on the url
        response = self.client.get(url)

        # assertions
        # assertContains is smart enough to assert the response code is 200
        # and to check the fields we want are in the response body
        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    # test that the change page renders correctly (i.e. the page where the admins can edit user details)
    def test_user_change_page(self):
        """Test the user edit page works"""

        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/<id>

        result = self.client.get(url)

        # assertions
        self.assertEqual(result.status_code, 200)

    # test that the create page render correctly (i.e. the page where admins can create new users)
    def test_user_create_page(self):
        """Test that the create user page works"""

        url = reverse('admin:core_user_add')

        result = self.client.get(url)

        # assertions
        self.assertEqual(result.status_code, 200)

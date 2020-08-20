from unittest.mock import patch
# allow us to call a command from our source code
from django.core.management import call_command
# operational error that django throws the database is unavailable
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):
    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        # To set up the test, we need to simulate the behaviour of django when the db is available
        # The management command we're implementing will try to retrieve the db connection from django
        # and is gonna check if when we try to retrieve it if the command retrieves an OperationalError or not
        # So we'll override the behaviour of the connection handler and set it to return True

        # As we'll find when we actually create the management command, the way we test if the database is available
        # in django, is we just try to retrieve the default database via the ConnectionHandler
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # the way to mock the behaviour of a function is
            gi.return_value = True
            # this means that everytime ConnectionHandler.__getitem__ is called during test execution,
            # instead of actually performing whatever it does,
            # it will override it and replace it with a mock object that does 2 things:
            # 1. it will just return whatever we specify as return_value
            # 2. it allows us to monitor how many times it was called and the different calls that were made to it

            # wait_for_db is the name of the command we're going to create
            call_command('wait_for_db')

            # assertions
            self.assertEqual(gi.call_count, 1)

    # when we create the management command later, the way it's gonna work is it's gonna be a while loop
    # that checks to see if the ConnectionHandler raises the OperationalError
    # and if it does, then it's gonna wait 1 second and then try again
    # this is so that it doesn't flood the output by trying every microsecond to check the database
    # we can actually remove that 1 second delay in the unit test by mocking the delay with a patch decorator
    # using patch as a decorator is pretty much the same as using it inside the function,
    # but it passes the mock object as an argument of the function
    # even if we don't use it, it has to be there, otherwise we get an error in the test
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # you can set a side effect to the function that we're mocking
            # the side effect that we want is to make the mocked object raise the OperationalError
            # the 5 first times it calls the mocked function
            # and then on the 6th time it doesn't raise the error
            gi.side_effect = [OperationalError] * 5 + [True]

            call_command('wait_for_db')

            # assertions
            self.assertEqual(gi.call_count, 6)

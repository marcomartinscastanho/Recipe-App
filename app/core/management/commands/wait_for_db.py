import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    # overridden function
    # handle function is what is run whenever we run this management command
    def handle(self, *args, **options):
        # write things to the screen
        self.stdout.write('Waiting for database...')

        db_connection = None
        while not db_connection:
            try:
                db_connection = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable. Retrying in 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))

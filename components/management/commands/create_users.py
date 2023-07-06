"""Import: Django command to import data from the previous database."""
from faker import Faker, proxy

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Populate the database random users.'

    def add_arguments(self, parser):
        # Optional argument
        parser.add_argument('-c', '--count',
                            type=str,
                            help='The number of users to be generated.',
                            default=2280)
        
    def handle(self, *args, **kwargs) -> None:
        start = User.objects.count()
        count = kwargs["count"]
        fake = Faker()

        for _ in range(start, count):
            saved= False
            while not saved:
                first = fake.unique.first_name()
                last  = fake.unique.last_name()
                try:
                    user = User.objects.create_user(
                        f"{first} {last}",
                        email=f"{first}.{last}@example.com",
                        password=fake.lexify(text='??????????'),
                        first_name=first,
                        last_name=last
                    )
                    print(user)
                    user.save()
                    saved=True
                except (IntegrityError, proxy.UniquenessException):
                    ...
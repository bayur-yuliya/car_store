import random

from django.core.management.base import BaseCommand

from store.models import CarType, Car


class Command(BaseCommand):
    help = """the command generates a fake posts, 
            if you do not specify a parameter, by default 10 posts are generated"""

    def handle(self, *args, **options):
        for _ in range(10):
            Car.objects.create(
                car_type=CarType(id=random.randint(1, 3)),
                color="red",
                year=random.randint(2009, 2025),
            )
            Car.objects.create(
                car_type=CarType(id=random.randint(1, 3)),
                color="white",
                year=random.randint(2009, 2025),
            )
            Car.objects.create(
                car_type=CarType(id=random.randint(1, 3)),
                color="black",
                year=random.randint(2009, 2025),
            )

        self.stdout.write(self.style.SUCCESS("Все прошло успешно!"))
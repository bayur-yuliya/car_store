from django.core.management.base import BaseCommand

from store.models import CarType, Car


class Command(BaseCommand):
    help = """the command generates a fake posts, 
            if you do not specify a parameter, by default 10 posts are generated"""

    def handle(self, *args, **options):
        Car.objects.create(car_type=CarType(id=1), color="red", year=2023)
        Car.objects.create(car_type=CarType(id=2), color="red", year=2023)
        Car.objects.create(car_type=CarType(id=3), color="red", year=2023)
        Car.objects.create(car_type=CarType(id=1), color="black", year=2023)
        Car.objects.create(car_type=CarType(id=2), color="black", year=2023)
        Car.objects.create(car_type=CarType(id=3), color="black", year=2023)
        Car.objects.create(car_type=CarType(id=1), color="red", year=2023)
        Car.objects.create(car_type=CarType(id=2), color="red", year=2023)
        Car.objects.create(car_type=CarType(id=3), color="red", year=2023)
        Car.objects.create(car_type=CarType(id=1), color="black", year=2023)
        Car.objects.create(car_type=CarType(id=2), color="black", year=2023)
        Car.objects.create(car_type=CarType(id=3), color="black", year=2023)
        Car.objects.create(car_type=CarType(id=1), color="red", year=2023)
        Car.objects.create(car_type=CarType(id=2), color="red", year=2023)
        Car.objects.create(car_type=CarType(id=3), color="red", year=2023)
        Car.objects.create(car_type=CarType(id=1), color="black", year=2023)
        Car.objects.create(car_type=CarType(id=2), color="black", year=2023)
        Car.objects.create(car_type=CarType(id=3), color="black", year=2023)
        Car.objects.create(car_type=CarType(id=1), color="red", year=2023)
        Car.objects.create(car_type=CarType(id=2), color="red", year=2023)
        Car.objects.create(car_type=CarType(id=3), color="red", year=2023)
        Car.objects.create(car_type=CarType(id=1), color="black", year=2023)
        Car.objects.create(car_type=CarType(id=2), color="black", year=2023)
        Car.objects.create(car_type=CarType(id=3), color="black", year=2023)

        self.stdout.write(self.style.SUCCESS("Все прошло успешно!"))

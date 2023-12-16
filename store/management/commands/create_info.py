from django.core.management.base import BaseCommand

from store.models import CarType, Car, Client, Dealership


class Command(BaseCommand):
    help = """the command generates a fake posts, 
            if you do not specify a parameter, by default 10 posts are generated"""

    def handle(self, *args, **options):
        CarType.objects.create(name='M135i xDrive', brand='BMW', price=200)
        CarType.objects.create(name='X7 M60i xDRIVE', brand='BMW', price=100)
        CarType.objects.create(name='XM LABEL RED', brand='BMW', price=150)

        Car.objects.create(car_type=CarType(id=1), color='red', year=2023)
        Car.objects.create(car_type=CarType(id=2), color='red', year=2023)
        Car.objects.create(car_type=CarType(id=3), color='red', year=2023)
        Car.objects.create(car_type=CarType(id=1), color='black', year=2023)
        Car.objects.create(car_type=CarType(id=2), color='black', year=2023)
        Car.objects.create(car_type=CarType(id=3), color='black', year=2023)

        Client.objects.create(name='Tonya', email="test@gmail.com", phone='0387410203')
        Dealership.objects.create(name='OdessaBMW')
        my_instance = Dealership.objects.get(pk=1)

        my_instance.available_car_types.set([CarType.objects.get(id=1)])
        my_instance.clients.set([Client.objects.get(id=1)])

        self.stdout.write(
            self.style.SUCCESS("Все прошло успешно!")
        )

from rest_framework import serializers

from store.models import Car, CarType, Order, Dealership


class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = ["id", "name", "brand", "price"]


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", "car_type", "color", "year", "photo"]


class DealershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealership
        fields = ["name", "available_car_types"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "client", "dealership", "is_paid"]

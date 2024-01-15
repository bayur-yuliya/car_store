import pytest
import requests

from store.models import CarType, Car

API_URL = "http://127.0.0.1:8000/api"


def test_get_cars():
    r = requests.get(API_URL + "/cars/")
    r.raise_for_status()
    assert r.status_code == 200


def test_get_car_types():
    r = requests.get(API_URL + "/car-types/")
    r.raise_for_status()
    assert r.status_code == 200

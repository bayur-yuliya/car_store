from django.shortcuts import render

from .forms import CarForm


def cars(request):
    form = CarForm()
    return render(request, "store/buy_car.html", context={"form": form})

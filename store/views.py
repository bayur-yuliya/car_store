from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import CarForm, ClientForm
from .models import Car


def cars(request):
    if request.method == "GET":
        form = CarForm()
        all_cars = Car.objects.order_by("car_type")
        cars_count = (
            Car.objects.filter(blocked_by_order__isnull=True, owner__isnull=True)
            .aggregate(cars_count=Count("*"))
            .values()
        )
        return render(
            request,
            "store/car_store.html",
            context={"form": form, "all_cars": all_cars, "cars_count": cars_count},
        )

    form = CarForm(request.POST)

    if form.is_valid():
        form.save()
        order_id = form.id

        return redirect(reverse("order", order_id))


def order(request, order_id):
    form_client = ClientForm()

    if request.GET.get("cancel"):
        return redirect(reverse("cars"))

    if request.method == "POST":
        if form_client.is_valid():
            form_client.save()

        return redirect(reverse("order_is_processed"))

    data = {
        "order_info": "order_info",
        "form_client": form_client,
        "order_id": order_id,
    }
    return render(request, "store/order_page.html", context=data)


def order_is_processed(request, order_id):
    return render(
        request, "store/order_is_processed.html", context={"order_id": order_id}
    )

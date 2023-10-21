from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import CarForm, ClientForm


def cars(request):
    form = CarForm()
    return render(request, "store/car_store.html", context={"form": form})


def order(request, order_id):
    form_client = ClientForm()
    if request.POST.get("cancel"):
        return redirect(reverse("cars"))

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

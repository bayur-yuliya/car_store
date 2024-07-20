import random

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from api_store.invoices import create_invoice
from .forms import CarPhotoChangeForm
from .models import Car, Order, OrderQuantity, Dealership, Client, Licence


def cars(request):
    if request.method == "GET":
        all_cars = Car.objects.filter(owner__isnull=True)

        paginator = Paginator(all_cars, 15)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        blocked_cars = Car.objects.filter(
            blocked_by_order__isnull=False, owner__isnull=True
        )

        return render(
            request,
            "store/car_store.html",
            context={
                "all_cars": all_cars,
                "blocked_cars": blocked_cars,
                "page_obj": page_obj,
            },
        )
    try:
        client, existence = Client.objects.get_or_create(
            name=request.user.username, email=request.user.email, phone="0387410203"
        )
    except AttributeError:
        return redirect("account_login")

    find_order = Order.objects.filter(
        client=client,
        dealership=Dealership.objects.get(id=1),
        is_paid=False,
    )

    if find_order.exists():
        order = Order.objects.get(
            client=client,
            dealership=Dealership.objects.get(id=1),
            is_paid=False,
        )
    else:
        order = Order.objects.create(
            client=client,
            dealership=Dealership.objects.get(id=1),
            is_paid=False,
        )

    return redirect(reverse("order", kwargs={"order_id": order.id}))


def add_to_cart(request, car_id):
    try:
        client, existence = Client.objects.get_or_create(
            name=request.user.username, email=request.user.email, phone="0387410203"
        )
    except AttributeError:
        return redirect("account_login")

    order, is_created = Order.objects.get_or_create(
        client=client,
        dealership=Dealership.objects.get(id=1),
        is_paid=False,
    )
    quantity = 1
    order_quantity, is_created = OrderQuantity.objects.get_or_create(
        car_type=Car.objects.get(id=int(car_id)).car_type,
        quantity=quantity,
        order=order,
    )

    if not is_created:
        order_quantity.quantity = order_quantity.quantity + 1
        order_quantity.save()

    Car.objects.get(id=car_id).block(order=order)

    return redirect(reverse("cars"))


def update_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == "GET":
        form = CarPhotoChangeForm(instance=car)
        return render(request, "store/update_car.html", {"car": car, "form": form})

    form = CarPhotoChangeForm(request.POST, request.FILES, instance=car)
    if form.is_valid():
        form.save()
    return redirect(reverse("update_car", kwargs={"car_id": car_id}))


def order(request, order_id):
    order_created = Order.objects.get(id=order_id)
    cars = OrderQuantity.objects.filter(order=order_created).all()

    if request.GET.get("cancel"):
        order_created.delete()
        return redirect(reverse("cars"))

    if request.method == "POST":
        orders = Order.objects.get(client=Client.objects.get(email=request.user.email))
        full_url_webhook = "https://webhook.site/2f8f0a75-24c7-4907-ac1d-efeb1e58d1e8"
        full_url_orders = f"http://127.0.0.1:8000/order_is_processed/{order_id}"
        invoice_url = create_invoice(orders, full_url_webhook, full_url_orders)

        for car in Car.objects.filter(blocked_by_order=order_created.id):
            licence_number = random.randint(1000, 9999)
            if Licence.objects.filter(number=f"BH {licence_number} IT").exists():
                licence_number = random.randint(1000, 9999)
            Licence.objects.create(car=car, number=f"BH {licence_number} IT")

            order_created.is_paid = True
            order_created.save()
            car.sell()
        return redirect(invoice_url)

    data = {
        "order_id": order_id,
        "cars": cars,
    }
    return render(request, "store/order_page.html", context=data)


def order_is_processed(request, order_id):
    if request.GET.get("index_page"):
        return redirect(reverse("cars"))
    if request.GET.get("purchased_cars"):
        return redirect(reverse("purchased_cars"))
    return render(
        request, "store/order_is_processed.html", context={"order_id": order_id}
    )


def purchased_cars(request):
    if request.GET.get("index_page"):
        return redirect(reverse("cars"))

    try:
        client, existence = Client.objects.get_or_create(
            name=request.user.username, email=request.user.email
        )
    except AttributeError:
        return redirect("account_login")

    cars_list = Car.objects.filter(owner=client)
    return render(
        request, "store/purchased_cars.html", context={"cars_list": cars_list}
    )

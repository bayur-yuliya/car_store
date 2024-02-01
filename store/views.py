import random

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from api_store.invoices import create_invoice, verify_signature
from .forms import CarPhotoChangeForm
from .models import Car, Order, OrderQuantity, Dealership, Client, Licence


def cars(request):
    if request.method == "GET":
        all_cars = Car.objects.filter(owner__isnull=True)

        paginator = Paginator(all_cars, 6)
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

    cars_id_list = []

    if request.POST.get("select"):
        select = request.POST.get("select")
        quantity = 1
        order_quantity = OrderQuantity.objects.get_or_create(
            car_type=Car.objects.get(id=int(select)).car_type,
            quantity=quantity,
            order=Order.objects.get(id=order.id),
        )

        if order_quantity[1] is False:
            order_quantity[0].quantity = order_quantity[0].quantity + 1
            order_quantity[0].save()

        cars_id_list.append(int(select))

        for el in cars_id_list:
            Car.objects.get(id=el).block(order=Order.objects.get(id=order.id))

        return redirect(reverse("cars"))

    order_id = order.id
    return redirect(reverse("order", kwargs={"order_id": order_id}))


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
        orders = Order.objects.filter(
            client=Client.objects.get(email=request.user.email)
        )
        full_url_webhook = request.build_absolute_uri(reverse("webhook-mono"))
        full_url_orders = request.build_absolute_uri(
            reverse("order_is_processed", kwargs={"order_id": order_id})
        )
        # invoice_url = create_invoice(orders, full_url_webhook, full_url_orders)
        invoice_url = create_invoice(orders, full_url_webhook, full_url_orders)

        for el in Car.objects.filter(blocked_by_order=order_created.id):
            licence_number = random.randint(1000, 9999)
            if Licence.objects.filter(number=f"BH {licence_number} IT").exists():
                licence_number = random.randint(1000, 9999)
            Licence.objects.create(car=el, number=f"BH {licence_number} IT")

            order_created.is_paid = True
            order_created.save()
            el.sell()
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

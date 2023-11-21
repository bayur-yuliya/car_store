import random

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.signing import Signer, BadSignature
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import RegisterUserForm
from .models import Car, Order, OrderQuantity, Dealership, Client, Licence


def send_activation_email(request, user: User):
    user_signed = Signer().sign(user.id)
    signed_url = request.build_absolute_uri(f"/activate/{user_signed}")
    send_mail(
        "Registration complete",
        "Click here to activate your account: " + signed_url,
        "juliy14497@outlook.com",
        [user.email],
        fail_silently=False,)


def activate(request, user_signed):
    try:
        user_id = Signer().unsign(user_signed)
    except BadSignature:
        return redirect("login")
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect("login")
    user.is_active = True
    user.save()
    return redirect("login")


def register(request):
    if request.method == "GET":
        form = RegisterUserForm()
        return render(request, "store/register.html", {"form": form})

    form = RegisterUserForm(request.POST)
    if form.is_valid():
        form.instance.is_active = False
        form.save()
        send_activation_email(request, form.instance)
        return HttpResponse("Отправили на почту подтверждение регистрации")
    return render(request, "store/register.html", {"form": form})


def cars(request):

    if request.method == "GET":
        all_cars = Car.objects.filter(owner__isnull=True)
        blocked_cars = Car.objects.filter(
            blocked_by_order__isnull=False, owner__isnull=True
        )
        cars_count = (
            all_cars.values("car_type", "color").annotate(Count("id")).order_by()
        )

        return render(
            request,
            "store/car_store.html",
            context={
                "all_cars": all_cars,
                "cars_count": cars_count,
                "blocked_cars": blocked_cars,
            },
        )
    try:
        client, existence = Client.objects.get_or_create(
            name=request.user.username, email=request.user.email, phone="0387410203"
        )
    except AttributeError:
        return redirect("register")

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


def order(request, order_id):
    order_created = Order.objects.get(id=order_id)
    cars = OrderQuantity.objects.filter(order=order_created).all()

    if request.GET.get("cancel"):
        order_created.delete()
        return redirect(reverse("cars"))

    if request.method == "POST":
        for el in Car.objects.filter(blocked_by_order=order_created.id):
            licence_number = random.randint(1000, 9999)

            if Licence.objects.filter(number=f"BH {licence_number} IT").exists():
                licence_number = random.randint(1000, 9999)
                Licence.objects.create(car=el, number=f"BH {licence_number} IT")

            order_created.is_paid = True
            order_created.save()
            el.sell()
        return redirect(reverse("order_is_processed", kwargs={"order_id": order_id}))

    data = {
        "order_id": order_id,
        "cars": cars,
    }
    return render(request, "store/order_page.html", context=data)


def order_is_processed(request, order_id):
    if request.GET.get("index_page"):
        return redirect(reverse("cars"))

    return render(
        request, "store/order_is_processed.html", context={"order_id": order_id}
    )


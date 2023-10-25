from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Car, Order, OrderQuantity, Dealership, Client, CarType


def cars(request):
    order = Order.objects.get_or_create(client=Client.objects.get(id=1), dealership=Dealership.objects.get(id=1))

    if request.method == "GET":
        all_cars = Car.objects.order_by("car_type")
        cars_count = (
            Car.objects.filter(blocked_by_order__isnull=True, owner__isnull=True)
            .aggregate(cars_count=Count("*"))
            .values()
        )
        cart = OrderQuantity.objects.filter(order=Order.objects.get(id=order[0].id)).aggregate(cars_count=Count("*"))
        return render(
            request,
            "store/car_store.html",
            context={"all_cars": all_cars, "cars_count": cars_count, 'cart': cart},
        )

    cars_id_list =[]

    if request.POST.get("select"):
        select = request.POST.get("select")
        OrderQuantity.objects.create(car_type=CarType.objects.get(name=select),
                                                      quantity=1,
                                                      order=Order.objects.get(id=order[0].id))

        car = CarType.objects.get(name=select)
        cars_id_list.append(car.id)
        return redirect(reverse("cars"))

    for el in cars_id_list:
        Car.objects.filter(id=el).block(order=Order.objects.get(id=order[0].id))

    order_id = order[0].id
    return redirect(reverse("order", kwargs={'order_id': order_id}))


def order(request, order_id):
    order_created = Order.objects.get(id=order_id)
    cars = OrderQuantity.objects.filter(order=order_created).all()

    if request.GET.get("cancel"):
        order_created.delete()
        return redirect(reverse("cars"))

    if request.method == "POST":
        return redirect(reverse("order_is_processed", kwargs={'order_id': order_id}))

    data = {
        "order_id": order_id,
        'cars': cars,
    }
    return render(request, "store/order_page.html", context=data)


def order_is_processed(request, order_id):

    return render(
        request, "store/order_is_processed.html", context={"order_id": order_id}
    )

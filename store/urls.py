from django.urls import path

from . import views

urlpatterns = [
    path("", views.cars, name="cars"),
    path("order/<int:order_id>", views.order, name="order"),
    path("add/<int:car_id>", views.add_to_cart, name="add_to_cart"),
    path("update_car/<int:car_id>", views.update_car, name="update_car"),
    path(
        "order_is_processed/<int:order_id>",
        views.order_is_processed,
        name="order_is_processed",
    ),
    path("purchased_cars/", views.purchased_cars, name="purchased_cars"),
]

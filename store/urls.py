from django.contrib.auth.views import LoginView
from django.urls import path

from . import views

urlpatterns = [
    path("", views.cars, name="cars"),
    path("order/<int:order_id>", views.order, name="order"),
    path('update_car/<int:car_id>', views.update_car, name="update_car"),
    path(
        "order_is_processed/<int:order_id>",
        views.order_is_processed,
        name="order_is_processed",
    ),
]

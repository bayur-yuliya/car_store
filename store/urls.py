from django.contrib.auth.views import LoginView
from django.urls import path

from . import views

urlpatterns = [
    path("", views.cars, name="cars"),
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("order/<int:order_id>", views.order, name="order"),
    path("activate/<user_signed>", views.activate, name="activate"),
    path(
        "order_is_processed/<int:order_id>",
        views.order_is_processed,
        name="order_is_processed",
    ),
]

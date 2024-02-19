from django.urls import path
import rest_framework.authtoken.views
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"cars", views.CarViewSet, "car")
router.register(r"car-types", views.CarTypeViewSet, "car_type")
router.register(r"dealership", views.DealershipViewSet, "dealership")
router.register(r"order", views.OrderView, "order")

urlpatterns = router.urls
urlpatterns += [
    path("api-token-auth/", rest_framework.authtoken.views.obtain_auth_token),
    path(
        "webhook-mono/",
        views.MonoAcquiringWebhookReceiver.as_view(),
        name="webhook-mono",
    ),
]

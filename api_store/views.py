from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from api_store.invoices import verify_signature, create_invoice
from api_store.serializers import (
    CarTypeSerializer,
    CarSerializer,
    OrderSerializer,
)
from store.models import Car, CarType, Client, Order, OrderQuantity, Dealership


class CarTypeViewSet(viewsets.ModelViewSet):
    queryset = CarType.objects.all()
    serializer_class = CarTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.filter(owner__isnull=True, blocked_by_order__isnull=True)
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class OrderView(
    generics.ListAPIView,
    generics.RetrieveAPIView,
    GenericViewSet,
):
    queryset = Order.objects.filter(is_paid=False)
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        if car.blocked_by_order or car.owner:
            return Response(
                {"massage": "Car is blocked or already owned"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        client = Client.objects.filter(client=request.user)
        order, created = Order.objects.get_or_create(
            client=client, dealership=Dealership.objects.get(id=1), is_paid=False
        )

        car_type = car.car_type
        order_quantity, _ = OrderQuantity.objects.get_or_create(
            order=order, car_type=car_type
        )
        car.block(order)
        create_invoice(order, reverse("webhook-mono"))
        return Response({"invoice_url": order.invoice_url})

    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        cars = Car.objects.filter(blocked_by_order=order)

        for car in cars:
            car.unblock()
        order.delete()

        return Response({"message": "The order was successfully deleted"})


class MonoAcquiringWebhookReceiver(APIView):
    def post(self, request):
        try:
            verify_signature(request)
        except Exception as e:
            return Response({"status": "error"}, status=400)
        reference = request.data.get("reference")
        order = Order.objects.get(id=reference)
        if order.order_id != request.data.get("invoiceId"):
            return Response({"status": "error"}, status=400)
        order.status = request.data.get("status", "error")
        order.save()
        return Response({"status": "ok"})

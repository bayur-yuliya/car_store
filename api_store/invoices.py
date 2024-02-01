import base64
import hashlib

import ecdsa
import requests
from django.conf import settings

from store.models import OrderInvoice, MonoSettings, Car


def get_monobank_public_key():
    r = requests.get(
        "https://api.monobank.ua/api/merchant/pubkey",
        headers={"X-Token": settings.MONOBANK_TOKEN},
    )
    r.raise_for_status()
    return r.json()["key"]


def _verify_signature(x_sign_base64, body: bytes, public_key):
    pub_key_bytes = base64.b64decode(public_key)
    signature_bytes = base64.b64decode(x_sign_base64)
    pub_key = ecdsa.VerifyingKey.from_pem(pub_key_bytes.decode())
    ok = pub_key.verify(
        signature_bytes,
        body,
        sigdecode=ecdsa.util.sigdecode_der,
        hashfunc=hashlib.sha256,
    )
    return ok


def verify_signature(request):
    ok = _verify_signature(
        request.headers["X-Sign"],
        request.body,
        MonoSettings.get_latest_or_add(get_monobank_public_key).public_key,
    )

    if ok:
        return
    MonoSettings.create_new(get_monobank_public_key)
    ok = _verify_signature(
        request.headers["X-Sign"],
        request.body,
        MonoSettings.get_latest_or_add(get_monobank_public_key).public_key,
    )
    if not ok:
        raise Exception("Signature is not valid")


def create_invoice(order, webhook_url, redirect_url):
    if OrderInvoice.objects.filter(orders__in=order).exists():
        return OrderInvoice.objects.filter(orders__in=order).first().invoice_url

    order_invoice = OrderInvoice.objects.create()
    for el in order:
        order_invoice.orders.add(el)

    amount = 0
    basket_order = []

    for car in Car.objects.filter(owner__isnull=True, blocked_by_order__in=order).all():
        amount += car.car_type.price
        basket_order.append(
            {"name": car.car_type.name, "qty": 1, "sum": car.car_type.price * 100}
        )

    merchants_info = {
        "reference": str(order_invoice.id),
        "destination": "Покупка машины",
        "basketOrder": basket_order,
    }
    request_body = {
        "webHookUrl": webhook_url,
        "redirectUrl": redirect_url,
        "amount": amount,
        "merchantPaymInfo": [merchants_info],
    }
    headers = {"X-Token": settings.MONOBANK_TOKEN}

    r = requests.post(
        "https://api.monobank.ua/api/merchant/invoice/create",
        headers=headers,
        json=request_body,
    )
    r.raise_for_status()
    order_invoice.order_id = r.json()["invoiceId"]
    order_invoice.invoice_url = r.json()["pageUrl"]
    order_invoice.status = "created"
    order_invoice.save()

    return r.json()["pageUrl"]

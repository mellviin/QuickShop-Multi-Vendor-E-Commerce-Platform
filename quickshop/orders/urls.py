from django.urls import path
from . import views

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("payment/", views.payment_page, name="payment_page"),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("", views.my_orders, name="my_orders"),
]
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="consumer_home"),
    path("detail/<int:product_id>/", views.product_detail, name="product_detail"),
]
from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart_page, name="cart_page"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),

    path("wishlist/", views.wishlist_page, name="wishlist_page"),
    path("wishlist/add/<int:product_id>/", views.add_to_wishlist, name="add_to_wishlist"),
    path("wishlist/remove/<int:item_id>/", views.remove_from_wishlist, name="remove_from_wishlist"),

    path("buy-now/<int:product_id>/", views.buy_now, name="buy_now"),
]
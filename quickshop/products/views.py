from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from quickshop.products.models import Product
from quickshop.cart.models import CartItem, WishlistItem


@login_required
def home(request):
    products = Product.objects.all().order_by("-created_at")
    cart_count = CartItem.objects.filter(user=request.user).count()
    wishlist_count = WishlistItem.objects.filter(user=request.user).count()

    return render(request, "products/home.html", {
        "products": products,
        "cart_count": cart_count,
        "wishlist_count": wishlist_count,
    })


@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_count = CartItem.objects.filter(user=request.user).count()
    wishlist_count = WishlistItem.objects.filter(user=request.user).count()

    return render(request, "products/detail.html", {
        "product": product,
        "cart_count": cart_count,
        "wishlist_count": wishlist_count,
    })
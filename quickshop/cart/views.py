from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from quickshop.products.models import Product
from quickshop.cart.models import CartItem, WishlistItem


@login_required
def cart_page(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in items)

    return render(request, "cart/cart.html", {
        "items": items,
        "total": total,
        "cart_count": items.count(),
        "wishlist_count": WishlistItem.objects.filter(user=request.user).count(),
    })


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        item.quantity += 1
        item.save()

    return redirect("cart_page")


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect("cart_page")


@login_required
def wishlist_page(request):
    items = WishlistItem.objects.filter(user=request.user)

    return render(request, "cart/wishlist.html", {
        "items": items,
        "cart_count": CartItem.objects.filter(user=request.user).count(),
        "wishlist_count": items.count(),
    })


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    WishlistItem.objects.get_or_create(user=request.user, product=product)
    return redirect("wishlist_page")


@login_required
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(WishlistItem, id=item_id, user=request.user)
    item.delete()
    return redirect("wishlist_page")


@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        item.quantity += 1
        item.save()

    return redirect("checkout")
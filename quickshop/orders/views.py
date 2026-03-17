from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from quickshop.cart.models import CartItem, WishlistItem
from quickshop.orders.models import Order


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    if not cart_items.exists():
        return redirect("cart_page")

    if request.method == "POST":
        request.session["checkout_data"] = {
            "full_name": request.POST.get("full_name"),
            "phone": request.POST.get("phone"),
            "address": request.POST.get("address"),
            "city": request.POST.get("city"),
            "pincode": request.POST.get("pincode"),
            "delivery_slot": request.POST.get("delivery_slot"),
        }
        return redirect("payment_page")

    return render(request, "orders/checkout.html", {
        "cart_items": cart_items,
        "total": total,
        "cart_count": cart_items.count(),
        "wishlist_count": WishlistItem.objects.filter(user=request.user).count(),
    })


@login_required
def payment_page(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    if "checkout_data" not in request.session:
        return redirect("checkout")

    return render(request, "orders/payment.html", {
        "cart_items": cart_items,
        "total": total,
        "cart_count": cart_items.count(),
        "wishlist_count": WishlistItem.objects.filter(user=request.user).count(),
    })


@login_required
def payment_success(request):
    cart_items = CartItem.objects.filter(user=request.user)
    checkout_data = request.session.get("checkout_data")

    if not cart_items.exists() or not checkout_data:
        return redirect("consumer_home")

    payment_method = request.POST.get("payment_method", "razorpay")
    created_orders = []

    for item in cart_items:
        order = Order.objects.create(
            customer=request.user,
            seller=item.product.seller,
            product=item.product,
            quantity=item.quantity,
            full_name=checkout_data["full_name"],
            phone=checkout_data["phone"],
            address=checkout_data["address"],
            city=checkout_data["city"],
            pincode=checkout_data["pincode"],
            delivery_slot=checkout_data["delivery_slot"],
            payment_method=payment_method,
            status="paid",
            total_price=item.product.price * item.quantity,
        )
        created_orders.append(order)

        if item.product.seller.email:
            send_mail(
                subject="QuickShop: New order received",
                message=(
                    f"Hello {item.product.seller.username},\n\n"
                    f"You received a new order for {item.product.name}.\n"
                    f"Customer: {request.user.username}\n"
                    f"Quantity: {item.quantity}\n"
                    f"Amount: ${item.product.price * item.quantity}\n\n"
                    f"Please prepare the product."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[item.product.seller.email],
                fail_silently=True,
            )

    if request.user.email:
        send_mail(
            subject="QuickShop: Order confirmed",
            message=(
                f"Hello {request.user.username},\n\n"
                f"Your order has been confirmed.\n"
                f"Items: {len(created_orders)}\n"
                f"Delivery to: {checkout_data['address']}, {checkout_data['city']} - {checkout_data['pincode']}\n"
                f"Slot: {checkout_data['delivery_slot']}\n\n"
                f"Thank you for shopping with QuickShop."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=True,
        )

    cart_items.delete()
    request.session.pop("checkout_data", None)

    return render(request, "orders/payment_success.html", {
        "orders": created_orders,
        "cart_count": 0,
        "wishlist_count": WishlistItem.objects.filter(user=request.user).count(),
    })


@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).order_by("-created_at")

    return render(request, "orders/my_orders.html", {
        "orders": orders,
        "cart_count": CartItem.objects.filter(user=request.user).count(),
        "wishlist_count": WishlistItem.objects.filter(user=request.user).count(),
    })
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from quickshop.cart.models import CartItem, WishlistItem
from quickshop.orders.models import Order


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    if not cart_items.exists():
        return redirect("cart_page")

    if request.method == "POST":
        request.session["checkout_data"] = {
            "full_name": request.POST.get("full_name"),
            "phone": request.POST.get("phone"),
            "address": request.POST.get("address"),
            "city": request.POST.get("city"),
            "pincode": request.POST.get("pincode"),
            "delivery_slot": request.POST.get("delivery_slot"),
        }
        return redirect("payment_page")

    return render(request, "orders/checkout.html", {
        "cart_items": cart_items,
        "total": total,
        "cart_count": cart_items.count(),
        "wishlist_count": WishlistItem.objects.filter(user=request.user).count(),
    })


@login_required
def payment_page(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    if "checkout_data" not in request.session:
        return redirect("checkout")

    return render(request, "orders/payment.html", {
        "cart_items": cart_items,
        "total": total,
        "cart_count": cart_items.count(),
        "wishlist_count": WishlistItem.objects.filter(user=request.user).count(),
    })


@login_required
def payment_success(request):
    cart_items = CartItem.objects.filter(user=request.user)
    checkout_data = request.session.get("checkout_data")

    if not cart_items.exists() or not checkout_data:
        return redirect("consumer_home")

    payment_method = request.POST.get("payment_method", "razorpay")
    created_orders = []

    for item in cart_items:
        order = Order.objects.create(
            user=request.user,
            product=item.product,
            quantity=item.quantity,
            address=checkout_data["address"],
            city=checkout_data["city"],
            payment_method=payment_method,
            status="placed",
        )
        created_orders.append(order)

        if item.product.seller.email:
            send_mail(
                subject="QuickShop: New order received",
                message=(
                    f"Hello {item.product.seller.username},\n\n"
                    f"You received a new order for {item.product.name}.\n"
                    f"Customer: {request.user.username}\n"
                    f"Quantity: {item.quantity}\n"
                    f"Amount: ${item.product.price * item.quantity}\n\n"
                    f"Please prepare the product."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[item.product.seller.email],
                fail_silently=True,
            )

    if request.user.email:
        send_mail(
            subject="QuickShop: Order confirmed",
            message=(
                f"Hello {request.user.username},\n\n"
                f"Your order has been confirmed.\n"
                f"Items: {len(created_orders)}\n"
                f"Delivery to: {checkout_data['address']}, {checkout_data['city']} - {checkout_data['pincode']}\n"
                f"Slot: {checkout_data['delivery_slot']}\n\n"
                f"Thank you for shopping with QuickShop."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=True,
        )

    cart_items.delete()
    request.session.pop("checkout_data", None)

    return render(request, "orders/payment_success.html", {
        "orders": created_orders,
        "cart_count": 0,
        "wishlist_count": WishlistItem.objects.filter(user=request.user).count(),
    })


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "orders/my_orders.html", {
        "orders": orders,
        "cart_count": CartItem.objects.filter(user=request.user).count(),
        "wishlist_count": WishlistItem.objects.filter(user=request.user).count(),
    })
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from quickshop.products.models import Product
from quickshop.accounts.models import Profile
from quickshop.orders.models import Order


@login_required
def dashboard(request):
    profile = Profile.objects.filter(user=request.user).first()

    if not profile or profile.role != "seller":
        return redirect("/products/")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add_product":
            name = (request.POST.get("name") or "").strip()
            category = (request.POST.get("category") or "").strip()
            description = (request.POST.get("description") or "").strip()
            price = request.POST.get("price")
            quantity = request.POST.get("quantity")
            image = request.FILES.get("image")

            if name and category and description and price and quantity:
                Product.objects.create(
                    seller=request.user,
                    name=name,
                    category=category,
                    description=description,
                    price=price,
                    quantity=quantity,
                    image=image,
                )
            return redirect("/seller/dashboard/")

        elif action == "edit_product":
            product_id = request.POST.get("product_id")
            product = get_object_or_404(Product, id=product_id, seller=request.user)

            product.name = (request.POST.get("name") or "").strip()
            product.category = (request.POST.get("category") or "").strip()
            product.description = (request.POST.get("description") or "").strip()
            product.price = request.POST.get("price")
            product.quantity = request.POST.get("quantity")

            new_image = request.FILES.get("image")
            if new_image:
                product.image = new_image

            product.save()
            return redirect("/seller/dashboard/")

        elif action == "delete_product":
            product_id = request.POST.get("product_id")
            product = get_object_or_404(Product, id=product_id, seller=request.user)
            product.delete()
            return redirect("/seller/dashboard/")

        elif action == "update_order_status":
            order_id = request.POST.get("order_id")
            new_status = request.POST.get("status")

            order = get_object_or_404(
                Order.objects.select_related("product"),
                id=order_id,
                product__seller=request.user
            )

            valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
            if new_status in valid_statuses:
                order.status = new_status
                order.save()

            return redirect("/seller/dashboard/")

    search_query = (request.GET.get("search") or "").strip()
    category_filter = (request.GET.get("category") or "").strip()
    order_status_filter = (request.GET.get("order_status") or "").strip()

    all_products = Product.objects.filter(seller=request.user).order_by("-created_at")
    all_orders = (
        Order.objects
        .filter(product__seller=request.user)
        .select_related("user", "product")
        .order_by("-created_at")
    )

    seller_products = all_products
    seller_orders = all_orders

    if search_query:
        seller_products = seller_products.filter(name__icontains=search_query)

    if category_filter:
        seller_products = seller_products.filter(category=category_filter)

    if order_status_filter:
        seller_orders = seller_orders.filter(status=order_status_filter)

    total_products = all_products.count()
    total_orders = all_orders.count()
    placed_orders = all_orders.filter(status="placed").count()
    shipped_orders = all_orders.filter(status="shipped").count()
    delivered_orders = all_orders.filter(status="delivered").count()

    total_revenue = Decimal("0.00")
    for order in all_orders:
        total_revenue += order.product.price * order.quantity

    seller_notifications = []
    recent_orders = all_orders[:8]
    for order in recent_orders:
        seller_notifications.append({
            "icon": "🛒",
            "title": "New order received",
            "message": f"{order.user.username} ordered {order.quantity} × {order.product.name}",
            "status": order.get_status_display(),
            "time": order.created_at,
        })

    edit_product_id = request.GET.get("edit")
    edit_product = None
    if edit_product_id:
        edit_product = Product.objects.filter(id=edit_product_id, seller=request.user).first()

    context = {
        "seller_products": seller_products,
        "seller_orders": seller_orders,
        "seller_notifications": seller_notifications,
        "seller_notification_count": len(seller_notifications),
        "total_products": total_products,
        "total_orders": total_orders,
        "placed_orders": placed_orders,
        "shipped_orders": shipped_orders,
        "delivered_orders": delivered_orders,
        "total_revenue": total_revenue,
        "search_query": search_query,
        "category_filter": category_filter,
        "order_status_filter": order_status_filter,
        "edit_product": edit_product,
        "order_status_choices": Order.STATUS_CHOICES,
    }

    return render(request, "seller/dashboard.html", context)
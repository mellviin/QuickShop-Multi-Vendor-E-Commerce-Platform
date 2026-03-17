from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from quickshop.accounts.models import Profile
from quickshop.orders.models import Order
from quickshop.cart.models import CartItem, WishlistItem


def login_view(request):
    error = ""
    selected_role = "consumer"

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        selected_role = request.POST.get("role", "consumer")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            profile = Profile.objects.filter(user=user).first()

            if profile and profile.role == selected_role:
                login(request, user)
                if selected_role == "seller":
                    return redirect("/seller/dashboard/")
                return redirect("/products/")
            else:
                error = "Account role does not match."
        else:
            error = "Invalid username or password."

    return render(request, "accounts/login.html", {
        "error": error,
        "selected_role": selected_role
    })


def register_view(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()
        role = request.POST.get("role", "consumer")
        phone = request.POST.get("mobile", "").strip()

        if password != confirm_password:
            error = "Passwords do not match."
        elif User.objects.filter(username=username).exists():
            error = "Username already exists."
        else:
            user = User.objects.create_user(
                username=username,
                email=username,  # assuming username is email
                password=password
            )
            Profile.objects.create(user=user, role=role, phone=phone)
            return redirect("/")

    return render(request, "accounts/register.html", {"error": error})


def logout_view(request):
    logout(request)
    return redirect("/")


def forgot_password(request):
    return render(request, "accounts/forgot_password.html")


@login_required
def my_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        request.user.first_name = request.POST.get("first_name", "").strip()
        request.user.last_name = request.POST.get("last_name", "").strip()
        request.user.email = request.POST.get("email", "").strip()

        if hasattr(profile, "phone"):
            profile.phone = request.POST.get("phone", "").strip()

        request.user.save()
        profile.save()

        return redirect("/profile/")

    total_orders = Order.objects.filter(user=request.user).count()
    cart_count = CartItem.objects.filter(user=request.user).count()
    wishlist_count = WishlistItem.objects.filter(user=request.user).count()

    context = {
        "profile_obj": profile,
        "total_orders": total_orders,
        "cart_count": cart_count,
        "wishlist_count": wishlist_count,
    }
    return render(request, "accounts/profile.html", context)
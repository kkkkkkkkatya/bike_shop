from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegisterForm, OrderForm
from .facade import BikeShopFacade
from .models import Order


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user_data = {
                    "username": form.cleaned_data["username"],
                    "email": form.cleaned_data["email"],
                    "password": form.cleaned_data["password"],
                }
                user = BikeShopFacade.register_user(user_data)  # 👈 фасад виконує все
                login(request, user)
                messages.success(request, "Реєстрація пройшла успішно!")
                return redirect("order")
            except Exception as e:
                messages.error(request, f"Помилка реєстрації: {str(e)}")
    else:
        form = RegisterForm()
    return render(request, "registration.html", {"form": form})


@login_required(login_url="login")
def order_bike(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            bike_type = form.cleaned_data["bike_type"]
            bike = BikeShopFacade.create_order(bike_type)  # 👈 теж через фасад
            Order.objects.create(
                user=request.user,
                bike_type=bike_type,
                details=bike.show()
            )
            return render(request, "order.html", {"bike": bike})
    else:
        form = OrderForm()
    return render(request, "order.html", {"form": form})

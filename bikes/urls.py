from django.urls import path
from .views import register, order_bike
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("register/", register, name="register"),
    path("order/", order_bike, name="order"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
]

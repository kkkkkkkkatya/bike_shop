from .builder import RegularBikeBuilder, ElectricBikeBuilder, Director
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.core.mail import send_mail


class BikeShopFacade:
    @staticmethod
    def validate_user_data(data: dict):
        if not data.get("username") or not data.get("email") or not data.get("password"):
            raise ValidationError("Усі поля обов'язкові.")
        try:
            validate_email(data["email"])
        except ValidationError:
            raise ValidationError("Невірна електронна адреса.")
        if len(data["password"]) < 6:
            raise ValidationError("Пароль має містити щонайменше 6 символів.")
        return True

    @staticmethod
    def register_user(data: dict):
        BikeShopFacade.validate_user_data(data)
        user = User.objects.create_user(
            username=data["username"],
            email=data["email"],
            password=data["password"]
        )
        BikeShopFacade.send_confirmation_email(user.email)
        return user

    @staticmethod
    def send_confirmation_email(email: str):
        send_mail(
            subject="Підтвердження реєстрації",
            message="Дякуємо за реєстрацію в нашому магазині велосипедів!",
            from_email="your_bikeshop@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )

    @staticmethod
    def create_order(bike_type: str):
        if bike_type == "electric":
            builder = ElectricBikeBuilder()
        else:
            builder = RegularBikeBuilder()
        director = Director(builder)
        return director.build_bike()

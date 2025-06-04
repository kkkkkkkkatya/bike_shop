from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bike_type = models.CharField(max_length=50)
    details = models.TextField()

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class Survey(models.Model):
    worker = models.BooleanField("Я работник приёмной комиссии:", default=False)
    city = models.CharField("Родной город:", max_length=100)
    points = models.IntegerField("Сумма баллов ЕГЭ:", validators=[MinValueValidator(1), MaxValueValidator(300)])
    main_direction = models.CharField("Направление подготовки:",max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


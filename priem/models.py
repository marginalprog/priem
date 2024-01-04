from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class Survey(models.Model):
    worker = models.BooleanField("Я работник приёмной комиссии:", default=False)
    city = models.CharField("Родной город:", max_length=100)
    points = models.IntegerField("Сумма баллов ЕГЭ:", validators=[MinValueValidator(1), MaxValueValidator(300)])
    main_direction = models.CharField("Направление подготовки:", max_length=100)
    is_form_filled = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # и дополнительные поля типа ФИО, паспорт и тп.

    def __str__(self):
        return (f'Анкета пользователя {self.user}')

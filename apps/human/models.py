from django.db import models


class Human(models.Model):
    """Human Model"""

    first_name = models.CharField(verbose_name='Имя', max_length=250)
    last_name = models.CharField(verbose_name='Фамилия', max_length=250)

from django.db import models
from datetime import datetime
from ..manage.models import *
from django.utils.safestring import mark_safe

class ContractorsTotal(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Подрядчик')
    year = models.CharField(max_length=255, blank=True, null=True, verbose_name='Год')
    contracts_cnt = models.IntegerField(verbose_name='Контрактов')
    contracts_active = models.IntegerField(verbose_name='Контрактов в работе')
    contracts_price = models.IntegerField(verbose_name='Стоимость всего')
    contracts_active_price = models.IntegerField(verbose_name='Стоимость в работе')
    objects_cnt = models.IntegerField(verbose_name='Объектов')
    objects_active = models.IntegerField(verbose_name='Объектов в работе')
    objects_progress = models.DecimalField(max_digits=8, decimal_places=3, verbose_name='Выполнение')
    # accidents_month = models.IntegerField(verbose_name='Инцидентов за период')


    class Meta:
        managed = False
        db_table = 'vcontractors_total'
        verbose_name = 'Итоговый Подрядчики'
        verbose_name_plural = 'Итоговый Подрядчики'

    def __str__(self):
        return f'{self.name}'


class ZonesTotal(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Геозона')
    year = models.CharField(max_length=255, blank=True, null=True, verbose_name='Год')
    # month = models.CharField(max_length=255, blank=True, null=True, verbose_name='Месяц')
    contracts_cnt = models.IntegerField(verbose_name='Контрактов')
    contracts_active = models.IntegerField(verbose_name='Контрактов в работе')
    contracts_price = models.IntegerField(verbose_name='Стоимость всего')
    contracts_active_price = models.IntegerField(verbose_name='Стоимость в работе')
    objects_cnt = models.IntegerField(verbose_name='Объектов')
    objects_active = models.IntegerField(verbose_name='Объектов в работе')
    objects_progress = models.DecimalField(max_digits=8, decimal_places=3, verbose_name='Выполнение')
    # accidents_month = models.IntegerField(verbose_name='Инцидентов за период')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        managed = False
        db_table = 'vzones_total'
        verbose_name = 'Итоговый Геозоны'
        verbose_name_plural = 'Итоговый Геозоны'


class ObjectProgress(models.Model):
    year = models.CharField(max_length=255, blank=True, null=True, verbose_name='Год контракта')
    month = models.CharField(max_length=255, blank=True, null=True, verbose_name='Месяц выполнения')
    contract = models.ForeignKey(Contract, models.PROTECT, blank=True, null=True, verbose_name='Контракт', related_name='+')
    contractor = models.ForeignKey(Contractor, models.PROTECT, blank=True, null=True, verbose_name='Подрядчик', related_name='+')
    zone = models.ForeignKey(Zone, models.PROTECT, blank=True, null=True, verbose_name='Геозона', related_name='+')
    price = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True, verbose_name='Цена')
    finished_price = models.IntegerField(blank=True, null=True, verbose_name='Освоено')
    progress = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True, verbose_name='Прогресс')
    finished_count = models.IntegerField(blank=True, null=True, verbose_name='Выполненных')
    start_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата начала')
    finish_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания')

    class Meta:
        managed = False
        db_table = 'vcontract_objects'
        verbose_name = 'Выполнение по участкам'
        verbose_name_plural = 'Выполнение по участкам'

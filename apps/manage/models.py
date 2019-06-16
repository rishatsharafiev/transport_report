from django.db import models

from datetime import datetime


class DeletedExcludeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(deleted__isnull=False)

class Contractor(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Наименование')
    inn = models.BigIntegerField(blank=True, null=True, verbose_name='ИНН')
    kpp = models.BigIntegerField(blank=True, null=True, verbose_name='КПП')
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name='Адрес')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    modified = models.DateTimeField(blank=True, null=True, auto_now=True)
    deleted = models.DateTimeField(blank=True, null=True)

    objects = DeletedExcludeManager()

    class Meta:
        managed = False
        db_table = 'tcontractor'
        verbose_name = 'Подрядчик'
        verbose_name_plural = 'Подрядчики'

    def __str__(self):
        return f'{self.name}'


class ZoneType(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Наименование')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        managed = False
        db_table = 'tzonetype'
        verbose_name = 'Тип геозоны'
        verbose_name_plural = 'Типы геозон'

    def __str__(self):
        return f'{self.name}'


class Zone(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Наименование')
    parent = models.ForeignKey('self', models.PROTECT, blank=True, null=True, related_name='+', verbose_name='Принадлежность')
    zonetype = models.ForeignKey(ZoneType, models.PROTECT, blank=True, null=True, related_name='+', verbose_name='Тим геозоны')
    address = models.CharField(max_length=500, blank=True, null=True, verbose_name='Адрес')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        managed = False
        db_table = 'tzone'
        verbose_name = 'Геозона'
        verbose_name_plural = 'Геозоны'


class Contract(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Наименование')
    numb = models.CharField(max_length=255, blank=True, null=True, verbose_name='Номер', unique=True)
    contract_date = models.DateField(blank=True, null=True, verbose_name='Дата')
    zone = models.ForeignKey(Zone, models.PROTECT, blank=True, null=True, verbose_name='Геозона')
    main_contractor = models.ForeignKey(Contractor, models.PROTECT, blank=True, null=True, related_name='+', verbose_name='Генподрядчик')
    sub_contractor = models.ForeignKey(Contractor, models.PROTECT, blank=True, null=True, related_name='+', verbose_name='Субподрядчик')
    address = models.CharField(max_length=500, blank=True, null=True, verbose_name='Адрес')
    total_price = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True, verbose_name='Сметная стоимость')
    contract_end = models.DateField(blank=True, null=True, verbose_name='Дата окончания')
    responsible_user_id = models.BigIntegerField(blank=True, null=True, verbose_name='Ответственный')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    start_date = models.DateTimeField(blank=True, null=True, verbose_name='Начало работ')
    finish_date = models.DateTimeField(blank=True, null=True, verbose_name='Окончание работ')
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    modified = models.DateTimeField(blank=True, null=True, auto_now=True)
    deleted = models.DateTimeField(blank=True, null=True)

    objects = DeletedExcludeManager()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        managed = False
        db_table = 'tcontract'
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'


class ContractObject(models.Model):
    contract = models.ForeignKey(Contract, models.PROTECT, blank=True, null=True, verbose_name='Контракт')
    contractor = models.ForeignKey(Contractor, models.PROTECT, blank=True, null=True, verbose_name='Подрядчик')
    zone = models.ForeignKey(Zone, models.PROTECT, blank=True, null=True, verbose_name='Геозона')
    from_latitude = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True, verbose_name='Широта, начало')
    from_longitude = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True, verbose_name='Долгота, начало')
    to_latitude = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True, verbose_name='Широта, окончание')
    to_longitude = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True, verbose_name='Долгота, окончание')
    price = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True, verbose_name='Цена')
    start_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата начала')
    finish_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания')
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    modified = models.DateTimeField(blank=True, null=True, auto_now=True)
    deleted = models.DateTimeField(blank=True, null=True)
    
    objects = DeletedExcludeManager()

    def delete(self):
        self.deleted = datetime.now()
        self.save()
        
    def __str__(self):
            return f'{self.contract} {self.contractor}'

    class Meta:
        managed = False
        db_table = 'tcontractobject'
        verbose_name = 'Объект контракта'
        verbose_name_plural = 'Объекты контракта'


class ObjectProgress(models.Model):
    contract = models.ForeignKey(Contract, models.PROTECT, blank=True, null=True, verbose_name='Контракт')
    contractobject = models.ForeignKey(ContractObject, models.PROTECT, blank=True, null=True, verbose_name='Объект контракта')
    contractor = models.ForeignKey(Contractor, models.PROTECT, blank=True, null=True, verbose_name='Подрядчик')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    from_latitude = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True, verbose_name='Широта, начало')
    from_longitude = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True, verbose_name='Долгота, начало')
    to_latitude = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True, verbose_name='Широта, окончание')
    to_longitude = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True, verbose_name='Долгота, окончание')
    price = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True, verbose_name='Цена')
    start_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата начала')
    finish_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания')
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    modified = models.DateTimeField(blank=True, null=True, auto_now=True)
    deleted = models.DateTimeField(blank=True, null=True)

    objects = DeletedExcludeManager()

    def __str__(self):
            return f'{self.contract} {self.contractor}'

    class Meta:
        managed = False
        db_table = 'tobjectprogress'
        verbose_name = 'Выполнение объёмов'
        verbose_name_plural = 'Выполнение объёмов'

# Generated by Django 2.1.5 on 2019-06-10 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0004_auto_20190610_0326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='uri',
            field=models.CharField(max_length=255, verbose_name='URI'),
        ),
    ]
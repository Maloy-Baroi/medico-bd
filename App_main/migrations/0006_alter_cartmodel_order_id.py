# Generated by Django 4.0.6 on 2022-07-11 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_main', '0005_cartmanagermodel_cartmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartmodel',
            name='order_id',
            field=models.CharField(default='000', max_length=100),
        ),
    ]

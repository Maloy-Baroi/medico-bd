# Generated by Django 4.0.6 on 2022-07-11 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_main', '0007_remove_cartmodel_cart_cartmodel_medicineitem_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartmodel',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

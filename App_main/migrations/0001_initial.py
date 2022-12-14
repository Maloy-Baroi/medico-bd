# Generated by Django 4.0.6 on 2022-07-07 11:18

from django.db import migrations, models
import django.db.models.deletion

from django.conf import settings

import App_main.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConsumingType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consuming_type', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MedicineGenericModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine_type', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MedicineModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('old_price', models.CharField(blank=True, default='NONE', max_length=100, null=True)),
                ('price', models.CharField(default='NONE', max_length=100)),
                ('description', models.TextField()),
                ('medicine_power', models.CharField(max_length=10)),
                ('availability', models.BooleanField(default=True)),
                ('total_available', models.IntegerField(default=1)),
                ('category', models.ManyToManyField(to='App_main.categorymodel')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                              related_name='medicine_company', to='App_main.companymodel')),
                ('generic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                              related_name='medicine_generic', to='App_main.medicinegenericmodel')),
                ('type_of_consumption', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING,
                                                          related_name='consumption_type',
                                                          to='App_main.consumingtype')),
            ],
        ),
        migrations.CreateModel(
            name='CartModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_cart',
                                           to=settings.AUTH_USER_MODEL)),
                ('order_id', models.CharField(default='000', max_length=100)),
                ('medicineItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicine',
                                                   to='App_main.models.MedicineModel')),
                ('quantity', models.PositiveIntegerField()),
                ('ordered', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('order_date', models.DateTimeField()),
            ],
        ),
    ]

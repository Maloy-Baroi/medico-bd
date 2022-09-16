from django.contrib.auth.models import User
from django.db import models
from App_main.All_data import common_description


# Create your models here.
class CategoryModel(models.Model):
    # ঔষধ কাদের জন্য
    category_name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category_image/', blank=True)

    def __str__(self):
        return f"{self.category_name}"


class CompanyModel(models.Model):
    # কোম্পানির নাম
    company_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.company_name}"


class MedicineGenericModel(models.Model):
    # কোম্পানির নামের বাহিরেও মেডিসিনের যে নাম বিশ্বের সকল দেশের জন্য এক, সেই নাম
    medicine_type = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.medicine_type}"


class ConsumingType(models.Model):
    # ঔষধ কিভাবে খাবে সেটা, চুষে খাবে নাকি গিলে খাবে নাকি ইঞ্জেকশন দেবে সেটা
    consuming_type = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.consuming_type}"


class MedicineModel(models.Model):
    name = models.CharField(max_length=100)
    old_price = models.CharField(max_length=100, default="NONE", blank=True, null=True)
    price = models.CharField(max_length=100, default="NONE")
    description = models.TextField(default=common_description)
    category = models.ManyToManyField(CategoryModel)
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE, related_name='medicine_company', blank=True,
                                null=True)
    generic = models.ForeignKey(MedicineGenericModel, on_delete=models.CASCADE, related_name='medicine_generic',
                                blank=True, null=True)
    type_of_consumption = models.ForeignKey(ConsumingType, on_delete=models.DO_NOTHING, related_name='consumption_type',
                                            default=None)
    medicine_power = models.CharField(max_length=10)
    availability = models.BooleanField(default=True)
    total_available = models.IntegerField(default=1)
    image = models.ImageField(upload_to='medicine_images', blank=True)

    def __str__(self):
        return f"{self.name}"


num_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']


class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_cart')
    order_id = models.CharField(max_length=100, default="000")
    medicineItem = models.ForeignKey(MedicineModel, on_delete=models.CASCADE, related_name='medicine')
    quantity = models.PositiveIntegerField()
    ordered = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user}'s cart"

    def total_price(self):
        price_0 = self.medicineItem.price
        list_price_0 = list(price_0.strip(""))
        price_unit_list = []
        for i in list_price_0:
            if f"{i}" in num_list:
                price_unit_list.append(i)
        so_price = "".join(price_unit_list)
        so_price = float(so_price)
        total = self.quantity * so_price
        return total


status_choice = (
    ('Processing', 'Processing'),
    ('Confirmed', 'Confirmed'),
    ('On the way', 'On the way'),
    ('Rejected', 'Rejected'),
    ('Completed', 'Completed'),
)


class Order(models.Model):
    order_items = models.ManyToManyField(CartModel)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=264, blank=True, null=True)
    order_id = models.CharField(max_length=264, blank=True, null=True)
    status = models.CharField(max_length=50, default="Processing", choices=status_choice)
    total_price = models.PositiveIntegerField(blank=True, null=True)

    additional_info = models.TextField(max_length=400, blank=True, null=True)
    selected_delivery_address = models.CharField(max_length=10)

    def get_order_total(self):
        total = 0
        for i in self.order_items.all():
            total += i.quantity * i.item.price_per_unit
        return format(total, '0.2f')

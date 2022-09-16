from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class ProfileModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='customer')
    fullName = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=14, unique=True)
    profile_picture = models.ImageField(upload_to='customers_picture/')
    paymentID = models.CharField(max_length=50, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fullName}"


division = (
    ('Barishal', 'Barishal'),
    ('Chattogram', 'Chattogram'),
    ('Dhaka', 'Dhaka'),
    ('Khulna', 'Khulna'),
    ('Mymensingh', 'Mymensingh'),
    ('Rajshahi', 'Rajshahi'),
    ('Rangpur', 'Rangpur'),
    ('Sylhet', 'Sylhet'),
)

address_type_ = (
    ('Home', 'Home'),
    ('Office', 'Office'),
    ('Home Town', 'Home Town'),
)


class CityModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class AreaModel(models.Model):
    division_id = models.ForeignKey(CityModel, on_delete=models.DO_NOTHING, related_name='division', blank=True)
    area_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.area_name}"


class DeliveryAddressModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='delivery_address_of_user')
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    house_address = models.TextField()
    address_type = models.CharField(choices=address_type_, max_length=12)

    def __str__(self):
        return f"{self.house_address}, {self.area}, {self.city}"

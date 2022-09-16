import uuid
from datetime import datetime

from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from App_main.models import *
from App_main.All_data import *
from App_auth.models import *
import random


# Create your views here.
def medicine_divide_into_covid_and_women_category(medicinesArray, covidList, womenList):
    if len(medicinesArray) == 0:
        return covidList, womenList
    else:
        for j in range(0, len(medicinesArray[0].category.values_list())):
            if 'Covid-19 Special' == medicinesArray[0].category.values_list()[j][1]:
                covidList.append(medicinesArray[0])
            elif 'Women Care' == medicinesArray[0].category.values_list()[j][1]:
                womenList.append(medicinesArray[0])
        medicinesArray.remove(medicinesArray[0])
        return medicine_divide_into_covid_and_women_category(medicinesArray, covidList, womenList)


@login_required
def homeReturn(request):
    return HttpResponseRedirect(reverse('App_main:home'))


@login_required
def home(request):
    carts = CartModel.objects.filter(user=request.user, ordered=False)
    total_price = [x.total_price() for x in carts]
    total = sum(total_price)
    content = {
        'categories': categoriesList,
        'carts': carts,
        'total': total,
    }
    return render(request, 'Home.html', context=content)


def covid_and_women(request):
    medicines = MedicineModel.objects.all()
    covid_ = []
    women_ = []
    covid_, women_ = medicine_divide_into_covid_and_women_category(list(medicines), [], [])
    return JsonResponse({""})


def single_medicine(request, pk, previous):
    medicine = MedicineModel.objects.get(id=pk)
    previous_path = previous
    image = []
    for i in medicine.category.all():
        image.append(i.image.url)
    content = {
        'medicine': medicine,
        'back_to_previous': previous_path,
        'image': image,
    }
    return render(request, 'App_main/single_medicine.html', context=content)


def all_category(request):
    return render(request, 'App_main/all_categories.html')


def medicineList(medicines, medicList):
    if len(medicines) == 0:
        return medicList
    else:
        medicList.append(medicines[0].name)
        medicines.remove(medicines[0])
        return medicineList(medicines, medicList)


def all_medicine(request):
    medicines = MedicineModel.objects.all()
    medicineNameList = medicineList(list(medicines), [])

    content = {
        'medicines': medicines,
        'medicineNameList': medicineNameList,
    }

    return render(request, 'App_main/AllMedicine.html', context=content)


def medicine_search(request):
    content = {

    }
    if request.method == 'POST':
        back_to_previous = request.POST.get('back-to-previous')
        searched_medicine = request.POST.get('searched-medicine')
        medicines = MedicineModel.objects.filter(Q(name__icontains=searched_medicine))
        content['medicines'] = medicines
        content['back_to_previous'] = back_to_previous
    return render(request, 'App_main/searched_medicine.html', context=content)


def choose_location(request):
    delivery_addresses = DeliveryAddressModel.objects.filter(user=request.user)
    try:
        profile = ProfileModel.objects.get(user=request.user)
    except:
        return HttpResponseRedirect(reverse('App_auth:profile-view'))
    content = {
        'delivery_addresses': delivery_addresses,
        'profile': profile
    }
    return render(request, 'App_main/choose_location.html', context=content)


def add_locations(request):
    cities = CityModel.objects.all()
    areas = AreaModel.objects.all()
    profile = ProfileModel.objects.get(user=request.user)

    if request.method == 'POST':
        city = request.POST.get('city')
        area = request.POST.get('area')
        house = request.POST.get('house')
        address_type = request.POST.get('address-type')
        if DeliveryAddressModel.objects.filter(user=request.user, address_type=address_type).exists():
            total_address = DeliveryAddressModel.objects.get(user=request.user, address_type=address_type)
            total_address.city = city
            total_address.area = area
            total_address.house_address = house
            total_address.save()
        else:
            total_address = DeliveryAddressModel(user=request.user, city=city, area=area, house_address=house,
                                                 address_type=address_type)
            total_address.save()
        return HttpResponseRedirect(reverse('App_main:choose-location'))

    content = {
        'cities': cities,
        'areas': areas,
        'profile': profile,
    }

    return render(request, 'App_main/add_new_address.html', context=content)


def add_to_cart_view(request):
    if request.method == 'POST':
        medicine_id = request.POST.get('medicine_id')
        cartQuantity = request.POST.get('cart_quantity')
        medicine = MedicineModel.objects.get(id=medicine_id)
        cart = CartModel.objects.filter(user=request.user, medicineItem=medicine, ordered=False)
        if cart.exists():
            cart[0].quantity += int(cartQuantity)
            cart[0].save()
        else:
            cart = CartModel(user=request.user, medicineItem=medicine, quantity=int(cartQuantity), ordered=False,
                             order_date=datetime.today())
            cart.save()

    return HttpResponseRedirect(reverse('App_main:home'))


def checkout_view(request):
    delivery_addresses = DeliveryAddressModel.objects.filter(user=request.user)
    profile = ProfileModel.objects.get(user=request.user)
    cart = CartModel.objects.filter(user=request.user, ordered=False)
    total_price = [x.total_price() for x in cart]
    total = sum(total_price)
    content = {
        'delivery_addresses': delivery_addresses,
        'profile': profile,
        'total': total,
    }
    return render(request, 'App_main/checkout.html', context=content)


def order_view(request):
    cart = CartModel.objects.filter(user=request.user, ordered=False)
    if request.method == 'POST':
        total = request.POST.get('price')
        address_type = request.POST.get('address_type')
        addition_info = request.POST.get('additional_info')
        customer_profile = ProfileModel.objects.get(user=request.user)
        orderID = random.randint(1000, 5000000)
        print(address_type)
        if not addition_info:
            addition_info = ""
        order = Order.objects.create(user=request.user,
                                     ordered=True,
                                     payment_id=customer_profile.paymentID,
                                     order_id="MedicBD-20220-" + str(orderID),
                                     status='Processing',
                                     total_price=total,
                                     selected_delivery_address=address_type,
                                     additional_info=addition_info
                                     )
        for i in cart:
            order.order_items.add(i.id)
            i.ordered = True
            i.save()
        # order.save()
        return HttpResponseRedirect(reverse('App_main:home'))


def my_all_orders(request):
    all_orders = Order.objects.filter(user=request.user)
    running_orders = []
    done_orders = []
    for x in all_orders:
        if x.status == 'Processing' or x.status == 'Confirmed' or x.status == 'On the way':
            running_orders.append(x)
        else:
            done_orders.append(x)
    content = {
        'running_orders': running_orders,
        'done_orders': done_orders,
    }
    return render(request, 'App_main/My_orders.html', context=content)


def previous_order_search(request):
    all_orders = Order.objects.filter(user=request.user)
    running_orders = []
    for x in all_orders:
        if x.status == 'Processing' or x.status == 'Confirmed' or x.status == 'On the way':
            running_orders.append(x)
    content = {
        'running_orders': running_orders
    }
    thisDays_order = []
    if request.method == 'POST':
        date = request.POST.get('order_date')
        orders = Order.objects.filter(user=request.user)
        for i in orders:
            if str(i.created)[:4] == date[:4] and str(i.created)[5:7] == date[5:7] and str(i.created)[8:10] == date[8:]:
                if i.status == 'Processing' or i.status == 'Confirmed' or i.status == 'On the way':
                    pass
                else:
                    thisDays_order.append(i)
        content['thisDays_orders'] = thisDays_order
    print(thisDays_order)
    return render(request, 'App_main/My_orders.html', context=content)

# def pharmacompany():
#     for i in allPharmaceutical:
#         c = CompanyModel(company_name=i)
#         c.save()
#
#
# def genericPharma():
#     for i in genericNames:
#         g = MedicineGenericModel(medicine_type=i)
#         g.save()
#
#
# def categoriesAdd():
#     for i in categoriesList:
#         cat = CategoryModel(category_name=i)
#         cat.save()
#
#
# def medicineUpload():
#     for i in medicineList[100:1000]:
#         company_name = CompanyModel.objects.get(company_name=i[2])
#         consum = ConsumingType.objects.get(id=random.randint(1, 9))
#         med = MedicineModel(name=i[0], medicine_power=i[1], company=company_name, old_price=i[3], price=i[3],
#                             type_of_consumption=consum)
#         med.save()
#         for j in range(1, 4):
#             category = CategoryModel.objects.get(category_name=random.choice(categoriesList))
#             med.category.add(category)
#

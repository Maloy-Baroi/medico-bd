from django.urls import path
from App_main.views import *

app_name = 'App_main'

urlpatterns = [
    path('', home, name='home'),
    path('home', homeReturn, name='homeReturn'),
    path('single-medicine/<int:pk>/<str:previous>/', single_medicine, name='single-medicine'),
    path('see-all-medicine/', all_medicine, name='see-all-medicine'),
    path('search-medicines', medicine_search, name='search-medicine'),
    path('choose-location/', choose_location, name='choose-location'),
    path('add-locations/', add_locations, name='add-locations'),
    path('add-to-cart/', add_to_cart_view, name='add-to-cart'),
    path('proceed-to-checkout', checkout_view, name='proceed-to-checkout'),
    path('order-place/', order_view, name='order-place'),
    path('my-all-orders/', my_all_orders, name='my-all-orders'),
    path('search-order/', previous_order_search, name='search-order'),
]

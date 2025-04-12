# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  
    path('add_product/', views.add_product, name='add_product'),

    path('product_desc/<pk>', views.product_desc, name='product_desc'),  

    path('add_to_cart/<pk>', views.add_to_cart, name='add_to_cart'),  
    path('add_item/<int:pk>', views.add_item, name='add_item'), 
    path('remove_item/<int:pk>', views.remove_item, name='remove_item'),  
    path('orderlist/', views.orderlist, name='orderlist'),  

    path('checkout/', views.checkout, name='checkout_page'),


    path('simulate_payment/', views.simulate_payment, name='simulate_payment'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('invoice/<int:order_id>/', views.invoice_detail, name='invoice_detail'),

]


from django.urls import path
from . import views

# app_name="store"

urlpatterns=[
    path('', views.store, name="store"),
    path('product/<int:product_id>', views.product_details, name="product_details"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('log_in/', views.log_in, name="log_in"),
    path('logout/', views.log_out, name='logout'),
    path('signup/', views.signup, name='signup'),
]
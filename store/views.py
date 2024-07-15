from django.shortcuts import render
from .models import *

# Create your views here.

def store(request):
    shop1 = Shop.objects.get(name="Shop 1")
    products = Product.objects.filter(shop=shop1)
    for product in products:
        print(product.name, product.price)
    context={"products": products}
    return render(request, 'store/store.html', context)

def cart(request):
    
    context={}
    return render(request, 'store/cart.html', context)

def checkout(request): 
       
    context={}
    return render(request, 'store/checkout.html', context)
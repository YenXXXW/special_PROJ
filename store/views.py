from django.shortcuts import render
from django.http import JsonResponse
from django import forms

import json
import datetime
from .models import *

# Create your views here.

class SelectCategoryForm(forms.Form):
    categories = Category.objects.all()
    category=forms.MultipleChoiceField(
        required=False,
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, **kwargs):
        super(SelectCategoryForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = [(category.id, category.name) for category in Category.objects.all()]
        # if selected_category:
        #     self.fields['category'].initial = [int(selected_category)]
 
# def store(request):
#     if "selected_category" not in request.session:
#         request.session["selected_category"] = "200"
#     products = Product.objects.all()
#     if request.method == "POST":
        
#         selected_category = request.POST.get('category')
#         request.session["selected_category"] = selected_category
#         request.session["selected_category"] 
#         print(selected_category)
#         products = Product.objects.filter(category=selected_category)
#         print(products)
        

#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         items= order.orderitem_set.all()
#         cartItems=order.get_cart_item
#     else:
#         items = []
#         order={'get_cart_total':0, 'get_cart_item':0}
#         cartItems=order['get_cart_item']

#     categories = Category.objects.all()
    
#     form = SelectCategoryForm(initial={'category': [request.session["selected_category"]]})
#     context={'products':products, 'cartItems':cartItems, "categories": categories, "selected_category":request.session["selected_category"], "form":form}
#     return render(request, 'store/store.html', context)       

def store(request):
    selected_category = request.session.get("selected_category", "0")
    
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Process AJAX request
        selected_category = request.POST.get('category')
        request.session["selected_category"] = selected_category
        if selected_category != "0":
            products = Product.objects.filter(category=selected_category)
        else:
            products = Product.objects.all()
        
        # Prepare response data
        products_data = [
            {
                'name': product.name,
                'price': product.price,
                'image_url': product.image.url if product.image else None,  # Get the URL of the image if it exists
            }
            for product in products
        ]
        
        return JsonResponse({'products': products_data})
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0}
        cartItems = order['get_cart_item']

    categories = Category.objects.all()
    
    context = {
        'products': Product.objects.filter(category=selected_category) if selected_category != "0" else Product.objects.all(),
        'cartItems': cartItems,
        'categories': categories,
        'selected_category': selected_category,
    }
    
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items= order.orderitem_set.all()
        cartItems=order.get_cart_item
    else:
        items = []
        order={'get_cart_total':0, 'get_cart_item':0}
        cartItems=order['get_cart_item']

    context={'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request): 
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items= order.orderitem_set.all()
        cartItems=order.get_cart_item
    else:
        items = []
        order={'get_cart_total':0, 'get_cart_item':0}
        cartItems=order['get_cart_item']

    context={'items':items, 'order':order,'cartItems':cartItems}  
    
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId= data['productID']
    action= data['action']
    print('Action:',action)
    print('productId:',productId)
    customer =request.user.customer
    product= Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1) 

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transcation_id =datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total= float(data ['form']['total'])
        order.transactoinId=transcation_id
        if total == order.get_cart_total:
            order.complete=True
        order.save()
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    else:
        print('User is not logged in')

    return JsonResponse('Payment complete', safe=False)
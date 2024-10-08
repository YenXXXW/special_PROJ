from django.shortcuts import render,redirect
from django.http import JsonResponse
from django import forms
import json
import requests
import datetime
from .models import *
from .util import cookieCart, cartData
from django.core import serializers
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse
from django.contrib import messages
from .UserCreationForm import CustomerSignUpForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from django.conf import settings

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
        # if selectAked_category:
        #     selectAked_categoryselectAked_categoryselectAked_category].initial = [int(selected_category)]

def store(request):
    selected_category = request.session.get("selected_category", "0")

    data = cartData(request)
    cartItems = data['cartItems']

    
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Process AJAX request
        selected_category = request.POST.get('category')
        shop_id = request.POST.get('shop_id')
        request.session["selected_category"] = selected_category
        if selected_category != "0" and shop_id == "all":
            products = Product.objects.filter(category=selected_category)
        elif selected_category != "0" and shop_id != "all":
            products = Product.objects.filter(shop=shop_id, category=selected_category)
        elif selected_category == "0" and shop_id == "all":
            products= Product.objects.all()
        else:
            products = Product.objects.filter(shop=shop_id)
        
        def serialize_products(products):
            return [
                {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image_url': product.image.url if product.image else None,
                    'description': product.description,
                    'shop_id': product.shop.id if product.shop else None,
                    'category_id': product.category.id if product.category else None
                }
                for product in products
            ]

        # Prepare response data
        products_data = serialize_products(products)
        
        return JsonResponse({'products': products_data})
    
    shops = Shop.objects.all()
    
    categories = Category.objects.all()
    context = {
        'products': Product.objects.filter(category=selected_category) if selected_category != "0" else Product.objects.all(),
        'cartItems': cartItems,
        'categories': categories,
        'selected_category': selected_category,
        'shop_owner': hasattr(request.user, 'shop'),
        'shops': shops
    }
    
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context={'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request): 
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context={'items':items, 'order':order,'cartItems':cartItems}  
    
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId= data['productID']
    action= data['action']
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

       
    else:
        print('User is not logged in')

        print('COOKIES:',request.COOKIES)
        name = data['form']['name']
        email = data['form']['email']

        cookieData = cookieCart(request)
        items = cookieData['items']
        
        customer, created = Customer.objects.get_or_create(
            email=email,
            )
        customer.name = name
        customer.save()

        order = Order.objects.create(
            customer=customer,
            complete=False,
            )
        for item in items:
            product = Product.objects.get(id=item['product']['id'])

            orderItem = OrderItem.objects.create(
                product=product,
                order=order,
                quantity= item['quantity']
            )
    insufficient_stock_items = []

    # Check if each ordered item has enough stock
    for item in order.orderitem_set.all():
        product = item.product
        if product.quantity < item.quantity:
            insufficient_stock_items.append({
                'product': product.name,
                'available_quantity': product.quantity
            })
            item.quantity = product.quantity
            item.save()
            if product.quantity <= 0:
                item.delete()
           

    # If there are any items with insufficient stock, return them to the frontend
    if insufficient_stock_items:
        return JsonResponse({'error': 'Not enough stock for some items', 'insufficient_items': insufficient_stock_items}, status=400)
    total= float(data ['form']['total'])
    order.transactoinId=transcation_id
    if total == order.get_cart_total:
        order.complete=True
        for item in order.orderitem_set.all():
            product = item.product
            product.quantity -= item.quantity
            product.save()
    order.save()
    ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    
    return JsonResponse('Payment complete', safe=False) 



def product_details(request, product_id):
    data = cartData(request)
    cartItems = data['cartItems']
    product = Product.objects.get(pk=product_id)
    context = {"product": product, 'cartItems':cartItems}
    return render(request, 'store/product_details.html', context)

def log_in(request):
    if request.method == 'POST':
        # Get username and password from the form
        email = request.POST["username"]
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Log the user in
            login(request, user)
            # Redirect to the home page or any other page
            return redirect('store')  # Replace 'home' with your desired URL pattern name
        else:
            # If authentication fails
            messages.error(request, "Invalid username or password")
            return redirect('log_in') 
    else:
        # If it's a GET request, just render the login page
        return render(request, 'store/log_in.html')


def signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('store')  # Redirect to a home page or dashboard after signup
    else:
        form = CustomerSignUpForm()
    return render(request, 'store/signup.html', {'form': form})

def log_out(request):
    logout(request)
   
    return redirect('store')  

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            
            if associated_users.exists():
                # If a user with the email exists, Django will send the email automatically
                form.save(
                    request=request,
                    use_https=True,
                    email_template_name="store/password_reset_email.html",
                    subject_template_name="store/password_reset_subject.txt"
                )
                messages.success(request, 'Password reset link has been sent to your email.')
                
            else:
                messages.error(request, "We can't find an account with that email.")
        else:
            messages.error(request, "Please provide a valid email.")
    else:
        form = PasswordResetForm()
    
    return render(request, 'store/password_reset.html', {'form': form})


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'store/password_reset_confirm.html'
    

    def form_valid(self, form):
        # Add any custom logic here if needed before saving the new password
        return super().form_valid(form)
    

from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django import forms
import json
import datetime
from .models import *
from .util import cookieCart, cartData
from django.core import serializers
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse
from .UserCreationForm import CustomerSignUpForm

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

    data = cartData(request)
    cartItems = data['cartItems']

    print(f"cartItsminStoreAbove{cartItems}")
    
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
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'image_url': product.image.url if product.image else None,  # Get the URL of the image if it exists
                'description': product.description
            }
            for product in products
        ]
        
        return JsonResponse({'products': products_data})
    
    categories = Category.objects.all()
    print(f"cartItsminStore{cartItems}")
    context = {
        'products': Product.objects.filter(category=selected_category) if selected_category != "0" else Product.objects.all(),
        'cartItems': cartItems,
        'categories': categories,
        'selected_category': selected_category,
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
    
    return JsonResponse('Payment complete', safe=False) 


def product_details(request, product_id):
    data = cartData(request)
    cartItems = data['cartItems']
    product = Product.objects.get(pk=product_id)
    context = {"product": product, 'cartItems':cartItems}
    return render(request, 'store/product_details.html', context)

def shop_admin_panel(request):
    return render(request, 'store/shop_admin.html')

def shop_admin_data(request):
    products = Product.objects.all()
    products_data = [
        {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'image_url': product.image.url if product.image else None,  # Get the URL of the image if it exists
            'description': product.description
        }
        for product in products
    ]

    return JsonResponse({'products': products_data})



@require_POST
def get_product_by_Id(request):
    if request.body:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)


    else:
        return JsonResponse({'error': 'Empty request body'}, status=400)
    if 'productId' not in data:
        return JsonResponse({'error': 'ID is required'}, status=400)

    # Process the data if the ID is present
    id_value = data['productId']
    
    product = Product.objects.filter(id = id_value).first()

    if not product:
        return JsonResponse({'error': "product with the given Id doesnot exist"}, status = 400)
    
    
    product_data = {
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'description': product.description,
        'image_url': product.imageURL
        # Add other fields as necessary
    }
    return JsonResponse({'product': product_data})
    

@require_POST
def shop_admin_panel_edit_product(request):
    try:
        id = request.POST.get("id")
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        if not all([name, price, id, description ]):
            return JsonResponse({"error": "The required fields are not present"}, status=400)
        product = Product.objects.filter(id=id).first()
        if not product:
            return JsonResponse({'error': "product does not exist"}, status=404)
        product.name = name
        product.description = description
        try:
            product.price =  int(price)
        except ValueError:
            return JsonResponse({"error": "Price must be the interger type"}, status=400)
            
        if image:
            if image.size > 5 * 1024 * 1024:
                return JsonResponse({"error": "The image size should not exceed 5mb"}, status=400)
            product.image = image

        product.save()

    except:
        return JsonResponse({"error"})        
    return JsonResponse({"message": "product updated successfully"},status=200)
    

def addProduct(request): 
    pass
def log_in(request):
    if request.method == 'POST':
        # Get username and password from the form
        username = request.POST["username"]
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Log the user in
            login(request, user)
            # Redirect to the home page or any other page
            return redirect('store')  # Replace 'home' with your desired URL pattern name
        else:
            # If authentication fails
            return redirect('log_in')
    else:
        # If it's a GET request, just render the login page
        return render(request, 'store/log_in.html')


def signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('store')  # Redirect to a home page or dashboard after signup
    else:
        form = CustomerSignUpForm()
    return render(request, 'store/signup.html', {'form': form})

def log_out(request):
    logout(request)
   
    return redirect('store')  


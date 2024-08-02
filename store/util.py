import json
from .models import *
from django.http import JsonResponse

def cookieCart(request):  
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}   

    print('Cart:',cart) 
    items = []
    order = {'get_cart_total':0, 'get_cart_item':0, }
    cartItems = order['get_cart_item']
        
    for  i in cart:
        try:
            cartItems += cart[i]["quantity"]
                
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])
             
            order['get_cart_total'] += total
            order['get_cart_item'] += cart[i]["quantity"]

            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                    },
                'quantity':cart[i]["quantity"],
                'get_total':total
                }
            item.append(item)
        except:
            pass
    return {'cartItems':cartItems, 'order':order, 'items':items }

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items= order.orderitem_set.all()
        cartItems=order.get_cart_item
    else: 
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems':cartItems, 'order':order, 'items':items}
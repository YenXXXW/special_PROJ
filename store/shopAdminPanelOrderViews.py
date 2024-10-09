from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from .models import *

def getOrders(request):
    if not hasattr(request.user, 'shop'):
        return redirect('store')
    shop = request.user.shop
    shopOrders= ShopOrder.objects.filter(shop=shop)
    order_data = [
        {
            'id': shopOrder.id,
            'customer_name': shopOrder.order.customer.name,
            'customer_email': shopOrder.order.customer.email,
            'completed': shopOrder.order.complete,
            'date_ordered': shopOrder.order.date_ordered,
            'products': [
                {
                    'product_name': item.product.name if item.product else 'No product',
                    'quantity': item.quantity,
                    'total_price': item.get_total
                }
                for item in shopOrder.order.orderitem_set.all()
            ],
            'shipping_address': {
            'address': shipping_address.address,
            'city': shipping_address.city,
            'state': shipping_address.state,
            'zipcode': shipping_address.zipcode,
            } if (shipping_address := ShippingAddress.objects.filter(order=shopOrder.order).first()) else 'No shipping address' 
        }
        for shopOrder in shopOrders
    ]
    context = {
        "order_data": order_data  
    }
    return render(request, 'store/adminPanel/viewOrders.html', context)




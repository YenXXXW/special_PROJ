from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from .models import *

@require_POST
def getOrders(request):
    shop = request.user.shop
    if not hasattr(request.user, 'shop'):
        return redirect('store')
    orders = Order.objects.all()
    print(orders)
    if orders.exists():
        for order in orders:
            print(order.customer.name)

        order_data = [
            {
                'id': order.id,
                'customer_id': order.customer.id,
                'date_ordered': order.date_ordered,
                'completed': order.complete,
                'date_ordered': order.date_ordered
            }
            for order in orders
        ] 
        return render 
    return JsonResponse({"message": "no orders"})



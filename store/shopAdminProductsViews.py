from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import *
import json

def shop_admin_panel(request):
    if not hasattr(request.user, 'shop'):
        return redirect('store')
    return redirect('get-products')

def getAllProducts(request):
    if not hasattr(request.user, 'shop'):
        return redirect('store')
    shop = request.user.shop
    products = Product.objects.filter(shop=shop)
    if not shop:
        return JsonResponse({"error": "shop not found"})
    context = {
        'products': [
            {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'image_url': product.image.url if product.image else None,  # Get the URL of the image if it exists
                'description': product.description
            }
            for product in products
        ]
    }

    return render(request, 'store/adminPanel/viewProducts.html', context)



@require_POST
def get_product_by_Id(request):
    if not hasattr(request.user, 'shop'):
        return redirect('store')
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
    

def edit_product(request, product_id):
    if not hasattr(request.user, 'shop'):
        return redirect('store')
    if request.method == "POST":
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
    
    product = Product.objects.get(pk=product_id)
    print(product.name, product.price, product.id)
    context = {'product': product}
    if not product:
        return JsonResponse({"error": "product not found"}, status=404)
    return render(request, "store/adminPanel/editProduct.html", context)

def addProduct(request): 

    if request.method == "POST":
        shop = request.user.shop
        if not shop:
            return JsonResponse({"error": "Shop does not exist"}, status=400)

        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        category_name = request.POST.get("category")
        brand =  request.POST.get("brand")
        color= request.POST.get('color')
        if not all([name, price,  description, image , category_name, brand, color]):
            return JsonResponse({"error": "The required fields are not present"}, status=400)
        try:
            price =  int(price)
        except ValueError:
            return JsonResponse({"error": "Price must be the interger type"}, status=400)
            
        if image:
            if image.size > 5 * 1024 * 1024:
                return JsonResponse({"error": "The image size should not exceed 5mb"}, status=400)
            
        category  = Category.objects.filter(name=category_name).first()
        product = Product(
            name=name,
            description = description,
            price=price,
            shop=shop,
            category=category,
            brand= brand,
            color= color,
            image=image
        )
        product.save()
        return JsonResponse({"message": "The product is added"})


    categories = Category.objects.all()
    category_list = [{"id": category.id, "name": category.name} for category in categories]
    context = {
        'categories': category_list
    }
    return render(request, 'store/adminPanel/addProduct.html', context)
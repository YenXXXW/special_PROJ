from django.db import models
from django.contrib.auth .models import User

# Create your models here.
class Customer(models.Model):
  user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
  name = models.CharField(max_length=200, null=True)
  email = models.CharField(max_length=200, null=True)

  def __str__(self):
    # This is what appears in the Admin panel
    return self.name
  

class Shop(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    # Other fields as needed

    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=255)
    shops = models.ManyToManyField('Shop', related_name='categories')
    # Other fields as needed

    def __str__(self):
        return self.name


class Product(models.Model):
  name = models.CharField(max_length=200, null=True)
  price=models.FloatField()
  shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')
  category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
  quantity = models.IntegerField(default=0)
  image = models.ImageField(null=True, blank=True)

  def __str__(self):
    return self.name
  
  @property
  def imageUrl(self):
    try:
      url = self.image.url
    except:
      url = ''
    return url
    
  
class Cart (models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
  # date_ordered = models.DateTimeField(auto_now_add=True)
  transactoinId = models.CharField(max_length=200, null=True)

  def __str__(self):
    return str(self.id)


class CartItem(models.Model):
  product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
  cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, blank=True, null=True)
  quantity = models.IntegerField(default=0, null=True, blank=True)


class ShippingAddress(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
  cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, blank=True, null=True)
  address = models.CharField(max_length=200, null=True)
  city = models.CharField(max_length=200, null=True)
  state = models.CharField(max_length=200, null=True)
  zipcode = models.CharField(max_length=200, null=True)


  def __str__(self):
    return self.address
   


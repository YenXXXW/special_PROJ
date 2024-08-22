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

  HIGH = 'high'
  MEDIUM = 'medium'
  LOW = 'low'
    
  QUALITY_CHOICES = [
      (HIGH, 'High'),
      (MEDIUM, 'Medium'),
      (LOW, 'Low'),
  ]
  
  name = models.CharField(max_length=200, null=True)
  price = models.IntegerField(default=10000)
  shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')
  category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
  description = models.CharField(max_length=1000, null=True)
  quantity = models.IntegerField(default=0)
  image = models.ImageField(null=True, blank=True)
  quality = models.CharField(max_length=6, choices=QUALITY_CHOICES, default=MEDIUM)
  color = models.CharField(max_length=50, null=True)
  brand = models.CharField(max_length=50, null=True)
  weight = models.DecimalField(max_digits=5,  decimal_places=2, default=10)

  def __str__(self):
    return self.name
  
  @property
  def imageURL(self):
    try:
      url = self.image.url
    except:
      url = ''
    return url

  
class Order (models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
  date_ordered = models.DateTimeField(auto_now_add=True)
  transactoinId = models.CharField(max_length=200, null=True)
  complete = models.BooleanField(default=False, null=True, blank=False)

  @property
  def get_cart_total(self):
     orderitems = self.orderitem_set.all()
     total = sum([item.get_total for item in orderitems])
     return total
  
  @property
  def get_cart_item(self):
     orderitems = self.orderitem_set.all()
     total = sum([item.quantity for item in orderitems])
     return total

  def __str__(self):
    return str(self.id)


class OrderItem(models.Model):
  product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
  quantity = models.IntegerField(default=0, null=True, blank=True)
  date_added = models.DateTimeField(auto_now_add=True)

  @property
  def get_total(self):
      if self.product:
          total = self.product.price * self.quantity
      else:
          total = 0
      return total



class ShippingAddress(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
  address = models.CharField(max_length=200, null=True)
  city = models.CharField(max_length=200, null=True)
  state = models.CharField(max_length=200, null=True)
  zipcode = models.CharField(max_length=200, null=True)

  def _str_(self):
    return str(self.address)
   


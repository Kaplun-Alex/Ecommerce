from email.mime import image
from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user =  models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=254, null=True)
    email = models.CharField(max_length=254)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    customer =
    date_ordered =
    complete = 
    transaction_id =
    

class ShippingAdress(models.Model):
    customer = 
    order = 
    adress =
    city =
    state =
    country =
    zipcode = 
    date_added =

    
class OrderItem(models.Model):
    product = 
    order =
    qantyty =
    date_added =
    

class Product(models.Model):

    name = 
    price = 
    digital = 
    image =
    


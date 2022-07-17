from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):

    '''Customer ORM class'''

    user =  models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):

    '''Product ORM class'''

    name = models.CharField(max_length=255, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    #image

    def __str__(self):
        return self.name

class Order(models.Model):

    '''Order ORM class'''

    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=127, null=True)

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):

    '''OrderItem ORM class'''

    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    qantyty = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

class ShippingAdress(models.Model):

    '''ShippingAdress ORM class'''

    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    adress = models.CharField(max_length=255, null=True )
    city = models.CharField(max_length=255, null=True )
    state = models.CharField(max_length=255, null=True )
    country = models.CharField(max_length=255, null=True )
    zipcode = models.CharField(max_length=255, null=True )
    date_added = date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.adress

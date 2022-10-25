from tokenize import blank_re
from django.db import models
from django.contrib.auth.models import User


class Nauser(models.Model):
    csrfName = models.CharField(max_length=255, null=True)
    shortName = models.CharField(max_length=4, null=True)
    date_created = models.DateTimeField(auto_now_add=True)


class Customer(models.Model):

    '''Customer ORM class'''

    user =  models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# class Anonimouscustomer(models.Model):
#     '''Anonimous customer ORM clas'''
#     aUser = models.CharField(max_lenght=255, null=True)

class Product(models.Model):

    '''Product ORM class'''

    name = models.CharField(max_length=255, null=True)
    number_of_pieces = models.IntegerField(null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):

        '''!'''
        try:
            url = self.image.url

        except:
            url = "static/images/no-image.png"

        return url

class Order(models.Model):

    '''Order ORM class'''

    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    nacustomer = models.ForeignKey(Nauser, null=True, blank=True, on_delete=models.SET_NULL)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=127, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):

        '''check cart digital products'''
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital is False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):

        '''get cart total'''
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total


    @property
    def get_cart_items(self):

        '''get cart items'''

        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):

    '''OrderItem ORM class'''

    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


    @property
    def get_total(self):

        '''get cart total items'''
        total = self.product.price * self.quantity
        return total


class ShippingAdress(models.Model):

    '''ShippingAdress ORM class'''

    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    nacustomer = models.ForeignKey(Nauser, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    adress = models.CharField(max_length=255, null=True )
    city = models.CharField(max_length=255, null=True )
    state = models.CharField(max_length=255, null=True )
    country = models.CharField(max_length=255, null=True )
    zipcode = models.CharField(max_length=255, null=True )
    date_added = date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.adress

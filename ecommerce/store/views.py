'''wiews.py module'''

import json
from django.shortcuts import render
from .models import Product
from  .models import Order
from django.http import JsonResponse



def store(request):

    '''Store hrml rendering'''

    products = Product.objects.all()
    context ={'products': products }
    return render(request, "store/store.html", context)


def cart(request):

    '''Cart hrml rendering'''

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {"get_cart_items":0, "get_cart_total":0}
    context ={"items":items, "order":order}
    return render(request, "store/cart.html", context)


def checkout(request):

    '''Checkout hrml rendering'''
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {"get_cart_items":0, "get_cart_total":0}
    context ={"items":items, "order":order}
    return render(request, "store/checkout.html", context)


def updateItem(request):

    '''Updating items in cart'''
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    return JsonResponse('Item was added', safe=False)
    
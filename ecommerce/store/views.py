from itertools import product
import json
from django.shortcuts import render
from .models import OrderItem, Product
from  .models import Order
from django.http import JsonResponse
from .utils import cookieCart, cartData


def store(request):

    '''Store html rendering'''
    data = cartData(request)
    cartItems = data["cartItems"]

    products = Product.objects.all()
    context ={'products': products, 'cartItems':cartItems }
    return render(request, "store/store.html", context)


def cart(request):

    '''Cart html rendering'''
    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {"items":items, "order":order, 'cartItems':cartItems}
    return render(request, "store/cart.html", context)


def checkout(request):

    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {"items":items, "order":order, 'cartItems':cartItems}
    return render(request, "store/checkout.html", context)


def updateItem(request):

    '''Updating items in cart'''

    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product  = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
    
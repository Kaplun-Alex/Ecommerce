from itertools import product
import json
from django.shortcuts import render
from .models import OrderItem, Product
from  .models import Order, Nauser
from django.http import JsonResponse
from .utils import cookieCart, cartData, requestViewer, nauserfinder



def store(request):

    '''Store html rendering'''
    data = cartData(request)
    cartItems = data["cartItems"]

    products = Product.objects.all()
    context ={'products': products, 'cartItems':cartItems }
    return render(request, "store/store.html", context)


def cart(request):
#    for i in request.META.items():
#        print(i)

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

    '''Updating items in cart for Registered user'''

    print(request.META['HTTP_X_CSRFTOKEN'])

    if request.user.is_authenticated == False:
        anonimouseCustomerKey = request.META['HTTP_X_CSRFTOKEN']
        usercsrfid = nauserfinder(anonimouseCustomerKey)
        print("Print in vievs", usercsrfid, "Type of return obj", type(usercsrfid))
        if usercsrfid == 0:
            print("usercsrfid - ", usercsrfid)
            nev_nouser = Nauser(csrfName=anonimouseCustomerKey, shortName = anonimouseCustomerKey[:4])
            nev_nouser.save()
      
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        print('DATA:', data)
        print('Action:', action)
        print('Product:', productId)

        nacustomer = Nauser.objects.get(id=usercsrfid)
        print(nacustomer.id, nacustomer.csrfName)
        
        product  = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(nacustomer=nacustomer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity = (orderItem.quantity +1)
            print('item added')
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity -1)
            print('Item remowe')

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

    else:    

        '''Updating items in cart for Registered user'''
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

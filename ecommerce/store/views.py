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

    requestInfo = requestViewer(request)

    #print(requestInfo)
    print(type(request))

    if request.user.is_authenticated == False:
        print('User is not authenticated')
        anonimouseCustomerKey = request.META['HTTP_X_CSRFTOKEN']
        print('ANUserKey:', anonimouseCustomerKey)
        print(abs(hash(anonimouseCustomerKey)), 'Type of hash', type(hash(anonimouseCustomerKey)))
        usercsrfid = nauserfinder(anonimouseCustomerKey)
        print(usercsrfid)
        
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        print('DATA:', data)
        print('Action:', action)
        print('Product:', productId)

        nacustomer = Nauser(csrfName=anonimouseCustomerKey)
        #nacustomer.save()
        product  = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(nacustomer=nacustomer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            print('item added')
        elif action == 'remove':
            print('Item remowe')

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

import json
from .models import *
import requests

def cookieCart(request):

    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart ={}
        print('Cart:', cart)
    items = []
    order = {"get_cart_total":0, "get_cart_items":0, "shipping": False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                    },
                'quantity':cart[i]["quantity"],
                'get_total':total,
                }
            items.append(item)
            if product.digital == False:
                order["shipping"] = True
        except:
            pass
    return {"items":items, "order":order, "cartItems":cartItems}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData["cartItems"]
        order = cookieData["order"]
        items = cookieData["items"]
    return {"items":items, "order":order, "cartItems":cartItems}

def requestViewer(request):

    '''Request info viewer'''

    headers = ''
    #print(request.META)
    #print(request.META['HTTP_X_CSRFTOKEN'])
    
    for header, value in request.META.items():
        if not header.startswith('HTTP'):
            continue
        header = '-'.join([h.capitalize() for h in header[5:].lower().split('_')])
        headers += '{}: {}\n'.format(header, value)
    return (
        '{method} HTTP/1.1\n'
        'Content-Length: {content_length}\n'
        'Content-Type: {content_type}\n'
        '{headers}\n\n'
        '{body}'
    ).format(
        method=request.method,
        content_length=request.META['CONTENT_LENGTH'],
        content_type=request.META['CONTENT_TYPE'],
        headers=headers,
        body=request.body,
    )
    
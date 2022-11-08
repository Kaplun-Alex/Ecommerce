
from xmlrpc.client import Boolean
from .models import *


__all__ = [
    "cartData",
    "requestViever",
    "nauserFinder", 
    "nauserCreator",
    "csrfCheck",
    "csrfBaseCheck",
]

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items   
    else:
        nauserfinder(request.META['CSRF_COOKIE'])
        

    if request.META['CSRF_COOKIE']:
        print('in csrf_coocie_exist')
        customer = Nauser.objects.get(id=nauserfinder(request.META['CSRF_COOKIE']))
        print(customer.id, customer.shortName)
        order, created = Order.objects.get_or_create(nacustomer=customer, complete=False)
        print(order)
        items = order.orderitem_set.all()
        print(items)
        cartItems = order.get_cart_items
        print(cartItems)

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

def nauserfinder(nauserCSRF):
    shortCsrf = nauserCSRF[:4]
    print("!!!!!!", nauserCSRF, shortCsrf)
    if Nauser.objects.filter(shortName=shortCsrf):
        print('User exist')
    else:
        print('No user')
    
    if not res:
        return int(0)
    if len(res) == 1:
        print(res[0].id)
        return res[0].id
    if len(res) > 1:
        return ((res.order_by("date_created")).last()).id

def csrfCheck(csrfData):
    try:
        if csrfData.META["CSRF_COOKIE"]:
            print("True")
            return True
        else:
            print("False")
            return False
    except KeyError:
        return False

def csrfBaseCheck(csrfData):
    data = (csrfData.META["CSRF_COOKIE"])[:4]
    if Nauser.objects.filter(shortName=data):
        print("Schort name is find")
        return True
    else:
        print("csrf not in base")
        return False

    
def nausercreator(nauserCSRF):
    nacustomer = Nauser(csrfName=nauserCSRF)
    #nacustomer.save()
    
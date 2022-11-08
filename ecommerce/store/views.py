from itertools import product
import json
from django.shortcuts import render
from .models import OrderItem, Product
from  .models import Order, Nauser
from django.http import JsonResponse
from .utils import cartData, requestViewer, nauserfinder, csrfCheck, csrfBaseCheck
from django.http import HttpResponseNotFound, HttpResponse
from django.views import View



__all__ = [
    "StoreView", 
    "Cartview",
    "CheckoutView",
    "UpdateItemsView"
]

class StoreView(View):

    def get(self, request):
        if request.user.is_authenticated == False:
            proof = csrfCheck(request)
            if proof:
                print("!!!is csrf!!!")
                if csrfBaseCheck(request):
                    print("Csrf in base")
                else:
                    print("user not in base")
                    products = Product.objects.all()
                    cartItems = 0
                    context ={'products': products, 'cartItems':cartItems} 
            else:
                print("!!!csrf_error!!!")
                return HttpResponse("For you service is closed")
        else:
            print("User is auth", request.user.customer)
            products = Product.objects.all()
            cartItems = 0
            context ={'products': products, 'cartItems':cartItems}

        return render(request, "store/store.html", context)        


class CartView(View):
    def get(self, request):

        '''Cart html rendering'''
        data = cartData(request)
        cartItems = data["cartItems"]
        order = data["order"]
        items = data["items"]

        context = {"items":items, "order":order, 'cartItems':cartItems}
        return render(request, "store/cart.html", context)

class CheckoutView(View):
    def get(self, request):

        data = cartData(request)
        cartItems = data["cartItems"]
        order = data["order"]
        items = data["items"]

        context = {"items":items, "order":order, 'cartItems':cartItems}
        return render(request, "store/checkout.html", context)

class UpdateItemsView(View):
    def put(request):

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

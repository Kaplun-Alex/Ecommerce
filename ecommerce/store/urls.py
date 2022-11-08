from django.urls import path
from . import views
from .views import StoreView, CartView, CheckoutView, UpdateItemsView 


urlpatterns = [
    path("", StoreView.as_view(), name="store"),
    path("cart/", CartView.as_view(), name="cart"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('update_item/', UpdateItemsView.as_view(), name="update_item"),
]

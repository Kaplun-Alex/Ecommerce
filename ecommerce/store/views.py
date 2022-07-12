from django.shortcuts import render


def store(request):
    context ={}
    return render(request, "store/store.html", context)


def cart(request):
    context ={}
    return render(request, "store/cart.html", context)


def checkout(request):
    context ={}
    return render(request, "store/chekout.html", context)

# Create your views here.

from django.shortcuts import render

# Create your views here.


def home(request):
    if request.method == "GET":
        return render(request, 'src/home.html', context={})


def menu(request):
    if request.method == "GET":
        return render(request, 'src/menu.html', context={})


def checkout(request):
    if request.method == "GET":
        return render(request, 'src/checkout.html', context={})


def cart(request):
    if request.method == "GET":
        return render(request, 'src/cart.html', context={})


def staff(request):
    if request.method == "GET":
        return render(request, 'src/staff.html', context={})

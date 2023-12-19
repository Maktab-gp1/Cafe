from django.shortcuts import render

# Create your views here.


def home(request):
    if request.method == "GET":
        return render(request, 'src/index.html', context={})


def menu(request):
    if request.method == "GET":
        return render(request, 'src/menu1.html', context={})


def checkout(request):
    if request.method == "GET":
        return render(request, 'src/checkout.html', context={})


def cart(request):
    if request.method == "GET":
        return render(request, 'src/cart.html', context={})


def about(request):
    if request.method == "GET":
        return render(request, 'src/about.html', context={})


def staff(request):
    if request.method == "GET":
        return render(request, 'src/team.html', context={})

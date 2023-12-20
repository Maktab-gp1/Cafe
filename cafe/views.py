from django.shortcuts import render
from django.views import View
from .forms import ReservationCreation
from .models import Menu, Reservation, Storage, Account
# Create your views here.


def home(request):
    if request.method == "GET":
        return render(request, 'src/index.html', context={})


def menu(request):
    if request.method == "GET":
        foods = Menu.objects.all()
        return render(request, 'src/menu1.html', context={"foods": foods})


def checkout(request):
    if request.method == "GET":
        use = Account.objects.create(name='gust', phone='09101212121')
        Account.save(use)
        foods = Reservation.objects.all()
        acc_id = Reservation.account_id
        # acc_id.name
        # print(acc_id.name)
        request.session["user"] = 'gust'
        return render(request, 'src/checkout.html', context={"reserv": foods})


def cart(request):
    if request.method == "GET":
        print(request.session['user'])
        if 'user' in request.session:
            foods = Reservation.objects.all()
        return render(request, 'src/cart.html', context={"foods": foods})


def about(request):
    if request.method == "GET":
        return render(request, 'src/about.html', context={})


def service(request):
    if request.method == "GET":
        return render(request, 'src/service.html', context={})


def staff(request):
    if request.method == "GET":
        reserves = Reservation.objects.all()
        storage = Storage.objects.filter(remined_material__lte=10)
        return render(request, 'src/staff.html', context={"reserves": reserves, "storage": storage})


def testimonial(request):
    if request.method == "GET":
        return render(request, 'src/testimonial.html', context={})


# def booking(request):
#     if request.method == "GET":
#         return render(request, 'src/booking.html', context={})

class booking(View):
    def get(self, request):
        form = ReservationCreation()
        return render(request, 'src/booking.html', {"form": form})

    def post(self, request, slug):
        return render(request, 'src/booking.html', {})

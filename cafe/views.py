from django.shortcuts import render
from django.views import View
from .forms import ReservationCreation
from .models import Menu, Reservation, Storage, Account, Tables
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
# Create your views here.


def home(request):
    if request.method == "GET":
        return render(request, 'src/index.html', context={})
    # if request.method == "POST":
    #     search = request.POST.get('form1')
    #     print("*********************")
    #     print(search)
    #     return render(request, 'src/index.html', context={})


def menu(request):
    if request.method == "GET":
        # request.session.clear()
        all = Menu.objects.all()
        foods = Menu.objects.filter(category='lunch')
        foods_d = Menu.objects.filter(category='dinner')
        for food in all:
            request.session[food.title] = 0
        return render(request, 'src/menu1.html', context={"foods": foods, 'foods_d': foods_d})
    if request.method == "POST":
        count = {}
        # foods = Menu.objects.all()
        foods = Menu.objects.all()
        search = request.POST.get('search')
        for food in foods:
            counter = request.POST.get(food.title)
            # price = food.price
            if counter is not None:
                request.session[food.title] = counter
                count[food.title] = counter
                # request.session[f"{food.title}_price"] = price * int(counter)
            else:
                if int(request.session[food.title]) > 0:
                    pass
                else:
                    request.session[food.title] = 0
            if request.session[food.title] == 0:
                del request.session[food.title]
            print("*********************")
            print(food.title)
            # print(request.session[f"{food.title}_price"])
            print(request.session[food.title])
            print(count)
        # print(data)
        if search is not None:
            foods = Menu.objects.filter(title__icontains=search)
        return render(request, 'src/menu1.html', context={"foods": foods, 'count': count})


def checkout(request):
    if request.method == "GET":
        names = []
        totall_price = 0
        foods = Menu.objects.all()
        for food in foods:
            # if request.session[food.title] == '0':
            #     del request.session[food.title]
            if request.session[food.title] != '0':
                totall_price += int(food.price) * \
                    int(request.session[food.title])
                # print(request.session[f"{food.title}_price"])
                names.append(food.title)
        reserv = Menu.objects.filter(title__in=names)
        return render(request, 'src/checkout.html', context={"reserv": reserv, 'price': totall_price})


def cart(request):
    if request.method == "GET":
        print(request.session.items())
        names = []
        totall_price = 0
        foods = Menu.objects.all()
        for food in foods:
            # if request.session[food.title] == '0':
            #     del request.session[food.title]
            if request.session[food.title] != '0':
                totall_price += int(food.price) * \
                    int(request.session[food.title])
                # print(request.session[f"{food.title}_price"])
                names.append(food.title)
        reserv = Menu.objects.filter(title__in=names)
        # account = Account(name='guest')
        # account.save()
        # table = Tables(pk=1)
        # table.save()
        # reserving = Reservation.objects.create(
        #     account_id=account, table=table, reserved_time=datetime.now(), created_at=datetime.now())
        # reserving.save()
        # for i in reserv:
        #     reserving.menu.add(i)
        #     reserving.save()
        return render(request, 'src/cart.html', context={"foods": reserv, 'price': totall_price})


def about(request):
    if request.method == "GET":
        return render(request, 'src/about.html', context={})


def service(request):
    if request.method == "GET":
        return render(request, 'src/service.html', context={})


@login_required
def staff(request):
    if request.method == "GET":
        reserves = Reservation.objects.all()
        storage = Storage.objects.filter(remined_material__lte=10)
        return render(request, 'src/staff.html', context={"reserves": reserves, "storage": storage})


def testimonial(request):
    if request.method == "GET":
        return render(request, 'src/testimonial.html', context={})


def contact(request):
    if request.method == "GET":
        return render(request, 'src/contact.html', context={})

# def booking(request):
#     if request.method == "GET":
#         return render(request, 'src/booking.html', context={})


class booking(View):
    def get(self, request):
        form = ReservationCreation()
        return render(request, 'src/booking.html', {"form": form})

    def post(self, request, slug):
        return render(request, 'src/booking.html', {})

from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReservationCreation
from .models import Menu, Reservation, Storage, Account, Tables
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
# Create your views here.


def home(request):
    if request.method == "GET":
        return render(request, 'src/index.html', context={})
   


def menu(request):
    if request.method == "GET":
        all = Menu.objects.all()
        foods = Menu.objects.filter(category='lunch')
        foods_d = Menu.objects.filter(category='dinner')
        for food in all:
            request.session[food.title] = 0
        return render(request, 'src/menu1.html', context={"foods": foods, 'foods_d': foods_d})
    if request.method == "POST":
        count = {}
        foods = Menu.objects.all()
        search = request.POST.get('search')
        for food in foods:
            counter = request.POST.get(food.title)
            if counter is not None:
                request.session[food.title] = counter
                count[food.title] = counter
            else:
                if int(request.session[food.title]) > 0:
                    pass
                else:
                    request.session[food.title] = 0
            if request.session[food.title] == 0:
                del request.session[food.title]
        if search is not None:
            foods = Menu.objects.filter(title__icontains=search)
        return render(request, 'src/menu1.html', context={"foods": foods, 'count': count})


def checkout(request):
    if request.method == "GET":
        names = []
        totall_price = 0
        foods = Menu.objects.all()
        for food in foods:
        
            if request.session[food.title] != '0':
                totall_price += int(food.price) * int(request.session[food.title])
                names.append(food.title)
        reserv = Menu.objects.filter(title__in=names)
        return render(request, 'src/checkout.html', context={"reserv": reserv, 'price': totall_price})


def cart(request):
    if request.method == "GET":
        names = []
        totall_price = 0
        foods = Menu.objects.all()
        for food in foods:
            if request.session[food.title] != '0':
                totall_price += int(food.price) * \
                    int(request.session[food.title])
                names.append(food.title)
        reserv = Menu.objects.filter(title__in=names)
        return render(request, 'src/cart.html', context={"foods": reserv, 'price': totall_price})


def about(request):
    if request.method == "GET":
        return render(request, 'src/about.html', context={})


def service(request):
    if request.method == "GET":
        return render(request, 'src/service.html', context={})

class StaffPanel(ListView,LoginRequiredMixin):
    model = Reservation
    template_name = 'src/staff.html'
    def get_queryset(self, *args, **kwargs): 
        qs = super(StaffPanel, self).get_queryset(*args, **kwargs) 
        qs = qs.order_by("-id").reverse() 
        return qs

def testimonial(request):
    if request.method == "GET":
        return render(request, 'src/testimonial.html', context={})

def contact(request):
    if request.method == "GET":
        return render(request, 'src/contact.html', context={})

class booking(View):
    def get(self, request):
        form = ReservationCreation()
        return render(request, 'src/booking.html', {"form": form})

    def post(self, request, slug):
        return render(request, 'src/booking.html', {})



    
class Confirm(View,LoginRequiredMixin):
    def post(self,request):
        print(request.POST)
        reserv = get_object_or_404(Reservation,id=request.POST['id'])
        if reserv.is_confirmed :
            reserv.is_confirmed = False
            reserv.save()
        else :
            reserv.is_confirmed = True
            reserv.save()
        return redirect(reverse("staff"))

        
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

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


# # @login_required
# # def staff(request):
# #     if request.method == "GET":
# #         reserves = Reservation.objects.all()
# #         storage = Storage.objects.filter(remined_material__lte=10)
# #         return render(request, 'src/staff.html', context={"reserves": reserves, "storage": storage})

# class StaffPanel(ListView,LoginRequiredMixin):
#     model = Reservation
#     template_name = 'src/staff.html'
#     def get_queryset(self, *args, **kwargs): 
#         qs = super(StaffPanel, self).get_queryset(*args, **kwargs) 
#         qs = qs.order_by("-id").reverse() 
#         return qs


def testimonial(request):
    if request.method == "GET":
        return render(request, 'src/testimonial.html', context={})


# # def booking(request):
# #     if request.method == "GET":
# #         return render(request, 'src/booking.html', context={})

# class booking(View):
#     def get(self, request):
#         form = ReservationCreation()
#         return render(request, 'src/booking.html', {"form": form})

#     def post(self, request, slug):
#         return render(request, 'src/booking.html', {})



    
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





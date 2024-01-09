from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import UpdateView, CreateView, FormView
from django.views.generic import ListView
from django.http import Http404
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import Order, OrderItem
from shop.models import Category, Product
from .forms import OrderItemStaffFormSet, StatusForm, StatusFormSet


class StaffPanel(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'staff/dashboard.html'
    form_class = StatusFormSet
    login_url = reverse_lazy('login')

    def get_queryset(self, *args, **kwargs):
        if self.request.GET.get('search'):
            filter = self.request.GET['search']
            return Order.objects.filter(
                Q(phone__icontains=filter) |
                Q(created__icontains=filter) |
                Q(status__icontains=filter))
        return Order.objects.all()

    def get_status_initial(self):
        orders = Order.objects.all()
        initial = [{'status': order.status} for order in orders]
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        context["categories"] = Category.objects.all()
        formset = StatusFormSet(initial=self.get_status_initial())
        context["status"] = formset
        print(context)
        return context

    def post(self, request):
        formset = StatusFormSet(self.request.POST)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    StatusFormSet = get_object_or_404(
                        StatusFormSet, id=StatusFormSet_id)
                    StatusFormSet_id = form.cleaned_data.get('id')
                    StatusFormSet.status = form.cleaned_data['status']
                    StatusFormSet.save()


class OrderFieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = [
                "phone",
                "table"
                "product",
                "price",
                "quantity",

            ]
        else:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class OrderItemFormValidMixin():
    def form_valid(self, form):
        context = self.get_context_data()
        order_item_staff_formset = context['order_item_staff_formset']
        if self.request.user.is_staff:
            self.obj = form.save()
            if order_item_staff_formset.is_valid():
                order_item_staff_formset.instance = self.obj
                order_item_staff_formset.save()
            return redirect('dashboard')
        else:
            self.obj = form.save(commit=False)
            self.obj.available = False
        return super().form_valid(form)


class OrderStaffUpdate(LoginRequiredMixin, UpdateView, OrderFieldsMixin, OrderItemFormValidMixin):
    login_url = reverse_lazy('login')
    model = Order
    fields = '__all__'
    template_name = 'staff/dashboard1.html'
    success_url = reverse_lazy('staff/dashboard')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            form = OrderItemStaffFormSet(
                self.request.POST, instance=self.object)
            data['order_item_staff_formset'] = form
            form.save()
        else:
            data['order_item_staff_formset'] = OrderItemStaffFormSet(
                instance=self.object)
        return data


class CategoryListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Category
    template_name = 'staff/categorieslist.html'


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Category
    fields = ['name']
    template_name = 'staff/categoriesview.html'
    success_url = reverse_lazy('dashboard')


class CategoryCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Category
    fields = ['name']
    template_name = 'staff/categorycreate.html'
    success_url = reverse_lazy('dashboard')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Product
    fields = '__all__'
    template_name = 'staff/newitem.html'
    success_url = reverse_lazy('dashboard')


class ProductCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Product
    fields = '__all__'
    template_name = 'staff/newitem.html'
    success_url = reverse_lazy('dashboard')


class Managerview(View):
    template_name = 'staff/manager.html'
    model = OrderItem

    def get(self, request):
        count, summ, time, hour = dict(), dict(), dict(), dict()
        mountain_elevation_data, mountain_elevation_data_time = list(), list()
        for item in OrderItem.objects.all():
            if item.order.id not in time:
                time[item.order.id] = Order.objects.filter(id=item.order.id)
            count[item.product.name] = OrderItem.objects.filter(
                product_id=item.product.id)
        for k, v in time.items():
            for x in v:
                if k in hour.keys():
                    hour[k] += x.created.hour
                else:
                    hour[k] = x.created.hour
        for k, v in count.items():
            for x in v:
                if k in summ.keys():
                    summ[k] += x.quantity
                else:
                    summ[k] = x.quantity
        for i in range(0, 25):
            for k, v in hour.items():
                if k == i:
                    mountain_elevation_data_time[i]['y'] += 1
                else:
                    mountain_elevation_data_time.append({"label": i, "y": 0})
        for k, v in summ.items():
            mountain_elevation_data.append({"label": k, "y": v})
        return render(request, self.template_name, context={"mountain_elevation_data": mountain_elevation_data, "mountain_elevation_data_time": mountain_elevation_data_time})

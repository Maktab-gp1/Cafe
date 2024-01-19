from typing import Any
from django.shortcuts import render
from django.views.generic import ListView
from shop.models import Category, Product, Cafe
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.views import View
from datetime import datetime
from decimal import Decimal
from .utils import Reporting
from orders.models import Order, Table
from .utils import export_csv
from orders.models import Order, OrderItem


class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class DashboardView(SuperUserRequiredMixin, View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        category = request.GET.get('category')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        selected_range = request.GET.get('range', 'month')

        if selected_range == 'year':
            days = 365
        elif selected_range == 'week':
            days = 7
        elif selected_range == 'day':
            days = 1
        elif selected_range == 'month':
            days = 30
        elif selected_range == 'total':
            days = 99999

        reporting_params = {'days': days}
        if category == 'All':
            category = None
        if start_date and end_date:
            start_date_obj = datetime.strptime(start_date, "%Y/%m/%d").date()
            end_date_obj = datetime.strptime(end_date, "%Y/%m/%d").date()
            reporting_params = {
                'start_at': start_date_obj, 'end_at': end_date_obj}
        else:
            start_date_obj = datetime.strptime('01/01/2024', '%m/%d/%Y').date()
            end_date_obj = datetime.strptime('01/01/2025', '%m/%d/%Y').date()

        count, summ, time, hour = dict(), dict(), dict(), dict()
        mountain_elevation_data, mountain_elevation_data_time = list(), list()
        cat = Category.objects.all()
        for item in OrderItem.objects.all():
            if start_date_obj <= item.order.created.date() <= end_date_obj:
                if item.order.id not in time:
                    time[item.order.id] = Order.objects.filter(
                        id=item.order.id)
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
                if category is not None:
                    if x.product.category.name == category:
                        if k in summ.keys():
                            summ[k] += x.quantity
                        else:
                            summ[k] = x.quantity
                else:
                    if k in summ.keys():
                        summ[k] += x.quantity
                    else:
                        summ[k] = x.quantity
        for i in range(0, 25):
            mountain_elevation_data_time.append({"label": i, "y": 0})
            for k, v in hour.items():
                if v == i:
                    mountain_elevation_data_time[i]['y'] += 1
        for k, v in summ.items():
            mountain_elevation_data.append({"label": k, "y": v})
        r = Reporting(reporting_params)

        total_sales: Decimal = r.total_sales()
        percentage_difference = r.get_percentage_difference()
        peak_hour, most_peak_hour = r.peak_hours()
        context = {
            'total_sales': total_sales,
            'percentage_difference': percentage_difference,
            'favorite_food': r.favorite_foods(),
            'favorite_table': r.favorite_tables(),
            'peak_hour': peak_hour,
            'peak_day': r.peak_day_of_week(),
            'most_peak_hour': most_peak_hour,
            'best_cutomer': r.best_cutomer(),
            'favorite_category': r.favorite_category(),
            'order_status_counts': r.order_status_counts(),
            "mountain_elevation_data": mountain_elevation_data,
            "mountain_elevation_data_time": mountain_elevation_data_time,
            'category': cat,
        }

        return render(request, self.template_name, context=context)


@user_passes_test(lambda u: u.is_superuser)
def OrderList(request):
    context = {}
    context['object_list'] = Order.objects.all().order_by('id')

    if 'export_csv' in request.GET:
        return export_csv()

    if request.method == "POST":
        order_instance = Order.objects.filter(id=request.POST["id"]).first()
        order_instance.status = request.POST["status"]
        order_instance.save()

    return render(request, 'dashboard/order_list.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def tables(request):
    context = {}
    context['tables'] = Table.objects.all()
    if request.method == "POST":
        table_instance = Table.objects.filter(id=request.POST["id"]).first()
        if "is_available" in request.POST:
            table_instance.is_available = True
        else:
            table_instance.is_available = False
        table_instance.save()
    return render(request, 'dashboard/tables.html', context=context)


class TableCreateView(SuperUserRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Table
    fields = ['id', 'name']
    template_name = 'dashboard/createtable.html'
    success_url = reverse_lazy('dashboard:table')


class FoodsListView(SuperUserRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Product
    template_name = 'dashboard/foodslist.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class FoodUpdateView(SuperUserRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Product
    fields = '__all__'
    template_name = 'dashboard/newfood.html'
    success_url = reverse_lazy('dashboard:foods')


class FoodCreateView(SuperUserRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Product
    fields = '__all__'
    template_name = 'dashboard/newfood.html'
    success_url = reverse_lazy('dashboard:foods')


class CategoryUpdateView(SuperUserRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Category
    fields = ['name']
    template_name = 'dashboard/newcategory.html'
    success_url = reverse_lazy('dashboard:foods')


class CategoryCreateView(SuperUserRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Category
    fields = ['name']
    template_name = 'dashboard/newcategory.html'
    success_url = reverse_lazy('dashboard:foods')


class CafeInfoUpdateView(UpdateView):
    model = Cafe
    fields = '__all__'
    template_name = 'dashboard/updateinfo.html'
    success_url = reverse_lazy('dashboard:manger')

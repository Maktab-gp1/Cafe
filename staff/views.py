from typing import Any
from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy 
from django.views import View
from django.views.generic.edit import UpdateView ,CreateView 
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import Order,OrderItem, Table
from shop.models import Category , Product 
from .mixin import OrderFieldsMixin,OrderItemFormValidMixin
from .forms import  OrderItemStaffFormSet 
import csv
from django.http import HttpResponse
from django.db.models import Count, Sum, F, ExpressionWrapper, DecimalField

  
def export_csv():
        queryset = Order.objects.all().values()
        customers_data = (
            queryset
            .values('phone')
            .annotate(count=Count('id'),
                      total=Sum(
                          F('items__price') * F('items__quantity')  ,
                          output_field=DecimalField(max_digits=10, decimal_places=2)
                      )
                      )
            .order_by('-total')
        )
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="customer_orders.csv"'

        writer = csv.writer(response)
        headers = ['phone' , 'count', 'total']
        writer.writerow(headers)

        for row in customers_data:
            writer.writerow([str(row[field]) for field in headers])

        return response  

    
   
@login_required
def dashboard(request):
    context = {}
    context["products"] = Product.objects.all()
    context["categories"] = Category.objects.all()
    context['object_list'] = Order.objects.all().order_by('id')
    
    if 'export_csv' in request.GET:
        return export_csv()
    
    if request.method == "POST":
        order_instance = Order.objects.filter(id=request.POST["id"]).first()
        order_instance.status = request.POST["status"]
        order_instance.save() 
    
    return render(request ,'staff/dashboard.html' , context=context )

    

    
@login_required
def tables(request):
    context = {}
    context['tables'] = Table.objects.all()
    if request.method == "POST":
        table_instance = Table.objects.filter(id=request.POST["id"]).first()
        if "is_available" in request.POST :
            table_instance.is_available = True
        else:
            table_instance.is_available = False
        table_instance.save()
    return render(request,'staff/tablelist.html' , context=context)

class TableCreateView(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('login')
    model= Table
    fields=['id' ,'name']
    template_name = 'staff/tablecreate.html'
    success_url = reverse_lazy('tablelist')

class OrderStaffUpdate(LoginRequiredMixin,UpdateView,OrderFieldsMixin,OrderItemFormValidMixin): 
    login_url = reverse_lazy('login')
    model = Order
    fields = '__all__'
    template_name = 'staff/dashboard1.html'
    success_url = reverse_lazy('staff/dashboard')
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            form =  OrderItemStaffFormSet(self.request.POST,instance=self.object)
            data['order_item_staff_formset'] = form
            form.save()
        else:
            data['order_item_staff_formset'] = OrderItemStaffFormSet(instance=self.object)
        return data


class CategoryListView(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('login')
    model = Category
    template_name = 'staff/categorieslist.html'

class CategoryUpdateView(LoginRequiredMixin,UpdateView):
    login_url = reverse_lazy('login')
    model = Category
    fields= ['name']
    template_name = 'staff/categoriesview.html'
    success_url = reverse_lazy('dashboard')
      
class CategoryCreateView(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('login')
    model= Category
    fields=['name']
    template_name = 'staff/categorycreate.html'
    success_url = reverse_lazy('dashboard')

class ProductUpdateView(LoginRequiredMixin,UpdateView):
    login_url = reverse_lazy('login')
    model = Product
    fields= '__all__'
    template_name = 'staff/newitem.html'
    success_url = reverse_lazy('dashboard')
      
class ProductCreateView(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('login')
    model= Product
    fields='__all__'
    template_name = 'staff/newitem.html'
    success_url = reverse_lazy('dashboard')


class Managerview(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    template_name = 'staff/manager.html'
    model = OrderItem

    def get(self, request):
        count = dict()
        summ = dict()
        mountain_elevation_data = list()
        for item in OrderItem.objects.all():
            count[item.product.name] = OrderItem.objects.filter(
                product_id=item.product.id)
        for k, v in count.items():
            for x in v:
                if k in summ.keys():
                    summ[k] += x.quantity
                else:
                    summ[k] = x.quantity
        for k, v in summ.items():
            mountain_elevation_data.append({"label": k, "y": v})
        return render(request, self.template_name, context={'count': summ, "mountain_elevation_data": mountain_elevation_data})
    









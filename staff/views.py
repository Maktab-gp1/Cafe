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

  
  

    
   
@login_required
def dashboard(request):
    context = {}
    context["products"] = Product.objects.all()
    context["categories"] = Category.objects.all()
    context['object_list'] = Order.objects.all().order_by('id')
   
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
    


import csv
import datetime
from django.http import HttpResponse




def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not \
              field.many_to_many and not field.one_to_many] 
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    # for obj in queryset:
    #     data_row = []
    #     for field in fields:
    #         value = getattr(obj, field.name)
    #         if isinstance(value, datetime.datetime):
    #             value = value.strftime('%d/%m/%Y')
    #         data_row.append(value)
    #     writer.writerow(data_row)
    data_rows = [[getattr(obj, field.name).strftime('%d/%m/%Y') \
        if isinstance(getattr(obj, field.name), datetime.datetime) \
        else getattr(obj, field.name) for field in fields] for obj in queryset]
    writer.writerows(data_rows)
    return response
export_to_csv.short_description = 'Export to CSV'

from typing import Any
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.views.generic import ListView ,DetailView

# Create your views here.

class ProductListView(ListView):
    template_name = 'shop/product/list1.html'
    def get_queryset(self) :
        if 'category' not in self.kwargs:
            self.kwargs['category']='all'
            if self.request.GET.get('search') :
                return Product.objects.filter(available=True , name__icontains=self.request.GET['search'] )
            return Product.objects.filter(available=True)
        if self.kwargs['category']=='all':
            self.kwargs['category']='all'
            if self.request.GET.get('search') :
                return Product.objects.filter(available=True , name__icontains=self.request.GET['search'] )
            return Product.objects.filter(available=True)
        else :
            self.category = get_object_or_404(Category,
                                          slug=self.kwargs['category'])
            if self.request.GET.get('search') :
                return Product.objects.filter(category = self.category,available=True , name__icontains=self.request.GET['search'] )
            return Product.objects.filter(available=True,category = self.category)
    def post(self, request, *args, **kwargs):
        # print(self.request.POST)
        override = (self.request.POST['override'])
        quantity =self.request.POST['quantity']
        form = CartAddProductForm(quantity,override)
        # if form.is_valid():
            # <process form cleaned data>
        return reverse('cart:cart_add')    
            
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context["form"] =  CartAddProductForm()
        return context            



    
class ProductDetailView(DetailView):
    queryset = Product.objects.filter(available = True)
    template_name = 'shop/product/detail1.html'
    slug_url_kwarg = "slug"
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] =  CartAddProductForm()
        print(context)
        return context
    




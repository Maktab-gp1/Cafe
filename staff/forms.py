from django.views.generic.edit import UpdateView
from django.forms.models import inlineformset_factory
from django import forms
from django.forms import modelformset_factory ,formset_factory 
from orders.models import Order ,OrderItem
from shop.models import Category , Product




class StatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

StatusFormSet = formset_factory(StatusForm , extra = 0)
CategoryFormSet = modelformset_factory(Category,fields='__all__',extra=4)
OrderItemStaffFormSet = inlineformset_factory(Order, OrderItem,fields='__all__')



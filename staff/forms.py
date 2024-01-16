from django.forms.models import inlineformset_factory
from django import forms
from orders.models import Order ,OrderItem , Table


class StatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

class TableForm(forms.ModelForm):
    class Meta:
       model = Table
       fields = ['is_available']

OrderItemStaffFormSet = inlineformset_factory(Order, OrderItem,fields='__all__')



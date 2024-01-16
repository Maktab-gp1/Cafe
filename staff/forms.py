from django.forms.models import inlineformset_factory
from django import forms
from orders.models import Order ,OrderItem


class StatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

OrderItemStaffFormSet = inlineformset_factory(Order, OrderItem,fields='__all__')



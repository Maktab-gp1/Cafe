from django import forms
from .models import Order ,Table


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [ 'phone','table']
    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        self.fields['table'].queryset = Table.objects.filter(is_available= True)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        

       

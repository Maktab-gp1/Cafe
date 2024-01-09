from django.http import Http404
from django.shortcuts import redirect

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
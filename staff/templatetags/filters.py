from django import template
from staff.forms import StatusForm

register = template.Library()

@register.inclusion_tag("staff/_item_order.html")
def show_order(order):
    form = StatusForm(instance=order)
    return {"order": order, "form": form}
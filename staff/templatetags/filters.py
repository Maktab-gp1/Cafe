from django import template
from staff.forms import StatusForm , TableForm

register = template.Library()

@register.inclusion_tag("staff/_item_order.html")
def show_order(order):
    form = StatusForm(instance=order)
    return {"order": order, "form": form}

@register.inclusion_tag("staff/_available_form.html")
def table_avalibility(table):
    form = TableForm(instance = table)
    return {"table": table , "form": form}
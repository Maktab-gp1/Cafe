from django import forms
from django.core.exceptions import ValidationError
from .models import Reservation


class ReservationCreation(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = "__all__"
        # exclude = ["account_id", "table_id"]
# class StaffCreation(forms.ModelForm):
#     class Meta:
#         model = Reservation
#         fields = "__all__"
#         # exclude = ["account_id", "table_id"]

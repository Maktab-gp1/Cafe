# from django import forms
# from django.contrib.auth.models import User


# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(label='Password',
#                                widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Repeat password',
#                                 widget=forms.PasswordInput)
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'email']
#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password'] != cd['password2']:
#             raise forms.ValidationError("Passwords don't match.")
#         return cd['password2']

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import PasswordResetForm

UserModel = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    phone = forms.RegexField(regex = '^9\d{9}$', required=True,
                            error_messages = {
                                    'required': 'The Phone field is required.',
                                    'invalid' : 'Enter phone number in 9XX.. format.'
                                }
                            )
    class Meta:
        model = UserModel
        fields = ('phone',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = UserModel
        fields = ('phone',)

class CustomPasswordResetForm(PasswordResetForm):
    pass

class VerifyForm(forms.Form):
    otp_code = forms.CharField(label='Code', max_length=6, required=True,
                        error_messages = {
                            'required' : 'the field is required',
                            'max_length' : 'max length exceeded'
                        }
    
                    )
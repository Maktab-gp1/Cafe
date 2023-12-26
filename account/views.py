from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import( authenticate,
                                 login as django_login,
                                 logout )
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required
from .forms import LoginForm , UserRegistrationForm


# Create your views here.
@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {})
                  
def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
    elif request.method =="POST":
        
        form = AuthenticationForm(data= request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            print(username)
            password = form.cleaned_data['password']
            print(password)
            user = authenticate(request,username=username,password=password)
            if user is not None:
                django_login(request,user)
                messages.add_message(request,messages.SUCCESS,f'welcome {username}')
                if user.is_staff == True:
                    return redirect('staff')
                else:
                    return redirect('checkout')
    return render(request , 'account/login.html',context={'form':form})



def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})

def logout_view(request):
    logout(request)
    return redirect('login')

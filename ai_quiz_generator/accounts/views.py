from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.

def login_view(request):
    if request.method== "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                messages.success(request,"Login successful !")
                return redirect('quiz:home')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        pass
    return render(request, 'accounts/login.html')

def logout_view(request):
   logout(request)
   messages.success(request, "Logout successful")
   return redirect('login') 

def signup_view(request):
    if request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('quiz:home')
        else:
            messages.error(request, "Registrtion failed! Please correct the the error")
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form':form})



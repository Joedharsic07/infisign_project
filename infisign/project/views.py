from django.shortcuts import render,redirect
from django.views import View
from .models import CustomUser 
from django.contrib import messages
from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import CustomUser

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # Get form data
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        field_errors = {}
        if not email:
            field_errors['email'] = "Email is required."
        if not password:
            field_errors['password'] = "Password is required."
        if not confirm_password:
            field_errors['confirm_password'] = "Confirm Password is required."
        if password and confirm_password and password != confirm_password:
            field_errors['confirm_password'] = "Passwords do not match."
        if email and CustomUser.objects.filter(email=email).exists():
            field_errors['email'] = "An account with this email already exists."
        if field_errors:
            return render(request, 'register.html', {'field_errors': field_errors})
        user = CustomUser(
            email=email,
            first_name=firstname,
            last_name=lastname,
            username=username
        )
        user.set_password(password)  
        user.save()

        messages.success(request, "Account created successfully. You can now log in.")
        return redirect('login')  

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')  
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        errors = {}

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            if not email:
                errors['email'] = "Email is required."
            if not password:
                errors['password'] = "Password is required."
            if email and password and user is None:
                errors['password'] = "Invalid email or password."
            return render(request, 'login.html', {'field_errors': errors})

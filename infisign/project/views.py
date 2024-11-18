from django.shortcuts import render,redirect,get_object_or_404
from .models import BlogPost
from .forms import BlogPostForm
from django.views import View
from .models import CustomUser 
from django.contrib import messages
from django.contrib.auth import authenticate, login,  logout
from django.contrib.auth.mixins import LoginRequiredMixin

# register view
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        email = request.POST.get('email')
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
        user = CustomUser(email=email,)
        user.set_password(password)  
        user.save()
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)

        messages.success(request, "Account created successfully. You are now logged in.")
        return redirect('home')  
# login-view
class LoginView(View):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        field_errors = {}
        if not email:
            field_errors['email'] = "Email is required."
        if not password:
            field_errors['password'] = "Password is required."
        if email and password:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                field_errors['password'] = "Invalid email or password."
        return render(request, 'login.html', {'field_errors': field_errors})
    def get(self, request):
        return render(request, 'login.html')
# home view
class homeview(LoginRequiredMixin, View):
    def get(self, request):
        articles = BlogPost.objects.all()
        article_id = request.GET.get('article_id')  
        selected_article = None
        if article_id:
            selected_article = get_object_or_404(BlogPost, pk=article_id)
        return render(request, 'home.html', {'articles': articles,'article': selected_article})
# view article view
class articledetailView(View):
    def get(self, request, pk):
        article = get_object_or_404(BlogPost, pk=pk)
        return render(request, 'home.html', {'article': article})

def create_blog_post(request):
    if request.method == 'POST':
        form=BlogPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            form=BlogPostForm
        return render(request,'create_blog_post',{'form',BlogPostForm})
    form = BlogPostForm()
    return render(request, 'create_blog_post.html', {'form': form})
# logout view
class LogoutView(View):
    def get(self, request):
        return redirect('login')  
    def post(self, request):
        logout(request)
        return redirect('login')
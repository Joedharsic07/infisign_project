from django.shortcuts import render,redirect,get_object_or_404
from .models import BlogPost,Category
from .forms import BlogPostForm
from django.views import View
from .models import CustomUser 
from django.contrib import messages
from django.http import JsonResponse

from django.contrib.auth import authenticate, login,logout

# register view
# class RegisterView(View):
#     def get(self, request):
#         return render(request, 'register.html')

#     def post(self, request):
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')
#         field_errors = {}

#         if not email:
#             field_errors['email'] = "Email is required."
#         if not password:
#             field_errors['password'] = "Password is required."
#         if not confirm_password:
#             field_errors['confirm_password'] = "Confirm Password is required."
#         if password and confirm_password and password != confirm_password:
#             field_errors['confirm_password'] = "Passwords do not match."
#         if email and CustomUser.objects.filter(email=email).exists():
#             field_errors['email'] = "An account with this email already exists."

#         if field_errors:
#             return render(request, 'register.html', {'field_errors': field_errors})
#         user = CustomUser(email=email,)
#         user.set_password(password)  
#         user.save()
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             login(request, user)

#         messages.success(request, "Account created successfully. You are now logged in.")
#         return redirect('home')  
    
# login-view
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')    
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
                if user.is_superuser:
                    login(request, user)
                    return redirect('home')
                else:
                    field_errors['email'] = "Access only for superusers."
            else:
                field_errors['password'] = "Invalid email or password."
        return render(request, 'login.html', {'field_errors': field_errors})

# mainhome
class mainhomeview(View):
    def get(self, request):
        categories = Category.objects.all()
        category_id = request.GET.get('category_id')  
        article_id = request.GET.get('article_id')
        selected_category = None
        selected_article = None
        articles = None  
        if not category_id and categories.exists():
            selected_category = categories.first() 
            articles = selected_category.blogposts.all()  
        elif category_id:
            selected_category = get_object_or_404(Category, pk=category_id)
            articles = selected_category.blogposts.all()
        if article_id:
            selected_article = get_object_or_404(BlogPost, pk=article_id)
        return render(request, 'mainhome.html', {
            'categories': categories,
            'selected_category': selected_category,
            'articles': articles,
            'selected_article': selected_article,
        })
    def post(self, request):
        query = request.POST.get('q', '').strip()  
        if query:
            articles = BlogPost.objects.filter(title__icontains=query)
        else:
            articles = BlogPost.objects.none()  
        data = {'results': [{'id': article.id, 'title': article.title} for article in articles]}
        return JsonResponse(data) 
# home view
class homeview(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        categories = Category.objects.all()
        category_id = request.GET.get('category_id')  
        article_id = request.GET.get('article_id')
        selected_category = None
        selected_article = None
        articles = None  
        if not category_id and categories.exists():
            selected_category = categories.first() 
            articles = selected_category.blogposts.all()  
        elif category_id:
            selected_category = get_object_or_404(Category, pk=category_id)
            articles = selected_category.blogposts.all()
        if article_id:
            selected_article = get_object_or_404(BlogPost, pk=article_id)
        return render(request, 'home.html', {
            'categories': categories,
            'selected_category': selected_category,
            'articles': articles,
            'selected_article': selected_article,
        })
    def post(self, request):
        query = request.POST.get('q', '').strip()  

        if query:
            articles = BlogPost.objects.filter(title__icontains=query)
        else:
            articles = BlogPost.objects.none()  
        data = {'results': [{'id': article.id, 'title': article.title} for article in articles]}
        return JsonResponse(data)  
    
# create view
class CreateBlogPostView(View):
    def get(self, request):
        form = BlogPostForm()
        categories = Category.objects.all()
        print(categories)
        return render(request, 'create_blog_post.html', {'form': form, 'categories': categories})
    def post(self, request):
        form = BlogPostForm(request.POST)
        category_id = request.POST.get('category')  
        other_category = request.POST.get('other_category', '').strip()  
        if category_id == 'others' and other_category:
            try:
                category = Category.objects.get(name=other_category)
            except Category.DoesNotExist:
                category = Category.objects.create(name=other_category)
            request.POST = request.POST.copy()  
            request.POST['category'] = category.id  
            form = BlogPostForm(request.POST)  
        if form.is_valid():
            form.save()  
            return redirect('home') 
        categories = Category.objects.all()
        return render(request, 'create_blog_post.html', {'form': form, 'categories': categories})
    
# editpage
class EditArticleView(View):
    def get(self, request, article_id):
        article = get_object_or_404(BlogPost, id=article_id)
        categories = Category.objects.all()    
        form = BlogPostForm(instance=article)
        return render(request, 'edit_article.html', {'form': form, 'article': article, 'categories': categories})
    def post(self, request, article_id):
        article = get_object_or_404(BlogPost, id=article_id)
        post_data = request.POST.copy()
        category_id = post_data.get('category')
        other_category = post_data.get('other_category', '').strip() 
        if category_id == 'others' and other_category:
            category, created = Category.objects.get_or_create(name=other_category)
            post_data['category'] = category.id  
        elif category_id:
            category = get_object_or_404(Category, id=category_id)
            post_data['category'] = category.id
        form = BlogPostForm(post_data, instance=article)
        if form.is_valid():
            form.save()  
            return redirect('home')  
        categories = Category.objects.all()  
        return render(request, 'edit_article.html', {
            'form': form,
            'article': article,
            'categories': categories,
        })

# delete view
class deleteview(View):
    def get(self, request, article_id):
        article = get_object_or_404(BlogPost, id=article_id)
        article.delete()
        return redirect('home')
    
# logout view
class LogoutView(View):  
    def post(self, request):
        logout(request)
        return redirect('login')
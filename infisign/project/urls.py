from django.urls import path
from.views import RegisterView, LoginView,homeview,LogoutView,articledetailView
from project.views import create_blog_post
urlpatterns=[
    path('register/',RegisterView.as_view(),name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('home/', homeview.as_view(), name='home'),
    path('logout/', LogoutView.as_view(), name='logout'), 
    path('article/<int:pk>/', articledetailView.as_view(), name='article_detail'),
    path('', create_blog_post, name='create_blog_post'),

 
]
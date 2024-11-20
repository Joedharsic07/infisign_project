from django.urls import path
from.views import RegisterView, LoginView,homeview,LogoutView,mainhomeview,CreateBlogPostView,EditArticleView
urlpatterns=[
    path('register/',RegisterView.as_view(),name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('home/', homeview.as_view(), name='home'),
    path('logout/', LogoutView.as_view(), name='logout'), 
    path('create/', CreateBlogPostView.as_view(), name='create_blog_post'),
    path('edit_article/<int:article_id>/', EditArticleView.as_view(), name='edit_article'),
    path('',mainhomeview.as_view(),name='mainhome')
]
from django.urls import path
from.views import RegisterView, LoginView,homeview,editview,LogoutView

urlpatterns=[
    path('register/',RegisterView.as_view(),name='register'),
    path('', LoginView.as_view(), name='login'),
    path('home/', homeview.as_view(), name='home'),
    path('editor/',editview.as_view(),name='editor'),
    path('logout/', LogoutView.as_view(), name='logout'),  
]
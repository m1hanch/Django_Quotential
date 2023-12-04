from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'app_auth'

urlpatterns = [
    path('signup/', LoginView.as_view(template_name='app_auth/login.html'), name='signup'),
    path('signin/', LoginView.as_view(template_name='app_auth/login.html'), name='signin'),
    path('logout/', LoginView.as_view(template_name='app_auth/login.html'), name='logout'),
]

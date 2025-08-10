from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login_view/', views.login_view, name='login_view'),
    path('profile/', views.profile, name='profile'),
    path('product/', views.product, name='product'),
    path('change_password/', views.change_password, name='change_password'),
    path('logout_view/', views.logout_view, name='logout_view'),
]




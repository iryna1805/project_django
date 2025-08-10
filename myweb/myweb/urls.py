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
     path('cart/', views.cart_view, name='cart_view'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-quantity/<int:cart_item_id>/<str:action>/', views.update_quantity, name='update_quantity'),
    path('products/json/', views.products_json, name='products_json'),

    path('fix_cart/', views.fix_cart_users),

]





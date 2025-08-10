import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, LoginForm
from .models import UserProfile, Product, Cart, CustomUser
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate


def home(request):
    return render(request, 'index.html')

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    return render(request, 'login.html', {'form': form})

def products_json(request):
    products = Product.objects.all()
    data = []
    for product in products:
        data.append({
            'id': product.id,
            'name': product.name,
            'price': str(product.price),  # decimal to string для JSON
            'description': product.description,
            'image_url': product.image_url,
        })
    return JsonResponse({'products': data})

@login_required
def profile(request):
    return render(request, 'profile.html', {'name': request.user.username, 'email': request.user.email})

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login_view')

    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
    cart_item.save()
    
    return redirect('cart_view')

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')

def update_quantity(request, cart_item_id, action):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)

    if action == "increase":
        cart_item.quantity += 1
    elif action == "decrease" and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()

    return redirect('cart_view')

def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login_view')

    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.get_total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})



def fix_cart_users(request):
    user = CustomUser.objects.get(id=1)
    
    carts_without_user = Cart.objects.filter(user__isnull=True)
    for cart in carts_without_user:
        cart.user = user
        cart.save()
    
    return HttpResponse(f"Updated {carts_without_user.count()} cart items")






def logout_view(request):
    logout(request)
    return redirect('/login_view/')

def product(request):
    products = Product.objects.all()
    return render(request, 'product.html', {'products': products})

@login_required
def change_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            old_password = data.get('oldPassword')
            new_password = data.get('newPassword')

            user = request.user
            if not authenticate(request, username=user.username, password=old_password):
                return JsonResponse({'error':'Старий пароль не вірний'}, status=400)

            user.set_password(new_password)
            user.save()

            login(request, user)
            return JsonResponse({'msg': 'Пароль успішно змінено'})
        except Exception as e:
            print(f"Помилка зміни пароля: {e}")
            return JsonResponse({'error': 'Server error'}, status=500)
    return JsonResponse({'error': 'method not found'}, status=405)









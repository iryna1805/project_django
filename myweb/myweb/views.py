import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .models import UserProfile, Product, Cart
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

@login_required
def profile(request):
    return render(request, 'profile.html', {'name': request.user.username, 'email': request.user.email})

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









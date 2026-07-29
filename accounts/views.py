from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserUpdateForm
from django.contrib.auth import logout as auth_logout
from cart.models import Order

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'The account has been created successfully!')
            return redirect('dashboard')  
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            if user.is_staff:
                return redirect('dashboard')
            else:
                return redirect('my_account')  
        else:
            messages.error(request, 'Incorrect username or password.')
    return render(request, 'accounts/login.html')

@login_required
def my_account_view(request):
    if request.method == 'POST' and 'update_profile' in request.POST:
        profile_form = UserUpdateForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('my_account')
    else:
        profile_form = UserUpdateForm(instance=request.user)

    password_form = PasswordChangeForm(user=request.user)
    if request.method == 'POST' and 'change_password' in request.POST:
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('my_account')

    orders_count = len(request.session.get('orders', []))
    context = {
        'profile_form': profile_form,
        'password_form': password_form,
        'orders_count': orders_count,
    }
    return render(request, 'accounts/my_account.html', context)

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # يبقي المستخدم مسجلاً
            messages.success(request, 'Password changed successfully!')
            return redirect('my_account')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/change_password.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        auth_logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('home')
    return render(request, 'accounts/logout_confirm.html')

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin, login_url='login')
def dashboard_view(request):
    context = {
        'total_products': 0,   
        'total_orders': Order.objects.count(),
        'total_users': User.objects.count() if request.user.is_superuser else 0,
    }
    return render(request, 'accounts/dashboard.html', context)

def check_username(request):
    username = request.GET.get('username', None)
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})   

@staff_member_required(login_url='login')
def manage_users(request):
    if not request.user.is_superuser:
        messages.error(request, "Access denied.")
        return redirect('dashboard')
    users = User.objects.all()
    return render(request, 'accounts/manage_users.html', {'users': users})       
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .forms import AuthenticationForm
from blog.constants import Constants
from django.contrib.auth import login as auth_login, authenticate 
from blog.views import get_common_context
from users.models import Profile

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = authenticate(username=username, password=form.cleaned_data.get('password'))
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Вы вошли в аккаунт {username}.')
                return redirect('profile')
    else:
        form = AuthenticationForm()
    context = get_common_context()
    context['form'] = form
    return render(request, 'users/login.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш аккаунт создан: можно войти на сайт.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = get_common_context()
    context['form'] = form
    return render(request, 'users/register.html', context)

@login_required
def profile(request):
    context = get_common_context()
    return render(request, 'users/profile.html', context)

def staff(request):
    context = get_common_context()
    context['staff_members'] = Profile.objects.filter(show_in_staff=True)
    return render(request, 'users/staff.html', context)
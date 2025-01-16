from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from . import forms
from blog.views import get_common_context
from .models import Profile
from blog.models import Post, Type
from django.contrib.auth.models import User
from blog import constants

def login(request):
    if request.method == 'POST':
        form = forms.AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = authenticate(username=username, password=form.cleaned_data.get('password'))
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Вы вошли в аккаунт {username}.')
                return redirect('profile')
    else:
        form = forms.AuthenticationForm()
    context = get_common_context()
    context['form'] = form
    return render(request, 'users/login.html', context)

def logout(request):
    auth_logout(request)
    messages.success(request, 'Вы вышли из аккаунта.')
    return redirect('blog-home')

def register(request):
    if not constants.SITE_PRIVATE:
        if request.method == 'POST':
            form = forms.UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Ваш аккаунт создан: можно войти на сайт.')
                return redirect('login')
        else:
            form = forms.UserRegisterForm()
        context = get_common_context()
        context['form'] = form
        return render(request, 'users/register.html', context)
    else:
        messages.error(request, 'Регистрация на этом сайте закрыта.')
        return redirect('blog-home')

@login_required
def profile(request):
    context = get_common_context()
    return render(request, 'users/profile.html', context)

@login_required
def profile_edit(request):
    user_form = forms.UserEditForm(instance=request.user, data=request.POST or None)
    profile_form = forms.UserProfileEditForm(instance=request.user.profile, data=request.POST or None, files=request.FILES or None)
    
    if request.method == 'POST' and user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        messages.success(request, 'Ваш профиль обновлен.')
        return redirect('profile')
    
    context = get_common_context()
    context['user_form'] = user_form
    context['profile_form'] = profile_form
    return render(request, 'users/profile_edit.html', context)

def staff(request):
    context = get_common_context()
    context['staff_members'] = Profile.objects.filter(show_in_staff=True)
    return render(request, 'users/staff.html', context)

def author(request, username):
    try:
        author = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, 'Такого пользователя не существует.')
        return redirect('blog-home')
    
    context = get_common_context()
    context['author'] = author
    context['posts'] = Post.objects.filter(author=author)
    return render(request, 'users/author.html', context)

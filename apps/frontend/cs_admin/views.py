from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

import datetime

from apps.backend.users.models import Worker

# Create your views here.
def main(request):
    if request.user.is_authenticated:
        return redirect('front:cs_admin:user_list')
    request.session['error'] = 'NOT_LOGGED_ERROR'
    return redirect('front:login:login')

def user_list(request):
    if request.user.is_authenticated:
        users = []
        for user in User.objects.all():
            state = Worker.objects.filter(user=user).first()
            working = state.working if state != None else None
            users.append({
                'user_info': user,
                'working': working
            })
        context = {
            'title': "Panel Administratora",
            'logged_user': request.user,
            'active': 'user_list',
            'users': users
        }
        return render(
            request,
            'apps/main_management/html/main.html',
            context
        )
    request.session['error'] = 'NOT_LOGGED_ERROR'
    return redirect('login_view')

def add_user(request):
    if request.user.is_authenticated:
        context = {
            'title': "Dodaj użytkownika - Panel Administratora",
            'logged_user': request.user,
            'active': 'add_user'
        }
        return render(
            request,
            'apps/main_management/html/main.html',
            context
        )
    request.session['error'] = 'NOT_LOGGED_ERROR'
    return redirect('login_view')

def user_manage(request, pk):
    if request.user.is_authenticated:
        user = User.objects.get(id=pk)
        worker = Worker.objects.filter(user=user).first()
        context = {
            'title': "Zarządzanie użytkownikiem - Panel Administratora",
            'logged_user': request.user,
            'active': 'manage_user',
            'user': {
                'user_info': user,
                'worker': worker
            }
        }
        return render(
            request,
            'apps/main_management/html/main.html',
            context
        )
    request.session['error'] = 'NOT_LOGGED_ERROR'
    return redirect('login_view')

def change_password(request, pk):
    logged_user = request.user
    if logged_user.is_staff:
        user = get_object_or_404(User, id=pk)
        context = {
            'title': "Zmiana hasła użytkownika - Panel Administratora",
            'logged_user': request.user,
            'active': 'change_password',
            'user': user
        }
        return render(
            request,
            'apps/main_management/html/main.html',
            context
        )
    raise PermissionDenied
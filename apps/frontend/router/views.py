from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from apps.backend.users.models import Worker, WorkTimestamp 
from apps.utils.errors import AuthError
from .routes import router_routes, cs_admin_routes, worker_routes, login_routes

# Create your views here.

def main_router_view(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect(router_routes['cs_admin'])
    if request.user.is_authenticated:
        worker = Worker.objects.filter(user=request.user).exists()
        if worker:
            return redirect(router_routes['worker'])
        logout(request)
        return AuthError.not_personel(request)          
    return redirect(login_routes['login_panel'])

def worker_router_view(request):
    if request.user.is_authenticated:
        worker = Worker.objects.filter(user=request.user).first()
        if worker:
            if not worker.working:
                if not WorkTimestamp.objects.filter(
                        user=request.user,
                        working_after=True,
                        timestamp__date=timezone.localdate()
                    ).exists():
                    return redirect(worker_routes['start_work_panel'])
                return redirect(worker_routes['add_work_time_panel'])
            return redirect(worker_routes['finish_work_panel'])
    return AuthError.not_logged(request)

def cs_admin_router_view(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect(cs_admin_routes['user_list'])
    return AuthError.not_admin(request)
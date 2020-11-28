from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from apps.frontend.router.routes import router_routes

from .models import Worker, WorkTimestamp, AdditionalWorkTime
from . import functions as funcs

import datetime


def start_work_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            worker = Worker.objects.filter(user = request.user).first()
            if worker:
                worked_today = WorkTimestamp.objects.filter(
                    user=request.user,
                    working_after=True,
                    timestamp__date=timezone.localdate()
                    ).exists()
                if not (worker.working or worked_today):
                    worker.working = True
                    timestamp = WorkTimestamp.objects.create(
                        user = request.user,
                        working_after = True,
                        location=request.POST.get('location'))
                    timestamp.save()
                    worker.save()
                    if request.user.is_staff or request.user.is_superuser:
                        return redirect(router_routes['cs_admin'])
                    return redirect('back:auth:logout')
                return HttpResponseForbidden
            raise PermissionDenied
        raise PermissionDenied
    return HttpResponseBadRequest

def finish_work_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            worker = Worker.objects.filter(user = request.user).first()
            if worker:
                if worker.working:
                    worker.working = False
                    timestamp = WorkTimestamp.objects.create(
                        user = request.user,
                        working_after = False)
                    timestamp.save()
                    worker.save()
                    if request.user.is_staff or request.user.is_superuser:
                        return redirect(router_routes['cs_admin'])
                    return redirect('back:auth:logout')
                return HttpResponseForbidden
            raise PermissionDenied
        raise PermissionDenied
    return HttpResponseBadRequest

def add_work_time_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            worker = Worker.objects.filter(user = request.user).first()
            if worker:
                worked_today = WorkTimestamp.objects.filter(
                    user=request.user,
                    working_after=True,
                    timestamp__date=timezone.localdate()
                    ).exists()
                if not worker.working and worked_today:
                    time = request.POST.get('work_additional_time').split(':')
                    minutes = int(time[0])*60 + int(time[1])
                    funcs.add_work_time(worker, minutes)
                    if request.user.is_staff or request.user.is_superuser:
                        return redirect(router_routes['cs_admin'])
                    return redirect('back:auth:logout')
                return HttpResponseForbidden
            raise PermissionDenied
        raise PermissionDenied
    return HttpResponseBadRequest

def updateUserInfo(request):
    if request.method == "POST":
        result = funcs.update_user(
            request.user,
            request.POST)
        return redirect(router_routes['main'])
    return HttpResponseBadRequest

def updatePassword(request, pk):
    if request.method == "POST":
        if request.user.is_staff:
            funcs.update_password(
                get_object_or_404(User, id=pk),
                request.POST.get('new_password')
            )
            return redirect(router_routes['main'])
        raise PermissionDenied
    return HttpResponseBadRequest

def delete_user_view(request, pk):
    current_user = request.user
    if current_user.is_staff:
        funcs.delete_user(get_object_or_404(User, id=pk))
        return redirect (router_routes['main'])
    raise PermissionDenied

def group_action_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.POST.get('action') == 'delete':
                users_ids = request.POST.getlist('user_selection')
                for id in users_ids:
                    funcs.delete_user(id)
            return redirect('cs_admin:front:users')
    return redirect(router_routes['main'])

def overview_download_view(request):
    if request.method == 'POST' and request.user.is_authenticated:
        from_date = datetime.datetime.strptime(request.POST.get('date_from'), '%Y-%m-%d')
        to_date = datetime.datetime.strptime(request.POST.get('date_to'), '%Y-%m-%d')
        from_date = timezone.localtime(from_date)
        to_date = timezone.localtime(to_date)
        str_from_date = from_date.strftime("%d-%m-%Y")
        str_to_date = to_date.strftime("%d-%m-%Y")
        filename = f"{str_from_date} - {str_to_date}.xlsx"

        users = request.POST.get('users').split(',')
        users = [User.objects.get(id=user) for user in users if user]

        response = HttpResponse(
            funcs.get_xlsx(users, from_date, to_date),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
    request.session['error'] = 'NOT_LOGGED_ERROR'
    return redirect(router_routes['main'])
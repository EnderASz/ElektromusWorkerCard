from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils import timezone

from apps.backend.users.models import Worker, AdditionalWorkTime
from apps.frontend.router.routes import worker_routes
from apps.utils.errors import AuthError
from apps.utils import functions as funcs

# Create your views here.
def start_work_panel(request):
    if request.user.is_authenticated:
        request.session.set_expiry(300)
        worker = Worker.objects.filter(user = request.user).first()
        if not worker:
            return AuthError.not_personel(request)
        if worker.working:
            return redirect(worker_routes['finish_work_panel'])
        if funcs.worked(worker, timezone.localdate()):
            return redirect(worker_routes['add_work_time_panel'])
        return render(
            request,
            'apps/work_form/html/work_form.html',
            {
                'title': "Rozpocznij Pracę",
                'action': {
                    'name': 'start_work',
                    'url': 'back:users:start_work'
                },
                'logged_user': request.user
            })
    return AuthError.not_logged(request)

def finish_work_panel(request):
    if request.user.is_authenticated:
        request.session.set_expiry(300)
        worker = Worker.objects.filter(user = request.user).first()
        if not worker:
            return AuthError.not_personel(request)
        today_work = funcs.get_work(worker, timezone.localdate())
        if not worker.working:
            if not today_work[0]:
                return redirect(worker_routes['start_work_panel'])
            return redirect(worker_routes['add_work_time_panel'])
        return render(
            request,
            'apps/work_form/html/work_form.html',
            {
                'title': "Zakończ Pracę",
                'action': {
                    'name': 'finish_work',
                    'url': 'back:users:finish_work'
                },
                'work': {
                    'start': today_work[0].timestamp.strftime("%Y-%m-%dT%H:%M"),
                    'location': today_work[0].location
                },
                'logged_user': request.user
            })
    return AuthError.not_logged(request)

def add_work_time_panel(request):
    if request.user.is_authenticated:
        request.session.set_expiry(300)
        worker = Worker.objects.filter(user = request.user).first()
        if not worker:
            return AuthError.not_personel(request)
        if worker.working:
            return redirect(worker_routes['finish_work_panel'])
        today_work = funcs.get_work(worker, timezone.localdate())
        if today_work and today_work[0]:
            additional_time = AdditionalWorkTime.objects.filter(
                user=request.user,
                date=timezone.localdate()
                ).first()
            additional_time = additional_time.time_minutes if additional_time else 0
            return render(
                request,
                'apps/work_form/html/work_form.html',
                {
                    'title': "Dodaj Czas Pracy",
                    'action': {
                        'name': 'add_work_time',
                        'url': 'back:users:add_work_time'
                    },
                    'work': {
                        'start': today_work[0].timestamp.strftime("%Y-%m-%dT%H:%M"),
                        'finish': today_work[1].timestamp.strftime("%Y-%m-%dT%H:%M"),
                        'location': today_work[0].location,
                        'additional_time': f'{str(additional_time//60).zfill(2)}:{str(additional_time%60).zfill(2)}'
                    },
                    'logged_user': request.user
                })
        return redirect(worker_routes['start_work_panel'])
    return AuthError.not_logged(request)
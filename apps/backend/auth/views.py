from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from apps.frontend.router.routes import login_routes, router_routes
from apps.backend.users.models import Worker

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        request.session['username'] = request.POST.get('username')
        username = request.session['username']
        user = authenticate(
            request,
            username=username,
            password=request.POST.get('password')
            )
        if user is not None:
            login(request, user)
            if Worker.objects.filter(user=user).first():
                request.session.set_expiry(300)
            return redirect(router_routes['main'])
        else:
            try:
                user = User.objects.get(username__exact=username)
            except User.DoesNotExist:
                request.session['error'] = 'INVALID_VALUE_USERNAME_ERROR'
                return redirect(login_routes['login_panel'])
            if not user.check_password(request.POST.get('identificator')):
                    request.session['error'] = 'INVALID_VALUE_PASSWORD_ERROR'
                    return redirect(login_routes['login_panel'])
    login(request)
    return redirect(router_routes['main'])

def logout_view(request):
    logout(request)
    return redirect(router_routes['main'])
from django.core.exceptions import RequestDataTooBig
from django.shortcuts import redirect
from django.contrib.auth import logout

class AuthError:
    def __new__(cls, request):
        logout(request)
        request.session['error'] = "UNKNOWN_AUTH_ERROR"
        return redirect('front:router:main')

    @staticmethod
    def not_logged(request):
        request.session['error'] = 'NOT_LOGGED_ERROR'
        return redirect('front:router:main')

    @staticmethod
    def not_personel(request):
        logout(request)
        request.session['error'] = "NOT_PERSONEL_ERROR"
        return redirect('front:router:main')  

    @staticmethod
    def not_admin(request):
        request.session['error'] = "NOT_ADMIN_ERROR"
        return redirect('front:router:main')

    @staticmethod
    def session_expired(request):
        request.session['error'] = "SESSION_EXPIRED"
        return redirect('front:router:main')


class UserUpdateError:
    def __new__(cls, request):
        request.session['error'] = "UNKNOWS_USER_UPDATE_ERROR"
        return redirect('front:router:main')

    @staticmethod
    def blank_username(request):
        request.session['error'] = "BLANK_USERNAME_ERROR"
        return redirect('front:router:main')
from django.shortcuts import redirect, render
from . import constants as consts

# Create your views here.
def login_panel(request):
    if request.user.is_authenticated:
        return redirect('front:router:main')

    error = request.session.get('error')
    context = {
        'title': "Panel Logowania",
        'default_username': request.session.get('username', ""),
        'error': {'name': error, 'description': consts.ERRORS[error]} if error else None
    }
    
    if error:
        context.update({
            'error': {
                'name': error,
                'description': consts.ERRORS[error]
            }
        })
        del request.session['error']
    return render(
        request,
        'apps/work_form/html/login_form.html',
        context
    )
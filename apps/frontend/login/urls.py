from django.urls import path
from . import views

# BASE_URL/login
app_name = "login"
urlpatterns = [
    path('', views.login_panel, name='login')
]

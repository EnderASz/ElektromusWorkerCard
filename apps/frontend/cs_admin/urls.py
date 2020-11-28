from django.urls import path
from . import views

app_name = 'cs_admin'
urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('add-user/', views.add_user, name='add_user'),

    path('user/<int:pk>/manage', views.user_manage, name='manage_user'),
    path('user/<int:pk>/change-password', views.change_password, name='change_password'),
]

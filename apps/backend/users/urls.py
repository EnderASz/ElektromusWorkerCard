from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path('start-work/', views.start_work_view, name="start_work"),
    path('finish-work/', views.finish_work_view, name="finish_work"),
    path('add-work-time/', views.add_work_time_view, name="add_work_time"),

    path('user/<int:pk>/delete', views.delete_user_view, name='delete_user_view'),
    path('user/<int:pk>/update-password', views.updatePassword, name='update_password'),
    path('update', views.updateUserInfo, name="update_user"),
    path('action', views.group_action_view, name='group_action'),

    path('overview-download/', views.overview_download_view, name='overview_download_view')
]
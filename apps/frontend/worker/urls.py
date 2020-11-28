from django.urls import path

from . import views

app_name = "worker"
urlpatterns = [
    path('start-work/', views.start_work_panel, name="start_work"),
    path('finish-work/', views.finish_work_panel, name="finish_work"),
    path('add-work-time/', views.add_work_time_panel, name="add_work_time")
]


from django.urls import path, include
from . import views

app_name = "router"
urlpatterns = [
    path('', views.main_router_view),
    path('router', views.main_router_view, name="main"),
    path('router/worker/', views.worker_router_view, name="worker"),
    path('router/admin/', views.cs_admin_router_view, name="cs_admin"),
]

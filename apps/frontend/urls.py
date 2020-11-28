from django.urls import path, include

app_name = "front"
urlpatterns = [
    path('', include('apps.frontend.router.urls', namespace="router")),
    path('login/', include('apps.frontend.login.urls', namespace="login")),
    path('admin/', include('apps.frontend.cs_admin.urls', namespace="cs_admin")),
    path('worker/', include('apps.frontend.worker.urls', namespace="worker"))
]

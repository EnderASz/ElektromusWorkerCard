from django.urls import path, include

app_name = "back"
urlpatterns = [
    path('auth/', include('apps.backend.auth.urls', namespace="auth")),
    path('users/', include('apps.backend.users.urls', namespace="users"))
]
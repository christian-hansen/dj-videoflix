"""videoflix_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from users.views import ListUsers, LoginView, RegisterView, SetNewPasswordView, PasswordResetRequestView, ActivateAccountView, UsernameRequestView
from videoflix.views import ListVideos, ListGenres

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/login/', LoginView.as_view()),
    path('api/v1/register/', RegisterView.as_view(), name='register'),
    path('api/v1/activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate-account'),
    path('api/v1/users/', ListUsers.as_view()),
    path('api/v1/videos/', ListVideos.as_view(), name='list-videos'),  # For listing all videos
    path('api/v1/videos/<int:video_id>/', ListVideos.as_view(), name='get-video'),  # For getting a single video
    path('api/v1/genres/', ListGenres.as_view(), name='genre-list'),
    path('api/v1/password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('api/v1/username-reminder/', UsernameRequestView.as_view(), name='username-reminder'),
    path('api/v1/reset-password/<uidb64>/<token>/', SetNewPasswordView.as_view(), name='reset-password'),
    path('django-rq/', include('django_rq.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + debug_toolbar_urls()

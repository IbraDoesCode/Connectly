"""
URL configuration for connectly project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.users.urls import profile_patterns
from .views import  GoogleVerifyTokenView, LogoutView, CompleteSignupView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('apps.posts.urls')),
    path('users/', include('apps.users.urls')),
    path('profiles/', include((profile_patterns, 'apps.users.urls'), namespace='profiles')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('google/signin/', GoogleVerifyTokenView.as_view(), name='google_signin'),
    path('google/complete-signup/', CompleteSignupView.as_view(), name='google_complete_signup')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""social_network URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from profiles import views
from profiles.views import SignupEmail, LoginView, SignupPhone, verify

from .view import home_view
from django.contrib import admin
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('signup/', Signup, name='signup'),
    path('signup-email/', SignupEmail, name='signup-email'),
    path('signup-phone/', SignupPhone, name='signup-phone'),
    path('verify/', verify, name='verify'),
    path('reset/login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # reset password
    path('reset/', include('django.contrib.auth.urls')),  # password_reset/
    path('activate/<slug:uidb64>/<slug:token>/',
         views.activate, name='activate'),
    path('', home_view, name='home-view'),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('posts/', include('posts.urls', namespace='posts')),

]

# after adding the two lines below addresses run  collect static in the command line
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

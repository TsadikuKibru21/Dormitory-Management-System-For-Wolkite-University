"""DMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from .import views
from django.conf.urls.static import static
urlpatterns = [
    path('LAdmin/',include("account.urls"),name="Admin"),
    path('admin/', admin.site.urls),
    path('',views.index, name="index"),
    path('Login',views.login_view,name="login_view"),
    path('studentdean/',include('StudentDean.urls')),
    path('Student/',include('Student.urls')),
    path('Proctor/',include('Proctor.urls')),
    path('Supervisor/',include('Supervisor.urls')),
    path('Registrar/',include('Registrar.urls')),
    path('President/',include('President.urls')),
    path('',include('chat.urls')),
    path('forget_password',views.forget_password, name="forget_password"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

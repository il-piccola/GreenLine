"""GreenLine URL Configuration

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
from django import views
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import static
from .settings import *
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login, name="login"),
    path('main', main, name="main"),
    path('show_file', show_file, name="show_file"),
    path('change_password', change_password, name="change_password"),
    path('admin_login', admin_login, name="admin_login"),
    path('admin_main', admin_main, name="admin_main"),
    path('show_employees', show_employees, name="show_employees"),
    path('add_employee', add_employee, name="add_employee"),
    path('add_file', add_file, name="add_file"),
    path('show_files', show_files, name="show_files"),
]
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

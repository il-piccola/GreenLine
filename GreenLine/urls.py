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
    path('employee/<int:id>/<int:edit>', employee, name="employee"),
    path('add_employee', add_employee, name="add_employee"),
    path('add_file', add_file, name="add_file"),
    path('show_files', show_files, name="show_files"),
    path('del_file/<int:id>', del_file, name="del_file"),
    path('show_organization', show_organization, name="show_organization"),
    path('add_organization', add_organization, name="add_organization"),
    path('organization/<int:id>/<int:edit>', organization, name="organization"),
    path('show_shipper', show_shipper, name="show_shipper"),
    path('add_shipper', add_shipper, name="add_shipper"),
    path('shipper/<int:id>/<int:edit>', shipper, name="shipper"),
    path('show_consignee', show_consignee, name="show_consignee"),
    path('add_consignee', add_consignee, name="add_consignee"),
    path('consignee/<int:id>/<int:edit>', consignee, name="consignee"),
    path('get_cities', get_cities, name="get_cities"),
    path('get_towns', get_towns, name="get_towns"),
    path('get_address_from_zip', get_address_from_zip, name="get_address_from_zip"),
    path('get_consignees', get_consignees, name="get_consignees"),
    path('get_consignees_from_shipper', get_consignees_from_shipper, name="get_consignees_from_shipper"),
    path('get_phone', get_phone, name="get_phone"),
    path('get_zip', get_zip, name="get_zip"),
    path('get_prefectures_from_shipper', get_prefectures_from_shipper, name="get_prefectures_from_shipper"),
    path('get_cities_from_shipper', get_cities_from_shipper, name="get_cities_from_shipper"),
    path('get_towns_from_shipper', get_towns_from_shipper, name="get_towns_from_shipper"),
    path('get_consignees_from_shipper', get_consignees_from_shipper, name="get_consignees_from_shipper"),
]
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

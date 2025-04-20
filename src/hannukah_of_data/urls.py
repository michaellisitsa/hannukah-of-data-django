"""
URL configuration for hannukah_of_data project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("day01/", views.day01, name="day01"),
    path("day02/", views.day02, name="day02"),
    path("day02_alt/", views.day02_alt, name="day02_alt"),
    path("day02_fk/", views.day02_fk, name="day02_fk"),
    path("day03/", views.day03, name="day03"),
    path("day04/", views.day04, name="day04"),
]

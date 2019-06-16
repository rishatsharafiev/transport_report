"""Urls"""

from conf import settings
from django.contrib import admin
from django.urls import include, path

from .views import some_report


urlpatterns = [
    path('some_report/', some_report),
]


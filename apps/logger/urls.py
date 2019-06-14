
from django.urls import path

from .views.log_list import LogListView


urlpatterns = (
    path('', LogListView.as_view(), name='log-list'),
)

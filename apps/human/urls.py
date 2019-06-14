from django.urls import include, path
from django.views import generic

from . import views


urlpatterns = [
    # path('', generic.TemplateView.as_view(template_name="human/index.html"), name="index"),
    path('', generic.RedirectView.as_view(url='./human', permanent=False), name="index"),
    path('human/', include(views.HumanViewSet().urls)),
]

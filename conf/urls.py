"""Urls"""

from conf import settings
from django.contrib import admin
from django.urls import include, path, re_path

from .views import setdata
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="manage/index.html")),
    path('jet/', include('jet.urls', 'jet')),
    # path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', admin.site.urls),
    path('manage/', include('apps.manage.urls')),
    re_path(r'^set/[a-z]+$', setdata),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

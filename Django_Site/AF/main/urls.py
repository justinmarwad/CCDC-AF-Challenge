from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, re_path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^(?!/static/.*)(?P<path>.*\..*)$', RedirectView.as_view(url='/static/%(path)s')),
]  

if settings.DEBUG == True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
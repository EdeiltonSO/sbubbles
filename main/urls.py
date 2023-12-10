from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from app.views import timeline

urlpatterns = [
    # path('', include('app.urls')),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', timeline, name='timeline')
]

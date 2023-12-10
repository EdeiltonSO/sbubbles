from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from app.views import home

urlpatterns = [
    # path('', include('app.urls')),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', home, name='home')
]

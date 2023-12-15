from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView
from app.views import home
from app.views import SignUpView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include([
        path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
        path('', include('django.contrib.auth.urls')),
    ])),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', home, name='home'),
]
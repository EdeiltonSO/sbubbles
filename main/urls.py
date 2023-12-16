from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView
from app.views import home, SignUpView, create_post, delete_post, like, repost, save

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include([
        path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
        path('', include('django.contrib.auth.urls')),
    ])),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', home, name='home'),
    path('post/create', create_post, name='create_post'),
    path('post/<post_id>/delete', delete_post, name='delete_post'),

    path('post/<post_id>/like', like, name='like'),
    path('post/<post_id>/repost', repost, name='repost'),
    path('post/<post_id>/save', save, name='save'),
]
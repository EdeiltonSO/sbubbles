from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView
from app.views import home, SignUpView, create, delete, like, repost, save, report, profile, follow, likes, collection, notifications, mark_as_checked, update

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include([
        path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
        path('', include('django.contrib.auth.urls')),
    ])),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', home, name='home'),

    path('post/create', create, name='create'),
    path('post/<post_id>/delete', delete, name='delete'),
    path('post/<post_id>/like', like, name='like'),
    path('post/<post_id>/repost', repost, name='repost'),
    path('post/<post_id>/save', save, name='save'),
    path('post/<post_id>/report', report, name='report'),

    path('user/<username>', profile, name='profile'),
    path('user/<username>/follow', follow, name='follow'),
    path('user/<username>/likes', likes, name='likes'),
    path('collection', collection, name='collection'),
    path('editprofile', update, name='update'),

    path('notifications', notifications, name='notifications'),
    path('notifications/<notif_id>/mark_as_checked', mark_as_checked, name='mark_as_checked'),
]
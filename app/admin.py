from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post, Like, Repost, Save, Follow, Report, Notification, CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = (
        'id', 'email', 'username', 'password', 'first_name', 'last_name', 'followers', 'following', 'bio', 'birthdate', 'created_at', 'suspended_at', 'is_staff'
        )

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Repost)
admin.site.register(Save)
admin.site.register(Follow)
admin.site.register(Report)
admin.site.register(Notification)
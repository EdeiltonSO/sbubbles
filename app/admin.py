from django.contrib import admin

from .models import Post, Like, Repost, Save, Follow, Report, Notification #, User

# admin.site.register(User)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Repost)
admin.site.register(Save)
admin.site.register(Follow)
admin.site.register(Report)
admin.site.register(Notification)
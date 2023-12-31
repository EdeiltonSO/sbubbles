import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bio = models.CharField(max_length=128, null=True)
    following = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    birthdate = models.DateField("Data de nascimento", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    suspended_at = models.DateTimeField(null=True)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    content = models.CharField(max_length=140, null=False)
    replies_to = models.UUIDField(null=True)
    likes = models.IntegerField(default=0)
    reports = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Repost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Save(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='follower')
    followed = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='followed')
    created_at = models.DateTimeField(auto_now_add=True)

class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    whistleblower = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    reported_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    ACTION_CHOICES = (("F", "Follow"), ("L", "Like"), ("R", "Repost"), ("P", "Reply"))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='sender')
    action_type = models.CharField(max_length=1, choices=ACTION_CHOICES, blank=False, null=False)
    action_link = models.CharField(max_length=128, null=False)
    post_owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='owner')
    message = models.CharField(max_length=128, null=False)
    was_viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

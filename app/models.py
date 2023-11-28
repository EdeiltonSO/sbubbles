import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usertitle = models.CharField(max_length=32, null=False)
    bio = models.CharField(max_length=128, null=True)
    birthdate = models.DateField("Data de nascimento", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    suspended_at = models.DateTimeField(null=True)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    content = models.CharField(max_length=140, null=False)
    replies_to = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Repost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Save(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follower_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='follower')
    followed_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='followed')
    created_at = models.DateTimeField(auto_now_add=True)

class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    whistleblower_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    reported_post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    ACTION_CHOICES = (("L", "Like"), ("R", "Repost"), ("P", "Post"))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='sender')
    action_type = models.CharField(max_length=1, choices=ACTION_CHOICES, blank=False, null=False)
    action_link = models.CharField(max_length=128, null=False)
    target_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    post_owner_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='owner')
    was_viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

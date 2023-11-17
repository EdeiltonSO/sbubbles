from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=64, unique=True, null=False)
    password = models.CharField(max_length=128, null=False)  # recebe senha criptografada
    username = models.CharField(max_length=24, unique=True, null=False)
    usertitle = models.CharField(max_length=32, null=False)
    bio = models.CharField(max_length=128, null=True)
    birthdate = models.DateField("Data de nascimento")
    created_at = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    content = models.CharField(max_length=140, null=False)
    replies_to = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
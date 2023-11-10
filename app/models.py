from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=64, unique=True)
    password = models.CharField(max_length=128)  # recebe senha criptografada
    username = models.CharField(max_length=24, unique=True)
    usertitle = models.CharField(max_length=32)
    bio = models.CharField(max_length=128)
    birthdate = models.DateField("Data de nascimento")
    created_at = models.DateTimeField(auto_now_add=True)
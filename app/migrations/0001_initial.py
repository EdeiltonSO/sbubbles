# Generated by Django 3.2.4 on 2023-11-10 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=64, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('username', models.CharField(max_length=24, unique=True)),
                ('usertitle', models.CharField(max_length=32)),
                ('bio', models.CharField(max_length=128)),
                ('birthdate', models.DateField(verbose_name='Data de nascimento')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

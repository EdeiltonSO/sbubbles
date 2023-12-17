from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    birthdate = forms.DateField(
        label='Data de nascimento',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'birthdate', 'username', 'password1', 'password2')

class CustomUserUpdateForm(UserCreationForm):
    birthdate = forms.DateField(
        label='Data de nascimento',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'bio', 'email', 'birthdate', 'username')
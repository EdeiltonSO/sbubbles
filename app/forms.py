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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adicione placeholders para outros campos, se necessário
        self.fields['first_name'].widget.attrs['placeholder'] = 'Seu Nome'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Seu Sobrenome'
        self.fields['email'].widget.attrs['placeholder'] = 'SeuEmail@example.com'
        self.fields['username'].widget.attrs['placeholder'] = 'Nome de Usuário'
        self.fields['password1'].widget.attrs['placeholder'] = 'Senha'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirme a Senha'

class CustomUserUpdateForm(UserCreationForm):
    birthdate = forms.DateField(
        label='Data de nascimento',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'bio', 'email', 'birthdate', 'username')
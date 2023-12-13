from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from app.forms import CustomUserCreationForm
    
@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
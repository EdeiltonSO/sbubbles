from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from app.forms import CustomUserCreationForm
from app.models import Post

@login_required(login_url='login')
def home(request):
    if request.method == 'GET':
        posts = Post.objects.order_by('-created_at')
        context = {'posts': posts}
        # for post in posts:
        #     print('\033[0;34m'+post.content+'\033[m')

    return render(request, 'home.html', context)

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')

        novo_post = Post.objects.create(
            author = request.user,
            content = content,
        )
    return redirect('home')

@login_required(login_url='login')
def delete_post(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    post.delete()
    # print('\033[0;31mO post "'+post.content+'" foi apagado\033[m')
    return redirect('home')
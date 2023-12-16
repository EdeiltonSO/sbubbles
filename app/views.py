from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from app.forms import CustomUserCreationForm
from app.models import Post, Like, Repost, Save

@login_required(login_url='login')
def home(request):
    posts = None

    if request.method == 'GET':
        posts = Post.objects.order_by('-created_at')
        for post in posts:
            try:
                like = Like.objects.get(author = request.user, post = post)
                post.liked_by_authenticated_user = True
            except Like.DoesNotExist:
                post.liked_by_authenticated_user = False
            try:
                repost = Repost.objects.get(author = request.user, post = post)
                post.reposted_by_authenticated_user = True
            except Repost.DoesNotExist:
                post.reposted_by_authenticated_user = False
            try:
                save = Save.objects.get(author = request.user, post = post)
                post.saved_by_authenticated_user = True
            except Save.DoesNotExist:
                post.saved_by_authenticated_user = False

    context = {'posts': posts}
    return render(request, 'home.html', context)

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')

        Post.objects.create(
            author = request.user,
            content = content,
        )
    return redirect('home')

@login_required(login_url='login')
def delete_post(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    if request.user == post.author:
        post.delete()
    # print('\033[0;31mO post "'+post.content+'" foi apagado\033[m')
    return redirect('home')

@login_required(login_url='login')
def like(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    try:
        like = Like.objects.get(author = request.user, post = post)
        like.delete()
        post.likes -= 1
    except Like.DoesNotExist:
        Like.objects.create(
            author = request.user,
            post = post,
        )
        post.likes += 1
    
    post.save()
    return redirect('home')

@login_required(login_url='login')
def repost(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    try:
        repost = Repost.objects.get(author = request.user, post = post)
        repost.delete()
    except Repost.DoesNotExist:
        Repost.objects.create(
            author = request.user,
            post = post,
        )
    
    return redirect('home')

@login_required(login_url='login')
def save(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    try:
        save = Save.objects.get(author = request.user, post = post)
        save.delete()
    except Save.DoesNotExist:
        Save.objects.create(
            author = request.user,
            post = post,
        )
    
    return redirect('home')
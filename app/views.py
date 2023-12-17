from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.http import Http404
from app.forms import CustomUserCreationForm, CustomUserUpdateForm
from app.models import Post, Like, Repost, Save, Report, CustomUser, Follow, Notification
from itertools import chain

@login_required(login_url='login')
def home(request):
    posts = []
    followed_users = []

    try:
        following = Follow.objects.filter(follower = request.user)
    except Follow.DoesNotExist:
        following = []

    for f in following:
        followed_users.append(f.followed)
    followed_users.append(request.user)

    if request.method == 'GET':
        posts = Post.objects.filter(author__in = followed_users).order_by('-created_at')

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
            try:
                report = Report.objects.get(whistleblower = request.user, reported_post = post)
                post.reported_by_authenticated_user = True
            except Report.DoesNotExist:
                post.reported_by_authenticated_user = False

    context = {'posts': posts}
    return render(request, 'home.html', context)

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@login_required(login_url='login')
def create(request):
    if request.method == 'POST':
        content = request.POST.get('content')

        Post.objects.create(
            author = request.user,
            content = content,
        )
    return redirect('home')

@login_required(login_url='login')
def delete(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    if request.user == post.author:
        post.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

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
        if request.user != post.author:
            Notification.objects.create(
                sender = request.user,
                action_type = 'L',
                action_link = '',
                message = str(request.user.username)+' curtiu seu post "'+str(post.content)+'"',
                post_owner = post.author,
            )

    post.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

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
        if request.user != post.author:
            Notification.objects.create(
                sender = request.user,
                action_type = 'R',
                action_link = '',
                message = str(request.user.username)+' repostou "'+str(post.content)+'"',
                post_owner = post.author,
            )

    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

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
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required(login_url='login')
def report(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    try:
        report = Report.objects.get(whistleblower = request.user, reported_post = post)
        post.reports -= 1
        report.delete()
    except Report.DoesNotExist:
        Report.objects.create(
            whistleblower = request.user,
            reported_post = post,
        )
        post.reports += 1
    
    post.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def profile(request, username):
    user = get_object_or_404(CustomUser, username = username)
    try:
        posts = Post.objects.filter(author = user)
    except Post.DoesNotExist:
        posts = []

    try:
        reposts = Repost.objects.filter(author = user)
    except Post.DoesNotExist:
        reposts = []
    
    reposted_posts = []
    for r in reposts:
        reposted_post = Post.objects.get(id = r.post.id)
        reposted_posts.append(reposted_post)

    all_posts = sorted(
        chain(posts, reposted_posts),
        key=lambda item: item.created_at,
        reverse=True
    )

    if request.user.is_authenticated:
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
            try:
                report = Report.objects.get(whistleblower = request.user, reported_post = post)
                post.reported_by_authenticated_user = True
            except Report.DoesNotExist:
                post.reported_by_authenticated_user = False


        follow = None
        try:
            follow = Follow.objects.filter(follower = request.user, followed = user)
        except Follow.DoesNotExist:
            follow = None

        try:
            likes = Like.objects.filter(author = user)
        except Like.DoesNotExist:
            like = []

        try:
            saved = Save.objects.filter(author = user)
        except Save.DoesNotExist:
            saved = []

        context = {
            'user': user,
            'all_posts': all_posts,
            'likes': likes,
            'saved': saved,
            'follow': follow
        }

        return render(request, 'fullprofile.html', context)
    else:
        context = {'user': user, 'all_posts': all_posts}
        return render(request, 'publicprofile.html', context)

@login_required(login_url='login')
def follow(request, username):
    user = get_object_or_404(CustomUser, username = username)
    
    follow = Follow.objects.filter(follower = request.user, followed = user)
    print(follow)
    if follow:
        follow.delete()
        request.user.following -= 1
        user.followers -= 1
    else:
        Follow.objects.create(
            follower = request.user, 
            followed = user
        )
        request.user.following += 1
        user.followers += 1
        if request.user != user:
            Notification.objects.create(
                sender = request.user,
                action_type = 'F',
                action_link = '',
                message = str(request.user.username)+' começou a seguir você!',
                post_owner = user,
            )

    request.user.save()
    user.save()

    return redirect('profile', username = user.username)
    
@login_required(login_url='login')
def likes(request, username):
    posts = []
    user = CustomUser.objects.get(username = username)
    likes = Like.objects.filter(author = user).order_by('-created_at')

    # código replicado a partir daqui
    for like in likes:
        posts.append(like.post)

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
        try:
            report = Report.objects.get(whistleblower = request.user, reported_post = post)
            post.reported_by_authenticated_user = True
        except Report.DoesNotExist:
            post.reported_by_authenticated_user = False

    follow = None
    try:
        follow = Follow.objects.filter(follower = request.user, followed = user)
    except Follow.DoesNotExist:
        follow = None
    # código replicado até daqui

    context = {
        'user': user,
        'follow': follow,
        'posts': posts
    }

    return render(request, 'likes.html', context)

@login_required(login_url='login')
def collection(request):
    posts = []
    saved = Save.objects.filter(author = request.user).order_by('-created_at')

    # código replicado a partir daqui
    for save in saved:
        posts.append(save.post)

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
        try:
            report = Report.objects.get(whistleblower = request.user, reported_post = post)
            post.reported_by_authenticated_user = True
        except Report.DoesNotExist:
            post.reported_by_authenticated_user = False
    # código replicado até daqui

    return render(request, 'collection.html', { 'posts': posts })

@login_required(login_url='login')
def notifications(request):
    notifications = Notification.objects.filter(post_owner = request.user).order_by('-created_at')
    return render(request, 'notifications.html', { 'notifications': notifications })

@login_required(login_url='login')
def mark_as_checked(request, notif_id):
    try:
        notif = Notification.objects.get(pk=notif_id)
        notif.was_viewed = True
        notif.save()
    except Notification.DoesNotExist:
        raise Http404("Notificação não encontrada!")
    
    notifications = Notification.objects.filter(post_owner = request.user).order_by('-created_at')
    return render(request, 'notifications.html', { 'notifications': notifications })

@login_required(login_url='login')
def update(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserUpdateForm(instance=request.user)

    return render(request, 'updateuser.html', {'form': form})
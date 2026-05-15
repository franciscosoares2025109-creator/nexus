from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Post, Comment, Like, Profile
from .forms import PostForm, CommentForm, RegisterForm, ProfileForm


def feed(request):
    posts = Post.objects.select_related('author', 'author__profile').prefetch_related('likes', 'comments')

    if request.method == 'POST' and request.user.is_authenticated:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Publicação criada com sucesso!')
            return redirect('feed')
    else:
        form = PostForm()

    for post in posts:
        post.liked_by_user = post.is_liked_by(request.user)

    return render(request, 'social/feed.html', {'posts': posts, 'form': form})


def post_detail(request, post_id):
    post = get_object_or_404(Post.objects.select_related('author', 'author__profile'), id=post_id)
    comments = post.comments.select_related('author', 'author__profile')
    post.liked_by_user = post.is_liked_by(request.user)

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comentário adicionado!')
            return redirect('post_detail', post_id=post_id)
    else:
        comment_form = CommentForm()

    return render(request, 'social/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })


def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = profile_user.posts.prefetch_related('likes', 'comments')

    for post in posts:
        post.liked_by_user = post.is_liked_by(request.user)

    profile, _ = Profile.objects.get_or_create(user=profile_user)

    edit_form = None
    if request.user == profile_user:
        if request.method == 'POST':
            edit_form = ProfileForm(request.POST, request.FILES, instance=profile)
            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, 'Perfil atualizado!')
                return redirect('user_profile', username=username)
        else:
            edit_form = ProfileForm(instance=profile)

    return render(request, 'social/profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'posts': posts,
        'edit_form': edit_form,
    })


@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({'liked': liked, 'count': post.get_like_count()})


@login_required
@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    messages.success(request, 'Publicação apagada.')
    return redirect('feed')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('feed')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Bem-vindo ao Nexus, {user.username}!')
            return redirect('feed')
    else:
        form = RegisterForm()

    return render(request, 'social/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('feed')
        else:
            messages.error(request, 'Credenciais inválidas.')

    return render(request, 'social/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
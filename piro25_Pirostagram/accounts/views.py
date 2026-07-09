from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Q

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('posts:main')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('posts:main')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('accounts:login')


@login_required
def profile(request, username):
    profile_user = get_object_or_404(get_user_model(), username=username)
    posts = profile_user.posts.all().order_by('-created_at')
    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        'posts': posts,
    })

@login_required
def follow(request, username):
    target = get_object_or_404(get_user_model(), username=username)
    if target == request.user:
        return redirect('accounts:profile', username=username)
    if target in request.user.followings.all():
        request.user.followings.remove(target)
    else:
        request.user.followings.add(target)
    return redirect('accounts:profile', username=username)

@login_required
def search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = get_user_model().objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query)
        ).exclude(pk=request.user.pk)
    return render(request, 'accounts/search.html', {
        'query': query,
        'results': results,
    })
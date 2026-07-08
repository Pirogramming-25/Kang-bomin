from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Story, StoryImage
from .forms import PostForm
from django.http import JsonResponse

@login_required
def main(request):
    following_users = list(request.user.followings.all()) + [request.user]
    posts = Post.objects.filter(author__in=following_users)

    sort = request.GET.get('sort')
    if sort == 'like':
        posts = posts.annotate(cnt=Count('like_users')).order_by('-cnt')
    elif sort == 'comment':
        posts = posts.annotate(cnt=Count('comments')).order_by('-cnt')
    else:
        posts = posts.order_by('-created_at')

    stories = []
    for u in following_users:
        latest = u.stories.order_by('-created_at').first()
        if latest:
            stories.append(latest)

    suggestions = get_user_model().objects.exclude(pk=request.user.pk)[:5]

    return render(request, 'posts/main.html', {'posts': posts, 'stories': stories, 'suggestions': suggestions})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:main')
    else:
        form = PostForm()
    return render(request, 'posts/post.html', {'form': form})


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('posts:main')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:main')
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        post.delete()
    return redirect('posts:main')


@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
        liked = False
    else:
        post.like_users.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'count': post.like_users.count()})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})


@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
    return redirect('posts:post_detail', pk=pk)


@login_required
def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return redirect('posts:post_detail', pk=comment.post.pk)
    if request.method == 'POST':
        comment.content = request.POST.get('content')
        comment.save()
        return redirect('posts:post_detail', pk=comment.post.pk)
    return render(request, 'posts/comment.html', {'comment': comment})


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author == request.user:
        comment.delete()
    return redirect('posts:post_detail', pk=comment.post.pk)


@login_required
def story_create(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        if images:
            story = Story.objects.create(author=request.user)
            for img in images:
                story.images.create(image=img)
        return redirect('posts:main')
    return render(request, 'posts/story.html')


@login_required
def story_detail(request, pk):
    story = get_object_or_404(Story, pk=pk)
    story_images = StoryImage.objects.filter(
        story__author=story.author
    ).order_by('story__created_at', 'pk')
    return render(request, 'posts/story_detail.html', {
        'story': story,
        'story_images': story_images,
    })
from django.shortcuts import render, get_object_or_404, redirect
from .models import Review

def review_list(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'reviews/review_detail.html', {'review': review})

def review_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        year = request.POST.get('year')
        genre = request.POST.get('genre')
        score = request.POST.get('score')
        director = request.POST.get('director')
        actor = request.POST.get('actor')
        running_time = request.POST.get('running_time')
        content = request.POST.get('content')
        poster = request.POST.get('poster')
        Review.objects.create(title=title, year=year, genre=genre, score=score, director=director, actor=actor, running_time=running_time, content=content)
        return redirect('review_list')
    return render(request, 'reviews/review_form.html')

def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.title = request.POST.get('title')
        review.year = request.POST.get('year')
        review.genre = request.POST.get('genre')
        review.score = request.POST.get('score')
        review.director = request.POST.get('director')
        review.actor = request.POST.get('actor')
        review.running_time = request.POST.get('running_time')
        review.content = request.POST.get('content')
        if 'poster' in request.FILES:
            review.poster = request.FILES['poster']
        review.save()
        return redirect('review_detail', pk=pk)
    return render(request, 'reviews/review_form.html', {'review': review})

def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('review_list')
    return redirect('review_detail', pk=pk)

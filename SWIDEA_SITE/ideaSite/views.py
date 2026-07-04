from django.shortcuts import render, redirect, get_object_or_404
from .models import Idea, DevTool, IdeaStar
from django.db.models import Count
import json
from django.http import JsonResponse

def list(request):
    sort = request.GET.get('sort', 'recent')
    
    if sort == 'name':
        ideas = Idea.objects.order_by('title')
    elif sort == 'old':
        ideas = Idea.objects.order_by('created_at')
    elif sort == 'interest':
        ideas = Idea.objects.order_by('-interest')
    elif sort == 'star':
        ideas = Idea.objects.annotate(star_count = Count('star')).order_by('-star_count')
    else:
        ideas = Idea.objects.order_by('-created_at')
    return render(request, 'ideaSite/list.html', {'ideas': ideas, 'sort': sort})

def add(request):
    if request.method == 'POST':
        idea = Idea.objects.create(
            title = request.POST['title'],
            image = request.FILES['image'],
            content = request.POST['content'],
            interest = request.POST.get('interest', 0),
            devtool_id = request.POST['devtool'],
        )
        return redirect('detail', id = idea.id)
    devtools = DevTool.objects.all()
    return render(request, 'ideaSite/add.html', {'devtools': devtools})

def detail(request, id):
    idea = get_object_or_404(Idea, id = id)
    return render(request, 'ideaSite/detail.html', {'idea': idea})

def modify(request, id):
    idea = get_object_or_404(Idea, id = id)
    if request.method == 'POST':
        idea.title = request.POST['title']
        idea.content = request.POST['content']
        idea.interest = request.POST.get('interest', 0)
        idea.devtool_id = request.POST['devtool']
        if 'image' in request.FILES:
            idea.image = request.FILES['image']
        idea.save()
        return redirect('detail', id = idea.id)
    devtools = DevTool.objects.all()
    return render(request, 'ideaSite/modify.html', {'idea': idea, 'devtools': devtools})

def delete(request, id):
    idea = get_object_or_404(Idea, id = id)
    idea.delete()
    return redirect('list')

def toolList(request):
    devtools = DevTool.objects.all()
    return render(request, 'ideaSite/toolList.html', {'devtools': devtools})

def toolAdd(request):
    if request.method == 'POST':
        devtool = DevTool.objects.create(
            name = request.POST['name'],
            kind = request.POST['kind'],
            content = request.POST['content']
        )
        return redirect('toolDetail', id = devtool.id)
    devtools = DevTool.objects.all()
    return render(request, 'ideaSite/toolAdd.html', {'devtools': devtools})


def toolDetail(request, id):
    devtool = get_object_or_404(DevTool, id = id)
    return render(request, 'ideaSite/toolDetail.html', {'devtool': devtool})

def toolModify(request, id):
    devtool = get_object_or_404(DevTool, id = id)
    if request.method == 'POST':
        devtool.name = request.POST['name']
        devtool.kind = request.POST['kind']
        devtool.content = request.POST['content']
        devtool.save()
        return redirect('toolDetail', id = devtool.id)
    return render(request, 'ideaSite/toolModify.html', {'devtool': devtool})

def toolDelete(request, id):
    devtool = get_object_or_404(DevTool, id = id)
    devtool.delete()
    return redirect('toolList')

def interest_update(request, id):
    if request.method == 'POST':
        idea = get_object_or_404(Idea, id = id)
        data = json.loads(request.body)
        if data['action'] == 'plus':
            idea.interest += 1
        elif data['action'] == 'minus':
            idea.interest -= 1
        idea.save()
        return JsonResponse({'interest': idea.interest})
    return JsonResponse({'error': 'POST only'}, status=405)

def star_toggle(request, id):
    if request.method == 'POST':
        idea = get_object_or_404(Idea, id = id)
        star = IdeaStar.objects.filter(idea = idea)
        if star.exists():
            star.delete()
            starred = False
        else:
            IdeaStar.objects.create(idea = idea)
            starred = True
        return JsonResponse({'starred': starred})
    return JsonResponse({'error': 'POST only'}, status=405)
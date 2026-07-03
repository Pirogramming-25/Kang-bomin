from django.shortcuts import render, redirect, get_object_or_404
from .models import Idea, DevTool, IdeaStar

def list(request):
    ideas = Idea.objects.order_by('-created_at')
    return render(request, 'ideaSite/list.html', {'ideas': ideas})

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
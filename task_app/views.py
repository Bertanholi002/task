from django.shortcuts import render, get_object_or_404, redirect
from task_app.models import Task
from .forms import TaskForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'task_app/index.html')

@login_required
def tasks(request):
    tasks = Task.objects.filter(owner=request.user).order_by('created_at')
    context = {'tasks': tasks}
    return render(request, 'task_app/tasks.html', context)

@login_required
def task(request, task_id):
    task = Task.objects.get(id = task_id)
    if task.owner != request.user:
        raise Http404
    context = {'task_title': task.title, 'task_description': task.description}  
    return render(request, 'task_app/task.html', context)

@login_required
def new_task(request):
    if request.method != 'POST':
        form = TaskForm()
    else:
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()  
            return HttpResponseRedirect(reverse('tasks'))  

    context = {'form': form}
    return render(request, 'task_app/new_task.html', context) 

@login_required
def edit_task(request, task_id):
    task = Task.objects.get(id = task_id)

    if task.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        form = TaskForm(instance=task)
    else:
        form = TaskForm(instance=task, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('task', args=[task.id]))
    context = {'form': form, 'task': task}
    return render(request, 'task_app/edit_task.html', context)

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.delete()
        return redirect('tasks')  
    
    return render(request, 'task_app/delete_task.html', {'task': task})
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import LoginTable, Task, Notification
from django.contrib.auth import login, logout
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User


# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = LoginTable.objects.filter(UserName = username, password = password).first()
        if user:
            user.is_active = True
            user.save()
            request.session['user_id'] = user.id
            return redirect('viewTask')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, "login.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            LoginTable.objects.create(
                UserName = username,
                password = password,
                email = email,
                is_active = True
            )
            return redirect('login')
        else:
            return render(request, 'signup.html', {'error_message' : "Password do not match"})
    return render(request, "signup.html")

def addTask(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST.get('description', '')
        due_date = request.POST['due_date']
        user = LoginTable.objects.get(id = request.session['user_id'])
        Task.objects.create(
            user = user,
            title = title,
            description = description,
            completed = False,
            created_at = datetime.now(),
            due_date = due_date
        )
        return redirect('viewTask')
    return render(request, "addTask.html")

def viewTask(request):
    if 'user_id' not in request.session:
        return redirect('login')
    user = LoginTable.objects.get(id = request.session['user_id'])
    tasks = Task.objects.filter(user = user).order_by('due_date')
    return render(request, "viewTask.html", {'tasks': tasks})

def viewNoti(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    user_id = request.session['user_id']
    user = LoginTable.objects.get(id=user_id)
    
    # Fetch upcoming tasks for the user
    now = timezone.now()
    upcoming_tasks = Task.objects.filter(user=user, due_date__gt=now, due_date__lt=now + timedelta(hours=24))
    
    # Only create a new notification if there isn't one for the task yet
    for task in upcoming_tasks:
        if not Notification.objects.filter(task=task, user=user, type='Task Due Soon').exists():
            Notification.objects.create(
                user=user,
                task=task,
                message=f"Reminder: Your task '{task.title}' is due soon on {task.due_date}.",
                type='Task Due Soon'
            )
    
    # Fetch notifications that are not marked as read
    notifications = Notification.objects.filter(user=user).order_by('created_at')

    # Handle form submission for marking notifications as read
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        if notification_id:
            try:
                notification = Notification.objects.get(id=notification_id)
                
                # Update read status to True, but avoid creating duplicates
                if not notification.read:
                    notification.read = True
                    notification.save()
                    # Ensure no duplicate notifications are created by checking again
                    notifications = Notification.objects.filter(user=user).order_by('created_at')

            except Notification.DoesNotExist:
                pass

    # Render notifications page with updated notifications
    return render(request, "viewNoti.html", {'notifications': notifications})



def user_logout(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = LoginTable.objects.get(id = user_id)
        user.is_active = False
    logout(request)
    return redirect('login')

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        completed = 'completed' in request.POST
        task.title = title
        task.description = description
        task.due_date = due_date
        task.completed = completed
        task.save()
        return redirect('viewTask')
    return render(request, "edit_task.html", {'task' : task})

def delete_task(request, task_id):
    if 'user_id' not in request.session:
        return redirect('login')
    task = get_object_or_404(Task, id=task_id)
    if task.user.id == request.session['user_id']:
        task.delete()
        return redirect('viewTask')
    else:
        return redirect('home')


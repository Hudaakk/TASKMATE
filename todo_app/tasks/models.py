from django.db import models

# Create your models here.

class LoginTable(models.Model):
    UserName = models.CharField(max_length=60)
    password=models.CharField(max_length=80)
    email=models.CharField(max_length=80)
    is_active=models.BooleanField(default=False)


class Task(models.Model):
    user = models.ForeignKey(LoginTable, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)

class Notification(models.Model):
    user = models.ForeignKey(LoginTable, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50, default="remainder")

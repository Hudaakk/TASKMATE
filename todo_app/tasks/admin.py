from django.contrib import admin
from .models import LoginTable, Task, Notification  # Import your models

# Register your models here
admin.site.register(LoginTable)
admin.site.register(Task)
admin.site.register(Notification)

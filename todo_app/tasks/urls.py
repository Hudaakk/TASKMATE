from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),

    path('signup', views.signup, name='signup'),

    path('addTask', views.addTask, name='addTask'),

    path('viewTask', views.viewTask, name='viewTask'),

    path('viewNoti', views.viewNoti, name='viewNoti'),
    
    path('user_logout', views.user_logout, name='user_logout'),

    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),

    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
]
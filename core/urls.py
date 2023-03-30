from django.contrib import admin
from django.urls import path
from api.views import get_tasks, get_task_id, completed_task, incompleted_task, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', get_tasks),
    path('tasks/<int:pk>', get_task_id),
    path('tasks/completed', completed_task),
    path('tasks/incompleted', incompleted_task),
    path('home/', home)
]
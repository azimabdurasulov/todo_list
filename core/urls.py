from django.contrib import admin
from django.urls import path
from api.views import tasks

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', tasks)
]
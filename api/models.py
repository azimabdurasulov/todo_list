from django.db import models
from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Task(models.Model):
    task = models.CharField(max_length=50)
    description = models.TextField()
    complited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
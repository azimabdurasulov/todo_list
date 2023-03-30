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

    def to_dict(self):
        returned = {
            'id': self.id,
            'task': self.task,
            'description': self.description,
            'complited': self.complited,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'student_id': self.student_id
        }
        return returned
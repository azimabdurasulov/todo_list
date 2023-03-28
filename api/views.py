from django.http import HttpResponse, JsonResponse,HttpRequest
from django.views import View
# Import user model
from django.contrib.auth.models import User
from .models import Task
# Import authentication classes
from django.contrib.auth import authenticate
from base64 import b64decode

def isAuth(auth):
    if auth is None:
        return False
    # Get token
    token = auth.split(' ')[1]
    auth=b64decode(token).decode() # Decode token
    username, password = auth.split(':') # Split token

    # Check if user is authenticated
    
    user = authenticate(username=username, password=password)

    if user is not None:
        return True
    return False



def tasks(request: HttpRequest) -> JsonResponse:
    """
    Create a task
    """
    auth = request.headers.get('Authorization')
    if isAuth(auth):
        if request.method == 'POST':
            return JsonResponse({'message': 'Task created successfully'}, status=201)
        if request.method == 'GET':
            todos = {
                'todo':[]
            }
            # Get all tasks
            tasks = Task.objects.all()
            for task in tasks:
                todos['todo'].append({
                    'id': task.id,
                    'task': task.task,
                    'description': task.description,
                    'complited': task.complited,
                    'created_at': task.created_at,
                    'updated_at': task.updated_at,
                   
                })

            return JsonResponse(todos, status=200)
        
    else:
        return JsonResponse({'message': 'Unauthorized'}, status=401)
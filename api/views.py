from django.http import HttpResponse, JsonResponse,HttpRequest
from django.views import View
import json
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
    user = isAuth(auth)
    if user:
        if request.method == 'POST':
            decoded = request.body.decode()
            todos = json.loads(decoded)
            task = todos.get('task',False)
            description = todos.get('description', False)
            completed = todos.get('completed', False)
            created_at = todos.get('created_at',False)
            updated_at = todos.get('updated_at', False)
            student_id = todos.get('student_id', False)

            if task == False:
                return JsonResponse({'status': 'task field is required'})
            if description == False:
                return JsonResponse({"status": 'description field is required'})
            if student_id == False:
                return JsonResponse({"status": 'student_id field is required'})
            
            tasks = Task(
                task=task,
                description=description,
                completed=completed,
                created_at=created_at,
                updated_at=updated_at,
                student_id=student_id
            )

            tasks.save()
            return JsonResponse(tasks.to_dict())
            # return JsonResponse({'message': 'Task created successfully'}, status=201)
        if request.method == 'GET':
            todos = {
                'todo':[]
            }
            # Get all tasks
            tasks = Task.objects.filter(student = user)
            for task in tasks:
                todos['todo'].append(task.to_dict())

            return JsonResponse(todos, status=200)
        
    else:
        return JsonResponse({'message': 'Unauthorized'}, status=401)
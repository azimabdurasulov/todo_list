from django.http import HttpResponse, JsonResponse,HttpRequest
from django.shortcuts import render
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



def get_tasks(request: HttpRequest) -> JsonResponse:
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
    
def get_task_id(request:HttpRequest, pk:int)->JsonResponse:
    auth = request.headers.get('Authorization')
    user = isAuth(auth)
    if user:
        if request.method == 'GET':
            try:
                # get task from database by id
                task = Task.objects.get(id=pk)
                return JsonResponse(task.to_dict())
            except:
                return JsonResponse({"status": "object doesn't exist"})
            
        if request.method == 'POST':
            decoded = request.body.decode()
            tasks = json.loads(decoded)
            task = tasks.get('task',False)
            description = tasks.get('description',False)
            completed = tasks.get('completed',False)
            created_at = tasks.get('created_at',False)
            updated_at = tasks.get('updated_at',False)

            todos = Task.objects.get(id=pk)
            if task:
                todos.task=task
            if description:
                todos.description=description
            if completed:
                todos.completed=completed
            if created_at:
                todos.created_at=created_at
            if updated_at:
                todos.updated_at=updated_at

            todos.save()
            return JsonResponse(todos.to_dict())

def delete_task_id(request: HttpRequest, pk: int) -> JsonResponse:
    auth = request.headers.get('Authorization')
    user = isAuth(auth)
    if user:
        if request.method == 'POST':
            try:
                tasks = Task.objects.get(id=pk)
                tasks.delete()
                return JsonResponse(tasks.to_dict())
            except:
                return JsonResponse({"status": "object doesn't exist"})
            
def completed_task(request: HttpRequest):
    auth = request.headers.get('Authorization')
    user = isAuth(auth)
    if user:
        try:
            tasks = Task.objects.all()
            result = []
            for task in tasks:
                if task.completed:
                    result.append(task.to_dict())

            return JsonResponse({'result':result})
        except:
            return HttpResponse('Hello World!')

def incompleted_task(request: HttpRequest):
    auth = request.headers.get('Authorization')
    user = isAuth(auth)
    if user:
        try:
            tasks = Task.objects.all()
            result = []
            for task in tasks:
                if task.completed == False:
                    result.append(task.to_dict())

            return JsonResponse({'result':result})
        except:
                return HttpResponse('Hello World!')
        
def home(request: HttpRequest):
    tasks = Task.objects.all()
    data = {
        "tasks":tasks
    }
    return render(request, 'home.html', context=data)
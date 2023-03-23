from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views import View
import json
# Import user model
from django.contrib.auth.models import User

# Import authentication classes
from django.contrib.auth import authenticate


class HomeView(View):
    def get(self, request):
        user = User.objects.all()
        data = {
            'users': []
        }
        for i in user:
            data['users'].append({
                'id': i.id,
                'username': i.username,
                'email': i.email
            })
        return JsonResponse(data)
    def post(self, request):
        return HttpResponse('ok')
        


def index(request: HttpRequest):
    if request.method == 'POST':
        decode = request.body.decode()
        data = json.loads(decode)
        # Check if user is authenticated
        user = authenticate(username=data['username'], password=data['passvord'])
        if user is not None:
            return JsonResponse({
                'username': user.username,
                'passvord': user.password
            })
        return JsonResponse({'result': 'You are not authenticated'})
    
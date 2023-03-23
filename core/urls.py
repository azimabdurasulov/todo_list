from django.contrib import admin
from django.urls import path
from api.views import HomeView
from api.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view()),
    path('index/', index)
]
from django.conf.urls import url
from django.urls import path
from . import tasks
from . import users

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('tasks/create', tasks.addTask),
    path('tasks/update/<str:id>', tasks.updateTask),
    path('tasks/delete/<str:id>', tasks.deleteTask),
    path('tasks/<str:id>', tasks.getTask),
    path('tasks/', tasks.getTasks),


    path('users/signup', users.signup),
    path('users/login', users.login),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
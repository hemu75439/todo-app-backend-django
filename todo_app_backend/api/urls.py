from django.conf.urls import url
from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('tasks/', views.getTask),
    path('tasks/create', views.addTask),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
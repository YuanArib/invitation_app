from django.urls import path
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/<int:id>', views.test, name='test'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
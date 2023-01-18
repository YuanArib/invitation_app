from django.urls import path
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    #CHANGE THIS LATER
    path('test/<int:id>', views.test, name='test'),
    path('dashboard/', views.dashboard, name='dashboard'),

    #EDIT
    path('edit/<int:id>', views.edit, name='edit'),
    path('edit_request/<int:id>', views.edit_request, name='edit_request'),

    #I KNOW THIS ISNT EVEN RELATED TO MEMBERS BUT IDK HOW SHOULD I DO IT
    path('register/', views.register, name='register'),
    path('register/register_request/', views.register_request, name='register_request')
]
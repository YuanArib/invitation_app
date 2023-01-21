from django.urls import path
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    #CHANGE THIS LATER
    path('add_request/<int:id>', views.add_request, name='add_request'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('edit_request/<int:id>', views.edit_request, name='edit_request'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('open/<int:id>', views.open_file, name='open_file'),

    #EDIT
    path('edit/<int:id>', views.edit, name='edit'),
    path('edit_request/<int:id>', views.edit_request, name='edit_request'),

    #I KNOW THIS ISNT EVEN RELATED TO MEMBERS BUT IDK HOW SHOULD I DO IT
    path('register/', views.register, name='register'),
    path('register/register_request/', views.register_request, name='register_request'),
    path("password_change/", views.password_change, name="password_change"),
    path("password_change_request/", views.password_change_request, name="password_change_request"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm')
]
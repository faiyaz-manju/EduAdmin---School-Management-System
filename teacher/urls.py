from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.show_teacher, name='show_teachers'),
    path('teacher/<int:id>/edit/', views.edit_teacher, name='edit_teacher'),
    path('teacher/<int:id>/delete/', views.delete_teacher, name='delete_teacher'),
    
    path('class/', views.show_class, name='show_classes'),
    path('class/<int:id>/edit/', views.edit_class, name='edit_class'),
    path('class/<int:id>/delete/', views.delete_class, name='delete_class'),
    
    
    # path('__reload__/', include('django_browser_reload.urls')),
]

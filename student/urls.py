from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.show_students, name='show_students'),
    path('add/', views.add_student, name='add_student'),
    path('<int:id>/', views.student_profile, name='student_profile'),
    path('<int:id>/edit/', views.edit_student, name='edit_student'),
    
    
    
    
    
    
    # path('__reload__/', include('django_browser_reload.urls')),
]
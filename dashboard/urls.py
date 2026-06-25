from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    
    
    
    
    # path('__reload__/', include('django_browser_reload.urls')),
]
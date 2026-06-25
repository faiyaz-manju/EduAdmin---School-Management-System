from django.urls import include, path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.parents_portal, name='portal'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('change_password/', views.change_password_view, name='change_password'),
    path('users/', views.user_management_view, name='user'),
    path('users/<int:id>/edit/', views.edit_user, name='edit_user'),
    path('users/<int:id>/delete/', views.delete_user, name='delete_user'),
    
    
    
    
    
    # path('__reload__/', include('django_browser_reload.urls')),
]
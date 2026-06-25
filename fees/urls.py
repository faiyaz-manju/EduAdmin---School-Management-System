from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.master, name='master'),
    # path('delete/<int:id>/', views.delete_fees, name='delete_fees'),
    path('payment/', views.payment, name='payment'),
    path('payment/add/', views.add_payment, name='add_payment'),
    path('generate/<int:id>/', views.generate_receipt, name='generate_receipt'),
    
    
    
    
    
    # path('__reload__/', include('django_browser_reload.urls')),
]
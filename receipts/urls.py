from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.show_receipts, name='show_receipts'),
    path('<int:id>/', views.receipt, name='receipt'),
    path('download/<int:id>/', views.download_receipt, name='download_receipt'),






    # path('__reload__/', include('django_browser_reload.urls')),
]
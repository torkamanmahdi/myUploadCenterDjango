from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('file/<uuid:unique_id>/', views.file_detail, name='file_detail'),
    path('view/<uuid:unique_id>/', views.file_view, name='file_view'),
    path('download/<uuid:unique_id>/', views.file_download, name='file_download'),
]
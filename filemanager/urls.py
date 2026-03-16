from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('file/<uuid:unique_id>/', views.file_detail, name='file_detail'),
    path('view/<uuid:unique_id>/', views.file_view, name='file_view'),
    path('download/<uuid:unique_id>/', views.file_download, name='file_download'),
    path('gallery/', views.public_gallery, name='public_gallery'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('file/<uuid:unique_id>/delete/', views.delete_file, name='delete_file'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
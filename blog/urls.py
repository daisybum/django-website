from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('delete/<int:id>/', views.post_delete, name='post_delete'),
    path('edit/<int:id>/', views.post_update, name='post_update'),
    path('write/', views.post_create, name='post_create'),
    path('<int:id>/', views.post_detail, name='post_detail'),
    path('', views.post_list, name='post_list'),
]
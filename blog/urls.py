from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('search/<str:q>/', views.post_search, name='post_search'),
    path('delete/<int:id>/', views.post_delete, name='post_delete'),
    path('edit/<int:id>/', views.post_update, name='post_update'),
    path('write/', views.post_create, name='post_create'),
    path('<int:id>/new_comment/', views.comment_create, name='comment_create'),
    path('<int:id>/', views.post_detail, name='post_detail'),
    path('', views.post_list, name='post_list'),
]
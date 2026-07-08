from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.main, name='main'),
    path('create/', views.post_create, name='post_create'),
    path('<int:pk>/update/', views.post_update, name='post_update'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('<int:pk>/like/', views.post_like, name='post_like'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/comments/create/', views.comment_create, name='comment_create'),
    path('comments/<int:pk>/update/', views.comment_update, name='comment_update'),
    path('comments/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('stories/create/', views.story_create, name='story_create'),
    path('stories/<int:pk>/', views.story_detail, name='story_detail'),
]
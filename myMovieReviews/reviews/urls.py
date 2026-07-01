from django.urls import path
from . import views

urlpatterns = [
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/create/', views.review_create, name='review_create'),
    path('reviews/<int:pk>/', views.review_detail, name='review_detail'),
    path('reviews/<int:pk>/update/', views.review_update, name='review_update'),
    path('reviews/<int:pk>/delete/', views.review_delete, name='review_delete'),
]
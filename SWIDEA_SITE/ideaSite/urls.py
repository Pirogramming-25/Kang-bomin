from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.list, name='list'),
    path("add/", views.add, name='add'),
    path("detail/<int:id>/", views.detail, name='detail'),
    path("modify/<int:id>/", views.modify, name='modify'),
    path("delete/<int:id>/", views.delete, name='delete'),
    path("toolList/", views.toolList, name='toolList'),
    path("toolAdd/", views.toolAdd, name='toolAdd'),
    path("toolDetail/<int:id>/", views.toolDetail, name='toolDetail'),
    path("toolModify/<int:id>/", views.toolModify, name='toolModify'),
    path("toolDelete/<int:id>/", views.toolDelete, name='toolDelete'),
    path("interest/<int:id>/", views.interest_update, name='interest_update'),
    path("star/<int:id>/", views.star_toggle, name='star_toggle'),
]
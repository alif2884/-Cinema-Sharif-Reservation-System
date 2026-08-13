from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='home'),
    path('list/', views.movie_list, name='movie_list'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),

    path('admin/list/', views.movie_admin_list, name='movie_admin_list'),
    path('admin/create/', views.movie_create, name='movie_create'),
    path('admin/<int:pk>/edit/', views.movie_update, name='movie_update'),
    path('admin/<int:pk>/delete/', views.movie_delete, name='movie_delete'),
]

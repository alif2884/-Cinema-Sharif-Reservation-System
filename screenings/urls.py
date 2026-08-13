from django.urls import path
from . import views

urlpatterns = [
    path('<int:movie_id>/', views.screening_list_for_movie, name='screening_list'),
    path('<int:movie_id>/cinemas/', views.movie_cinemas, name='movie_cinemas'),
]
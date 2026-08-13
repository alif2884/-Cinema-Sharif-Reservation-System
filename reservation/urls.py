from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:screening_id>/', views.reserve_seat, name='reserve_seat'),
    path('screening/<int:screening_id>/select-seats/', views.reserve_seat, name='seat_selection'),
    
    path('success/temp/<int:pk>/', views.reservation_success_temp, name='reservation_success'),
    path('success/temp/<int:pk>/alt/', views.reservation_success_temp, name='reservation_success_temp'),

    path('confirm/<str:tracking_code>/', views.confirm_reservation_payment, name='confirm_reservation_payment'),

    path('my-reservations/', views.my_reservations, name='my_reservations'),

    path('cancel/<str:tracking_code>/', views.cancel_reservation_view, name='cancel_reservation_view'),
    path('cancel/<str:tracking_code>/alt/', views.cancel_reservation_view, name='cancel_reservation'),

    path('cinemas/', views.cinema_list, name='cinema_list'),
    path('cinemas/create/', views.cinema_create, name='cinema_create'),
    path('cinemas/<int:pk>/update/', views.cinema_update, name='cinema_update'),
    path('cinemas/<int:pk>/delete/', views.cinema_delete, name='cinema_delete'),
    path('cinemas/<int:cinema_id>/movies/', views.cinema_movies, name='cinema_movies'),
]
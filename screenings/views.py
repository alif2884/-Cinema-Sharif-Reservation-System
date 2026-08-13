from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Screening
from movies.models import Movie
from reservation.models import Cinema

def screening_list_for_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    now = timezone.now()
    
    screenings = Screening.objects.filter(movie=movie, start_time__gte=now).order_by('start_time')
    
    current_cinema = None
    cinema_name_param = request.GET.get('cinema')

    if cinema_name_param:
        screenings = screenings.filter(cinema__name=cinema_name_param)
        current_cinema = Cinema.objects.filter(name=cinema_name_param).first()

    time_range = request.GET.get('time')
    
    if time_range == 'morning':
        screenings = screenings.filter(start_time__hour__lt=12)
    elif time_range == 'evening':
        screenings = screenings.filter(start_time__hour__gte=12)
        
    available_cinemas = Screening.objects.filter(movie=movie, start_time__gte=now)\
                                         .values_list('cinema__name', flat=True).distinct()

    context = {
        'movie': movie,
        'screenings': screenings,
        'available_cinemas': available_cinemas,
        'current_cinema': current_cinema,
    }
    
    return render(request, 'screenings/screening_list.html', context)


def movie_cinemas(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    now = timezone.now()
    
    cinemas = Cinema.objects.filter(
        screenings__movie=movie,
        screenings__start_time__gte=now
    ).distinct()

    context = {
        'movie': movie,
        'cinemas': cinemas,
    }
    return render(request, 'screenings/movie_cinemas.html', context)
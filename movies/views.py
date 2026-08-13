from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Movie
from .forms import MovieForm
from django.contrib import messages
from django.utils import timezone
from screenings.models import Screening

def is_admin(user):
    return user.is_staff and user.is_superuser

def movie_list(request):
    movies = Movie.objects.all()
    
    search_query = request.GET.get('q')
    genre_filter = request.GET.get('genre')
    year_filter = request.GET.get('year')

    if search_query:
        movies = movies.filter(title__icontains=search_query)
    
    if genre_filter:
        movies = movies.filter(genre=genre_filter)

    if year_filter:
        movies = movies.filter(release_date__year=year_filter)

    available_genres = Movie.GENRE_CHOICES 
    available_years = Movie.objects.dates('release_date', 'year')

    context = {
        'movies': movies,
        'available_genres': available_genres,
        'available_years': available_years,
    }
    return render(request, 'movies/movie_list.html', context)

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    current_time = timezone.now()
    screenings = Screening.objects.filter(
        movie=movie,
        start_time__gt=current_time 
    ).order_by('start_time')

    context = {
        'movie': movie,
        'screenings': screenings,
    }
    return render(request, 'movies/movie_detail.html', context)

@login_required
@user_passes_test(is_admin)
def movie_admin_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_admin_list.html', {'movies': movies})

@login_required
@user_passes_test(is_admin)
def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ فیلم با موفقیت اضافه شد')
            return redirect('movie_admin_list')
    else:
        form = MovieForm()
    return render(request, 'movies/movie_form.html', {'form': form, 'title': 'افزودن فیلم'})

@login_required
@user_passes_test(is_admin)
def movie_update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, '✏️ اطلاعات فیلم با موفقیت ویرایش شد')
            return redirect('movie_admin_list')
    else:
        form = MovieForm(instance=movie)
    return render(request, 'movies/movie_form.html', {'form': form, 'title': 'ویرایش فیلم'})

@login_required
@user_passes_test(is_admin)
def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.delete()
        messages.warning(request, '🗑 فیلم با موفقیت حذف شد')
        return redirect('movie_admin_list')
    return render(request, 'movies/movie_confirm_delete.html', {'movie': movie})
    
def landing_page(request):
    if request.user.is_authenticated:
        return redirect('movie_list')
    return render(request, 'landing.html')
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Count
import datetime

from .models import Reservation, Cinema
from screenings.models import Screening, Seat
from movies.models import Movie

from .forms import CinemaForm
from .patterns import BookingFacade, CinemaConfig 

User = get_user_model()

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
def create_reservation(request):
    return redirect('movie_list')

@login_required
def reserve_seat(request, screening_id):
    screening = get_object_or_404(Screening, pk=screening_id)
    
    expiration_time = timezone.now() - datetime.timedelta(minutes=15)
    expired_reservations = Reservation.objects.filter(
        screening=screening,
        status=Reservation.STATUS_PENDING,
        created_at__lt=expiration_time
    )
    for res in expired_reservations:
        if res.seat:
            res.seat.is_reserved = False
            res.seat.save(update_fields=['is_reserved'])
        res.status = Reservation.STATUS_CANCELLED
        res.save(update_fields=['status'])

    seats = Seat.objects.filter(screening=screening).order_by('row', 'number')

    if request.method == 'POST':
        seat_id = request.POST.get('seat_id')
        if not seat_id:
            messages.error(request, '❌ لطفاً یک صندلی انتخاب کنید')
            return redirect('reserve_seat', screening_id=screening.pk)

        reserved_until = timezone.now() + datetime.timedelta(minutes=15)

        try:
            with transaction.atomic():
                seat = Seat.objects.select_for_update().get(pk=seat_id, screening=screening)

                if seat.is_reserved:
                    messages.error(request, '❌ این صندلی قبلاً رزرو شده است')
                    return redirect('reserve_seat', screening_id=screening.pk)

                reservation = Reservation.objects.create(
                    user=request.user,
                    screening=screening,
                    seat=seat,
                    status=Reservation.STATUS_PENDING,
                    reserved_until=reserved_until
                )

                seat.is_reserved = True
                seat.save(update_fields=['is_reserved'])

        except Seat.DoesNotExist:
            messages.error(request, '❌ صندلی نامعتبر است')
            return redirect('reserve_seat', screening_id=screening.pk)
        except Exception as e:
            messages.error(request, f'❌ خطا در پردازش رزرو: {e}')
            return redirect('reserve_seat', screening_id=screening.pk)

        messages.success(request, '✅ صندلی رزرو شد. ۱۵ دقیقه برای پرداخت فرصت دارید.')
        return redirect('reservation_success_temp', pk=reservation.pk)

    return render(request, 'reservation/seat_selection.html', {
        'screening': screening,
        'seat_data': seats
    })

@login_required
def reservation_success_temp(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    
    if reservation.status == Reservation.STATUS_CONFIRMED:
        return redirect('my_reservations')

    if reservation.created_at:
        elapsed = (timezone.now() - reservation.created_at).total_seconds()
        time_left = max(0, 900 - int(elapsed))
    else:
        time_left = 0
    
    if time_left == 0:
        reservation.delete()
        messages.error(request, "زمان رزرو شما به پایان رسیده است.")
        return redirect('movie_list')

    price = reservation.screening.price 

    if request.method == 'POST' and 'charge_wallet' in request.POST:
        try:
            amount = int(request.POST.get('amount', 0))
            if amount > 0:
                wallet = request.user.wallet 
                wallet.balance += amount
                wallet.save()
                messages.success(request, f'✅ مبلغ {amount} تومان به کیف پول اضافه شد.')
                return redirect('reservation_success_temp', pk=pk)
            else:
                messages.error(request, 'مبلغ شارژ باید بیشتر از صفر باشد.')
                
        except ValueError:
            messages.error(request, 'مبلغ وارد شده معتبر نیست.')
            
        except AttributeError:
             messages.error(request, 'خطای سیستم: کیف پول برای شما یافت نشد.')

    try:
        wallet_balance = request.user.wallet.balance
    except AttributeError:
        wallet_balance = 0
        
    shortage = max(0, price - wallet_balance)
    
    context = {
        'reservation': reservation,
        'temporary': True,
        'time_left': time_left,
        'price': price,
        'wallet_balance': wallet_balance,
        'shortage': shortage, 
    }

    return render(request, 'reservation/reservation_success.html', context)


@login_required
def confirm_reservation_payment(request, tracking_code):
    reservation = get_object_or_404(Reservation, tracking_code=tracking_code, user=request.user)

    try:
        BookingFacade.finalize_booking(request.user, reservation)
        
    except ValidationError as e:
        messages.error(request, str(e))
        return redirect('reservation_success_temp', pk=reservation.pk)
    
    except Exception as e:
        messages.error(request, '❌ خطای سرور در پردازش پرداخت. لطفاً دوباره تلاش کنید.')
        return redirect('reservation_success_temp', pk=reservation.pk)

    messages.success(request, '🎉 پرداخت با موفقیت انجام و رزرو تأیید شد.')
    return redirect('reservation_success', pk=reservation.pk)

@login_required
def cancel_reservation_view(request, tracking_code):
    reservation = get_object_or_404(Reservation, tracking_code=tracking_code, user=request.user)

    if reservation.status == Reservation.STATUS_CANCELLED:
        messages.warning(request, 'این رزرو قبلاً لغو شده است.')
        return redirect('my_reservations')

    if request.method == 'POST':
        with transaction.atomic():
            reservation.status = Reservation.STATUS_CANCELLED
            reservation.reserved_until = None
            reservation.save()

            if reservation.seat:
                seat = reservation.seat
                seat.is_reserved = False
                seat.save()

        messages.success(request, '✅ رزرو با موفقیت لغو شد.')
        return redirect('my_reservations')
    
    return render(request, 'reservation/cancel_confirm.html', {'reservation': reservation})


@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user).select_related('screening', 'seat').order_by('-created_at')
    return render(request, 'reservation/my_reservations.html', {'reservations': reservations})


@login_required
def cinema_list(request):
    search_query = request.GET.get('q')
    cinemas = Cinema.objects.annotate(screening_count=Count('screenings'))
    if search_query:
        cinemas = cinemas.filter(name__icontains=search_query)

    return render(request, 'reservation/cinema_list.html', {'cinemas': cinemas})


@login_required
@user_passes_test(is_admin)
def cinema_create(request):
    if request.method == 'POST':
        form = CinemaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cinema_list')
    else:
        form = CinemaForm()
    return render(request, 'reservation/cinema_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def cinema_update(request, pk):
    cinema = get_object_or_404(Cinema, pk=pk)
    if request.method == 'POST':
        form = CinemaForm(request.POST, instance=cinema)
        if form.is_valid():
            form.save()
            return redirect('cinema_list')
    else:
        form = CinemaForm(instance=cinema)
    return render(request, 'reservation/cinema_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def cinema_delete(request, pk):
    cinema = get_object_or_404(Cinema, pk=pk)
    if request.method == 'POST':
        cinema.delete()
        return redirect('cinema_list')
    return render(request, 'reservation/cinema_confirm_delete.html', {'cinema': cinema})

def cinema_movies(request, cinema_id):
    cinema = get_object_or_404(Cinema, pk=cinema_id)
    
    movies = Movie.objects.filter(screenings__cinema=cinema).distinct()

    all_dates = movies.values_list('release_date', flat=True)
    available_years = sorted(list(set(d.year for d in all_dates if d)), reverse=True)
    
    genre_choices = Movie._meta.get_field('genre').choices

    genre_filter = request.GET.get('genre')
    year_filter = request.GET.get('year')
    search_query = request.GET.get('q')

    if search_query:
        movies = movies.filter(title__icontains=search_query)
    
    if genre_filter:
        movies = movies.filter(genre=genre_filter)
    
    if year_filter:
        movies = movies.filter(release_date__year=year_filter)

    context = {
        'cinema': cinema,
        'movies': movies,
        'available_years': available_years,
        'genre_choices': genre_choices,
    }
    return render(request, 'reservation/cinema_movies.html', context)
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from screenings.models import Screening, Seat, Cinema
from movies.models import Movie
from .models import Reservation
from django.utils import timezone
import datetime
import threading

User = get_user_model()

class ConcurrencyReserveTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='u1', password='p')
        self.user2 = User.objects.create_user(username='u2', password='p')

        self.movie = Movie.objects.create(title='M', description='d', release_date=timezone.now().date(), duration=datetime.timedelta(hours=2))
        self.cinema = Cinema.objects.create(name='C', capacity=100, city='X')
        self.screening = Screening.objects.create(movie=self.movie, cinema=self.cinema, start_time=timezone.now() + datetime.timedelta(hours=2), price=10000)
        self.seat = Seat.objects.create(screening=self.screening, row=1, number=1, is_reserved=False)

    def _reserve_with_client(self, username, password, results, idx):
        c = Client()
        c.login(username=username, password=password)
        url = reverse('reserve_seat', args=[self.screening.id])
        resp = c.post(url, {'seat_id': self.seat.id}, follow=True)
        results[idx] = resp

    def test_two_users_cannot_reserve_same_seat(self):
        results = [None, None]
        t1 = threading.Thread(target=self._reserve_with_client, args=('u1','p', results, 0))
        t2 = threading.Thread(target=self._reserve_with_client, args=('u2','p', results, 1))

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        reservations = Reservation.objects.filter(seat=self.seat)
        self.assertTrue(reservations.count() >= 1)
        pending_or_confirmed = reservations.filter(status__in=[Reservation.STATUS_PENDING, Reservation.STATUS_CONFIRMED]).count()
        self.assertEqual(pending_or_confirmed, 1)
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.is_reserved)
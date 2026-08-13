from django.core.management.base import BaseCommand
from django.utils import timezone
from reservation.models import Reservation
from django.db import transaction

class Command(BaseCommand):
    help = 'Release seats for expired PENDING reservations'

    def handle(self, *args, **options):
        now = timezone.now()
        expired = Reservation.objects.filter(status=Reservation.STATUS_PENDING, reserved_until__lt=now)
        total = expired.count()
        released = 0

        for r in expired.select_related('seat'):
            try:
                with transaction.atomic():
                    r = Reservation.objects.select_for_update().get(pk=r.pk)
                    if r.status != Reservation.STATUS_PENDING:
                        continue

                    if r.seat:
                        seat = r.seat
                        seat.is_reserved = False
                        seat.save()
                    r.status = Reservation.STATUS_CANCELLED
                    r.reserved_until = None
                    r.save()
                    released += 1
            except Reservation.DoesNotExist:
                continue

        self.stdout.write(self.style.SUCCESS(f'Found {total} expired, released {released}.'))
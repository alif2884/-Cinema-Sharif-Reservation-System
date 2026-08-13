from django.db import transaction
from django.core.exceptions import ValidationError
from reservation.models import Reservation

class CinemaConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CinemaConfig, cls).__new__(cls)
            cls._instance.ticket_price = 50000 
            cls._instance.tax_rate = 0.09       
        return cls._instance

    def get_final_price(self):
        return int(self.ticket_price * (1 + self.tax_rate))


class BookingFacade:

    @staticmethod
    def finalize_booking(user, reservation):
        config = CinemaConfig()
        price = config.get_final_price()

        with transaction.atomic():
            reservation = Reservation.objects.select_for_update().get(pk=reservation.pk)

            if reservation.is_expired():
                reservation.status = Reservation.STATUS_CANCELLED
                reservation.save(update_fields=['status'])
                raise ValidationError("⏰ زمان رزرو شما به پایان رسیده است.")

            wallet = getattr(user, 'wallet', None)
            if wallet is None:
                raise ValidationError("⚠️ کیف پول برای کاربر یافت نشد.")

            if wallet.balance < price:
                raise ValidationError("💳 موجودی کیف پول کافی نیست.")
            
            wallet.balance -= price
            wallet.save(update_fields=['balance'])

            reservation.status = Reservation.STATUS_CONFIRMED
            reservation.reserved_until = None
            reservation.save(update_fields=['status', 'reserved_until'])

            if reservation.seat:
                reservation.seat.is_reserved = True
                reservation.seat.save(update_fields=['is_reserved'])

            return True
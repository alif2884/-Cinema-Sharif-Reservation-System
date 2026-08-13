from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

class Cinema(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام سینما")
    city = models.CharField(max_length=50, verbose_name="شهر", null=True, blank=True)
    capacity = models.PositiveIntegerField(default=100, verbose_name="ظرفیت")
    address = models.TextField(blank=True, null=True, verbose_name="آدرس")

    class Meta:
        verbose_name = "سینما"
        verbose_name_plural = "سینماها"

    def __str__(self):
        return f"{self.name} ({self.city})"

class Reservation(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_CONFIRMED = 'CONFIRMED'
    STATUS_CANCELLED = 'CANCELLED'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'در انتظار پرداخت'),
        (STATUS_CONFIRMED, 'قطعی'),
        (STATUS_CANCELLED, 'لغو شده'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="کاربر")
    screening = models.ForeignKey('screenings.Screening', on_delete=models.CASCADE, verbose_name="سانس/اکران")
    seat = models.ForeignKey('screenings.Seat', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="صندلی")
    tracking_code = models.CharField(max_length=12, unique=True, blank=True, null=True, verbose_name="کد رهگیری")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING, verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    reserved_until = models.DateTimeField(null=True, blank=True, verbose_name="رزرو تا زمان", help_text="اگر وضعیت PENDING است تا چه زمانی رزرو قفل باشد")

    class Meta:
        verbose_name = "رزرو"
        verbose_name_plural = "رزروها"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.tracking_code:
            self.tracking_code = str(uuid.uuid4())[:10].upper()
        super().save(*args, **kwargs)

    def is_expired(self):
        if self.status != self.STATUS_PENDING:
            return False
        if not self.reserved_until:
            return False
        return timezone.now() >= self.reserved_until

    def __str__(self):
        return f"{self.tracking_code} - {self.user} - {self.status}"
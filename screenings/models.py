from django.db import models
from movies.models import Movie
from django.core.exceptions import ValidationError
from reservation.patterns import CinemaConfig

class Screening(models.Model):
    movie = models.ForeignKey(
        Movie, 
        on_delete=models.CASCADE, 
        verbose_name="فیلم",
        related_name='screenings'
    )
    
    cinema = models.ForeignKey(
        'reservation.Cinema', 
        on_delete=models.CASCADE, 
        verbose_name="سینما",
        related_name='screenings'
    )

    start_time = models.DateTimeField(verbose_name="زمان شروع سانس")
    capacity = models.PositiveIntegerField(verbose_name="ظرفیت سانس", blank=True)

    class Meta:
        verbose_name = "برنامه اکران"
        verbose_name_plural = "برنامه‌های اکران"
        unique_together = [['movie', 'cinema', 'start_time']]
        ordering = ['start_time']

    def clean(self):
        overlapping = Screening.objects.filter(
            cinema=self.cinema,
            start_time=self.start_time
        ).exclude(pk=self.pk)
        
        if overlapping.exists():
            raise ValidationError("⚠️ در این زمان و در این سینما، سانس دیگری تعریف شده است!")

    def save(self, *args, **kwargs):
        if not self.capacity:
            self.capacity = self.cinema.capacity
        super().save(*args, **kwargs)

    @property
    def total_capacity(self):
        return self.seats.count()

    @property
    def remaining_seats(self):
        return self.seats.filter(is_reserved=False).count()
    
    @property
    def price(self):
        return CinemaConfig().get_final_price()

    def __str__(self):
        return f"{self.movie} در {self.cinema} - {self.start_time.strftime('%Y/%m/%d %H:%M')}"


class Seat(models.Model):
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE, related_name='seats', verbose_name="اکران")
    row = models.CharField(max_length=5, verbose_name="ردیف")
    number = models.PositiveIntegerField(verbose_name="شماره صندلی")
    is_reserved = models.BooleanField(default=False, verbose_name="رزرو شده")

    class Meta:
        ordering = ['row', 'number']
        unique_together = ('screening', 'row', 'number')
        verbose_name = "صندلی"
        verbose_name_plural = "صندلی‌ها"

    def __str__(self):
        return f"{self.row}{self.number}"
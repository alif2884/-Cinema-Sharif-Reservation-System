from django.contrib import admin
from .models import Screening, Seat

@admin.register(Screening)
class ScreeningAdmin(admin.ModelAdmin):
    list_display = ('movie', 'cinema', 'start_time', 'capacity', 'remaining_seats')
    list_filter = ('cinema', 'start_time', 'movie')
    search_fields = ('movie__title', 'cinema__name')
    fields = ('movie', 'cinema', 'start_time', 'capacity')
    help_texts = {
        'capacity': 'اگر خالی بگذارید، ظرفیت کل سینما به صورت خودکار درج می‌شود.',
    }

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('screening', 'row', 'number', 'is_reserved')
    list_filter = ('is_reserved', 'screening__cinema', 'screening__movie')
    search_fields = ('screening__movie__title',)
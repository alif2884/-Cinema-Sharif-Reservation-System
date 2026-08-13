from django.contrib import admin
from .models import Reservation, Cinema

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'screening', '__str__', 'created_at')  
 
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Cinema)
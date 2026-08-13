from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True, verbose_name="شماره تماس")
    is_admin = models.BooleanField(default=False, verbose_name='دسترسی ادمین')

    def __str__(self):
        return self.username or self.phone_number
    
class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    balance = models.PositiveIntegerField(default=0, verbose_name="موجودی")

    def __str__(self):
        return f"کیف پول {self.user.username}"
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)
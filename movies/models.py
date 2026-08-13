from django.db import models

class Movie(models.Model):
    GENRE_CHOICES = [
        ('action', 'اکشن'),
        ('comedy', 'کمدی'),
        ('drama', 'درام'),
        ('sci-fi', 'علمی تخیلی'),
        ('horror', 'وحشت'),
        ('animation', 'انیمیشن'),
        ('documentary', 'مستند'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="عنوان فیلم")
    description = models.TextField(verbose_name="توضیحات فیلم")
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='drama', verbose_name="ژانر")
    director = models.CharField(max_length=100, verbose_name="کارگردان", default="نامشخص")
    actors = models.CharField(max_length=500, verbose_name="بازیگران اصلی", help_text="نام بازیگران را با ویرگول جدا کنید")

    release_date = models.DateField(verbose_name="تاریخ اکران")
    duration = models.DurationField(verbose_name="مدت زمان")
    poster_image = models.ImageField(upload_to='movies/', verbose_name="تصویر پوستر")

    def __str__(self):
        return self.title
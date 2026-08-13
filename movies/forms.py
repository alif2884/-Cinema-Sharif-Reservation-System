from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'genre', 'director', 'actors', 'release_date', 'duration', 'poster_image']

        labels = {
            'title': 'عنوان فیلم',
            'description': 'خلاصه داستان',
            'genre': 'ژانر',
            'director': 'کارگردان',
            'actors': 'بازیگران اصلی',
            'release_date': 'تاریخ اکران',
            'duration': 'مدت زمان',
            'poster_image': 'پوستر فیلم',
        }

        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'actors': forms.Textarea(),
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }
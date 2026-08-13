from django import forms
from .models import Reservation, Cinema
from screenings.models import Screening
from screenings.models import Seat

class ReservationForm(forms.ModelForm):
    screening = forms.ModelChoiceField(
        queryset=Screening.objects.all(),
        empty_label="اکران مورد نظر را انتخاب کنید",
        label="اکران",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    seat = forms.ModelChoiceField(
        queryset=Seat.objects.none(),
        empty_label="صندلی مورد نظر را انتخاب کنید",
        label="صندلی",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Reservation
        fields = ['screening', 'seat']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'screening' in self.data:
            try:
                screening_id = int(self.data.get('screening'))
                self.fields['seat'].queryset = Seat.objects.filter(
                    screening_id=screening_id,
                    is_reserved=False
                )
            except (ValueError, TypeError):
                pass
        
class CinemaForm(forms.ModelForm):
    class Meta:
        model = Cinema
        fields = ['name', 'capacity', 'address']
        labels = {
            'name': 'نام سینما',
            'capacity': 'ظرفیت سالن',
            'address': 'آدرس',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام سینما را وارد کنید'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity is not None and capacity <= 0:
            raise forms.ValidationError("ظرفیت سالن باید یک عدد مثبت باشد.")
        return capacity
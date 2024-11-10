from django import forms

from .models import Ticket, FlightReview


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['seat_number']


class TicketReservationForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['seat_number']

    def __init__(self, *args, **kwargs):
        self.flight = kwargs.pop('flight', None)
        super().__init__(*args, **kwargs)

    def clean_seat_number(self):
        seat_number = self.cleaned_data['seat_number']
        if Ticket.objects.filter(flight=self.flight, seat_number=seat_number).exists():
            raise forms.ValidationError("This seat is already reserved. Please choose another.")
        return seat_number


class ReviewForm(forms.ModelForm):
    class Meta:
        model = FlightReview
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Write your review here...', 'rows': 4}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }
        labels = {
            'text': 'Review',
            'rating': 'Rating (1 to 10)',
        }

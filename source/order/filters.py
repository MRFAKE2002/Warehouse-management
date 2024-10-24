from django import forms

class OrderFilter(forms.Form):
    start_date = forms.DateField(required=False, label='زمان شروع', widget=forms.DateInput(attrs={'class': 'datepicker'}))
    end_date = forms.DateField(required=False, label='زمان پایان', widget=forms.DateInput(attrs={'class': 'datepicker'}))

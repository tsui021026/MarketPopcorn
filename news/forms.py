from django import forms

class SubscriberForm(forms.Form):
    email = forms.EmailField(label=False,
                             max_length=100,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Adverts


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AdPostForm(forms.ModelForm):
    class Meta:
        model = Adverts
        fields = ['Ad_Title', 'price', 'property_location', 'Address', 'listing_category', 'sq_ft',
                  'bed_rooms',
                  'bath_rooms',
                  'picture']

        widgets = {
            'Ad_Title': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Title of your advert...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'property_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Exact location....'}),
            'Address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'your region, example: Uttara,Mirpur'}),
            'listing_category': forms.Select(attrs={'class': 'form-control'}),
            'sq_ft': forms.TextInput(attrs={'class': 'form-control'}),

            'bed_rooms': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Number of bed rooms...'}),
            'bath_rooms': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Number of bath rooms...'}),
            'picture': forms.FileInput(attrs={'class': 'form-control-file'})

        }

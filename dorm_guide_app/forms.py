from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Review, Property, Favourites, Location


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'phone', 'profile_picture', 'favourite_properties')



class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('latitude', 'longitude')


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'address', 'price_per_month', 'description', 'is_available', 'location', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Property Name', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'placeholder': 'Property Address', 'class': 'form-control'}),
            'price_per_month': forms.NumberInput(attrs={'placeholder': 'Price per Month', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control', 'rows': 5}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Property Name',
            'address': 'Address',
            'price_per_month': 'Price per Month',
            'description': 'Description',
            'is_available': 'Available for Rent',
            'location': 'Location (latitude & longitude)',
            'photo': 'Property Photo (optional)',
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['property', 'title', 'description', 'picture', 'rating', 'is_anonymous']
        widgets = {
            'property': forms.HiddenInput(),
            'title': forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control', 'rows': 5}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-control'}),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        labels = {
            'title': 'Title',
            'description': 'Description',
            'picture': 'Picture (optional)',
            'rating': 'Rating (1-5)',
            'is_anonymous': 'Post as anonymous',
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['property'].required = False
        self.fields['picture'].required = False


class FavouritesForm(forms.ModelForm):
    class Meta:
        model = Favourites
        fields = ['user', 'property']
        widgets = {
            'user': forms.HiddenInput(),
            'property': forms.HiddenInput(),
        }

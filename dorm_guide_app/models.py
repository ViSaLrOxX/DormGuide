from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.contrib.auth.models import User
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.apps import apps  

class University(models.Model):
    name = models.CharField(max_length=128)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    description = models.TextField(default="Description")
    picture = models.ImageField(upload_to="university_images/", blank=True, null=True)
    website = models.URLField(blank=True, default="")
    slug = models.SlugField(unique=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        if self.latitude > 90 or self.latitude < -90:
            raise ValidationError("Latitude must be between -90 and 90")
        if self.longitude > 180 or self.longitude < -180:
            raise ValidationError("Longitude must be between -180 and 180")


class Accommodation(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    rent_min = models.DecimalField(max_digits=9, decimal_places=2)
    rent_max = models.DecimalField(max_digits=9, decimal_places=2)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    reviews_no = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)
    
    def __str__(self):
        return f"{self.university.name} - {self.name}"

    def save(self, *args, **kwargs):
        if self.rent_min > self.rent_max:
            raise ValidationError("Rent Min cannot be greater than Rent Max.")
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        if self.rent_min < 0 or self.rent_max < 0:
            raise ValidationError("Rent values must be non-negative.")
        if self.rent_min > self.rent_max:
            raise ValidationError("Rent Min cannot be greater than Rent Max.")


class Review(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)  

    def clean(self):
        if self.rating < 0 or self.rating > 5:
            raise ValidationError("Rating must be between 0 and 5.")


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    favourite_properties = models.ManyToManyField(
        'Property', blank=True
    )

    def __str__(self):
        return f'{self.user.username} Profile'


class Location(models.Model):
    name = models.CharField(max_length=128)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name


class Property(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    
    def __str__(self):
        return self.name


class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.accommodation.name}"


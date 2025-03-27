from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from decimal import Decimal

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
    is_available = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='property_images/', blank=True, null=True)
    price_per_month = models.DecimalField(max_digits=9, decimal_places=2)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    picture = models.ImageField(upload_to='review_pictures/', null=True, blank=True)
    is_anonymous = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Review by {self.user} for {self.property}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    favourite_properties = models.ManyToManyField(
        Property, blank=True
    )

    def __str__(self):
        return f'{self.user.username} Profile'


class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.accommodation.name}"

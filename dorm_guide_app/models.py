from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone

class University(models.Model):
    NAME_MAX_LENGTH = 128
    DESCRIPTION_MAX_LENGTH = 2048
    SYNOPSIS_MAX_LENGTH = 1024

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    latitude = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        validators=[
            MaxValueValidator(90.0),
            MinValueValidator(-90.0),
        ],
        default=0,
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[
            MaxValueValidator(180.0),
            MinValueValidator(-180.0),
        ],
        default=0,
    )
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH, default="Description")
    picture = models.ImageField(upload_to='university_images', blank=True, null=True)
    website = models.URLField(blank=True)
    synopsis = models.CharField(max_length=SYNOPSIS_MAX_LENGTH, default="Synopsis")
    slug = models.SlugField(unique=True)
    email_domain = models.CharField(max_length=128, default="example.com")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(University, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Universities'

    def __str__(self):
        return self.name

class Accommodation(models.Model):
    NAME_MAX_LENGTH = 128
    DESCRIPTION_MAX_LENGTH = 2048

    university = models.ForeignKey(University, on_delete=models.CASCADE, blank=False)
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH, default="Description")
    latitude = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        validators=[
            MaxValueValidator(90.0),
            MinValueValidator(-90.0),
        ],
        default=0,
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[
            MaxValueValidator(180.0),
            MinValueValidator(-180.0),
        ],
        default=0,
    )
    rent_max = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[
            MinValueValidator(0.0),
        ],
        
        null=True,
        blank=True
    )
    rent_min = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[
            MinValueValidator(0.0),
        ],
        
        null=True,
        blank=True
    )
    avg_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[
            MaxValueValidator(5.0),
            MinValueValidator(1.0),
        ],
        null=True,
        blank=True
    )
    reviews_no = models.IntegerField(
        validators=[
            MinValueValidator(0),
        ],
        default=0
    )
    picture = models.ImageField(upload_to='accommodation_images', blank=True, null=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Accommodation, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('university', 'name')

    def __str__(self):
        return self.university.__str__() + " - " + self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    current_student = models.BooleanField(default=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

class Review(models.Model):
    TITLE_MAX_LENGTH = 128
    DESCRIPTION_MAX_LENGTH = 1024

    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, blank=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=False)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH)
    isAnonymous = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='review_images', blank=True, null=True)
    likes = models.IntegerField(
        validators=[
            MinValueValidator(0),
        ],
        default=0
    )
    rating = models.IntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1),
        ],
        default=5
    )
    datetime = models.DateTimeField(blank=False, default=timezone.now())

    def __str__(self):
        return self.accommodation.__str__() + " " + self.title + " by user " + self.user.__str__()

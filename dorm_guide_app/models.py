from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    profile_picture = models.ImageField(default='default.jpg', upload_to='media/profile_pictures')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    email = models.EmailField()
    phone = models.CharField(max_length=225)
    favourite_properties = models.ManyToManyField('Property',blank = True, related_name='favourite_properties')

    def __str__(self):
        return f'{self.user.username} Profile'
        

class Property(models.Model):
    name = models.CharField(max_length=225)
    address = models.TextField()
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
        
class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Favourite: {self.property.name}"

        
    
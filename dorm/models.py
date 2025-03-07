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
    


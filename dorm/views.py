from django.shortcuts import render
from .models import Property, UserProfile

def user_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'user_profile.html', {'profile': profile })


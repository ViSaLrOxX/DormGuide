from django.shortcuts import render, get_object_or_404, redirect
from .models import Property, UserProfile, Favourites
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def user_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        favourite_properties = Favourites.objects.filter(user=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('home')

    context = {
        'profile': profile,
        'favourite_properties': favourite_properties,
    }
    return render(request, 'user_profile.html', context)

@login_required
def add_to_favourites(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    favourite = Favourites.objects.get_or_create(user=request.user, property=property)
    
    if favourite:
        messages.success(request, f"{property.name} has been added to your favourites!")
    else:
        messages.info(request, f"{property.name} is already in your favourites.")

    return redirect('user_profile')

@login_required
def remove_from_favourites(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    favourite = Favourites.objects.filter(user=request.user, property=property)
    
    if favourite.exists():
        favourite.delete()
        messages.success(request, f"{property.name} has been removed from your favourites.")
    else:
        messages.warning(request, f"{property.name} was not in your favourites.")

    return redirect('user_profile')
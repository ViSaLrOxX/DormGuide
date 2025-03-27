from django.contrib import admin
from dorm_guide_app.models import Location, Property, UserProfile, Review, Favourites

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'price_per_month', 'is_available', 'created_at', 'location', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('property', 'user', 'title', 'rating', 'is_anonymous', 'datetime', 'likes')
    list_filter = ('rating', 'is_anonymous')
    search_fields = ('title', 'description')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'phone', 'profile_picture')

class FavouritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'added_on')
    search_fields = ('user__username', 'property__name')

class LocationAdmin(admin.ModelAdmin):
    list_display = ('latitude', 'longitude')
    search_fields = ('latitude', 'longitude')

admin.site.register(Property, PropertyAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Favourites, FavouritesAdmin)
admin.site.register(Location, LocationAdmin)

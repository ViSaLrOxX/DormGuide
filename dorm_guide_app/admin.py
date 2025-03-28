from django.contrib import admin
from dorm_guide_app.models import University, Accommodation, UserProfile, Review

class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'description', 'website')
    prepopulated_fields = {'slug': ('name',)}


class AccommodationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(University, UniversityAdmin)
admin.site.register(Accommodation, AccommodationAdmin)
admin.site.register(Review)
admin.site.register(UserProfile)

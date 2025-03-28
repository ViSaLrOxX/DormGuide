from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dorm-guide/', include('dorm_guide_app.urls')),
    path('accounts/', include('registration.backends.default.urls')),  
]

"""dorm_guide URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dorm_guide_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('universities/', views.university_list, name='university_list'),
    path('universities/<int:university_id>/accommodations/', views.accommodation_list, name='accommodation_list'),
    path('accommodations/<int:accommodation_id>/reviews/', views.review_list, name='review_list'),

    path('api/universities/', views.api_universities, name='api_universities'),
    path('api/universities/<int:university_id>/accommodations/', views.api_accommodations, name='api_accommodations'),
    path('api/accommodations/<int:accommodation_id>/reviews/', views.api_reviews, name='api_reviews'),
]

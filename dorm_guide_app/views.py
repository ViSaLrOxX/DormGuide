import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Avg, Q
from dorm_guide.models import University, Accommodation, Review
from dorm_guide.forms import ReviewForm
from .forms import UserProfileForm

logger = logging.getLogger(__name__)

def index(request):
    """Home page showing university listings."""
    universities = University.objects.all().order_by('name')

    paginator = Paginator(universities, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    logger.info(f"Loaded index page with {universities.count()} universities.")
    return render(request, 'dorm_guide/index.html', {'page_obj': page_obj})


def university_detail(request, university_id):
    """Displays details for a single university."""
    university = get_object_or_404(University, id=university_id)
    accommodations = university.accommodation_set.all()

    logger.info(f"Viewing details for {university.name} with {accommodations.count()} accommodations.")
    return render(request, 'dorm_guide/university_detail.html', {'university': university, 'accommodations': accommodations})


@login_required
def accommodation_detail(request, accommodation_id):
    """Shows detailed view of an accommodation."""
    accommodation = get_object_or_404(Accommodation, id=accommodation_id)
    reviews = accommodation.review_set.all().order_by('-created_at')

    
    paginator = Paginator(reviews, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = ReviewForm()

    logger.info(f"Viewing accommodation {accommodation.name} with {reviews.count()} reviews.")
    return render(
        request,
        'dorm_guide/accommodation_detail.html',
        {'accommodation': accommodation, 'page_obj': page_obj, 'form': form}
    )


@login_required
def add_review(request, accommodation_id):
    """Adds a new review to an accommodation."""
    accommodation = get_object_or_404(Accommodation, id=accommodation_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)

        if form.is_valid():
            review = form.save(commit=False)
            review.accommodation = accommodation
            review.user = request.user
            review.save()

            logger.info(f"Added review {review.title} by {request.user.username}")
            return redirect('accommodation_detail', accommodation_id=accommodation_id)
        else:
            logger.warning(f"Invalid review form submission by {request.user.username}")

    return render(request, 'dorm_guide/add_review.html', {'form': form, 'accommodation': accommodation})


@login_required
def like_review(request, review_id):
    """Increments the like count of a review."""
    review = get_object_or_404(Review, id=review_id)
    review.likes += 1
    review.save()

    logger.info(f"Review {review.title} liked. Total likes: {review.likes}")
    return JsonResponse({'likes': review.likes})


def search(request):
    """Search for accommodations or universities."""
    query = request.GET.get('q', '')
    results = []

    if query:
        results = Accommodation.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ) | University.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    logger.info(f"Search query: '{query}' returned {len(results)} results.")
    return render(request, 'dorm_guide/search_results.html', {'results': results, 'query': query})


@login_required
def edit_profile(request):
    """Edit the user's profile."""
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile') 
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'dorm_guide/edit_profile.html', {'form': form})

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from dorm_guide_app.models import *
from django.contrib.auth import logout
from dorm_guide_app.forms import ReviewForm


def index(request):
    universities = University.objects.all()
    universities_supported = universities.count()
    students_no = User.objects.all().count()

    try:
        accommodations = Accommodation.objects.all()

        accommodations_ratings = {}

        total_reviews = 0

        total_likes = 0

        for accommodation in accommodations:
            rating_score = 0
            reviews = Review.objects.filter(accommodation=accommodation)

            if reviews.count() > 0:
                total_reviews += reviews.count()

                for review in reviews:
                    rating_score += review.rating
                    total_likes += review.likes

                rating_score / reviews.count()

                accommodations_ratings[accommodation] = rating_score

        highest_rated_accommodations = sorted(accommodations_ratings, key=accommodations_ratings.get)[:4]

    except Accommodation.DoesNotExist:
        highest_rated_accommodations = None
        total_reviews = None

    context = {"universities": universities, "universities_supported": universities_supported,
               "accommodations": highest_rated_accommodations, "total_reviews": total_reviews,
               "students_no": students_no, "total_likes": total_likes}
    template_name = 'dorm_guide_app/index.html'
    return render(request, template_name, context)


def about(request):
    universities = University.objects.all()
    context = {"universities": universities}
    template_name = 'dorm_guide_app/about.html'
    return render(request, template_name, context)


def contact_us(request):
    universities = University.objects.all()
    context = {"universities": universities}
    template_name = 'dorm_guide_app/contact_us.html'
    return render(request, template_name, context)


def faq(request):
    universities = University.objects.all()
    context = {"universities": universities}
    template_name = 'dorm_guide_app/faq.html'
    return render(request, template_name, context)


@login_required
def my_account(request, user_id):
    user = User.objects.get(id=user_id)
    user_profile = UserProfile.objects.get(user=user)
    universities = University.objects.all()
    reviews = Review.objects.filter(user=user.userprofile)
    context = {"universities": universities, "reviews": reviews, "user": user, "user_profile": user_profile}
    template_name = 'dorm_guide_app/my_account.html'
    return render(request, template_name, context)


@login_required
def delete_account(request, user_id):
    logout(request)

    user = User.objects.get(id=user_id)
    user_profile = UserProfile.objects.get(user=user)

    user_profile.delete()
    user.delete()

    return redirect("/dorm-guide/")


def custom_logout(request):
    logout(request)
    return redirect('index')


def universities(request):
    universities = University.objects.all()
    accommodations = Accommodation.objects.all()
    context = {"universities": universities, "accommodations": accommodations}
    template_name = 'dorm_guide_app/universities.html'
    return render(request, template_name, context)


def university(request, university_slug):
    universities = University.objects.all()

    try:
        university = University.objects.get(slug=university_slug)
        accommodations = Accommodation.objects.filter(university=university)
    except University.DoesNotExist:
        university = None
        accommodations = None

    if university is None:
        return redirect('/dorm-guide/')

    context = {"universities": universities, "university": university, "accommodations": accommodations}
    template_name = 'dorm_guide_app/university.html'
    return render(request, template_name, context)


def accommodation(request, university_slug, accommodation_slug):
    universities = University.objects.all()

    try:
        accommodation = Accommodation.objects.get(slug=accommodation_slug)
        university = accommodation.university
        reviews = Review.objects.filter(accommodation=accommodation).order_by('-datetime')

        avg_rating = 0
        for review in reviews:
            rating = review.rating
            avg_rating += rating

        rating_no = reviews.count()
        if rating_no >= 1:
            avg_rating /= rating_no
            avg_rating = round(avg_rating, 1)

    except Accommodation.DoesNotExist:
        accommodation = None
        university = None
        avg_rating = None
        rating_no = None
    except Review.DoesNotExist:
        reviews = None
        avg_rating = None
        rating_no = None

    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            pass

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.accommodation = accommodation
            review.user = user_profile
            review.save()
            return redirect('.')
    else:
        form = ReviewForm()

    context = {"universities": universities, "accommodation": accommodation, "university": university,
               "reviews": reviews, "avg_rating": avg_rating, "rating_no": rating_no, "form": form,
               "user_profile": user_profile}
    template_name = 'dorm_guide_app/accommodation.html'
    return render(request, template_name, context)


def add_like(request):
    if request.method == "POST":
        pk = request.POST["pk"]

        try:
            review = Review.objects.get(pk=pk)
            review.likes += 1
            review.save()
        except Review.DoesNotExist:
            pass
    return HttpResponse()


@login_required
def logout_account(request):
    logout(request)

    return redirect("/dorm-guide/")

import tempfile
from django.apps import apps
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from decimal import Decimal
from dorm_guide_app.models import University, Accommodation, Review
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserForm, UserProfileForm

class UniversityModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        University.objects.create(name='University of Test', latitude=37.7749, longitude=-122.4194)

    def test_name_max_length(self):
        university = University.objects.get(id=1)
        max_length = university._meta.get_field('name').max_length
        self.assertEquals(max_length, 128)

    def test_longitude_min_value(self):
        university = University.objects.get(id=1)
        min_value = university._meta.get_field('longitude').validators[1].limit_value
        self.assertEquals(min_value, -180.0)

    def test_description_default_value(self):
        university = University.objects.get(id=1)
        default_value = university._meta.get_field('description').default
        self.assertEquals(default_value, 'Description')

    def test_latitude_default_value(self):
        university = University.objects.get(id=1)
        default_value = university._meta.get_field('latitude').default
        self.assertEquals(default_value, 0)

    def test_longitude_default_value(self):
        university = University.objects.get(id=1)
        default_value = university._meta.get_field('longitude').default
        self.assertEquals(default_value, 0)

    def test_picture_upload_to(self):
        university = University.objects.get(id=1)
        upload_to = university._meta.get_field('picture').upload_to
        self.assertEquals(upload_to, 'university_images')

    def test_website_blank(self):
        university = University.objects.get(id=1)
        self.assertEquals(university.website, '')

    def test_latitude_range(self):
        with self.assertRaises(ValidationError):
            University.objects.create(name='Test University', latitude=100, longitude=-122.4194)

        with self.assertRaises(ValidationError):
            University.objects.create(name='Test University', latitude=-100, longitude=-122.4194)

    def test_longitude_range(self):
        with self.assertRaises(ValidationError):
            University.objects.create(name='Test University', latitude=37.7749, longitude=200)

        with self.assertRaises(ValidationError):
            University.objects.create(name='Test University', latitude=37.7749, longitude=-200)

    def test_latitude_max_value_validator(self):
        max_value = University._meta.get_field('latitude').validators[0].limit_value
        self.assertEqual(max_value, 90.0)

    def test_latitude_min_value_validator(self):
        min_value = University._meta.get_field('latitude').validators[1].limit_value
        self.assertEqual(min_value, -90.0)

    def test_longitude_max_value_validator(self):
        max_value = University._meta.get_field('longitude').validators[0].limit_value
        self.assertEqual(max_value, 180.0)

    def test_longitude_min_value_validator(self):
        min_value = University._meta.get_field('longitude').validators[1].limit_value
        self.assertEqual(min_value, -180.0)

    def test_default_latitude(self):
        university = University.objects.create(name='Test University')
        self.assertEqual(university.latitude, 0)

    def test_default_longitude(self):
        university = University.objects.create(name='Test University')
        self.assertEqual(university.longitude, 0)

    def test_slug_creation(self):
        university = University.objects.create(name="Test University")
        self.assertEqual(university.slug, "test-university")

    def test_string_representation(self):
        university = University.objects.create(name="Test University")
        self.assertEqual(str(university), "Test University")

class AccommodationModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.university = University.objects.create(name='Test University')

    def test_name_max_length(self):
        name = 'a' * 129
        accommodation = Accommodation(name=name, university=self.university)
        with self.assertRaises(ValidationError):
            accommodation.full_clean()

    def test_rent_validation(self):
        accommodation = Accommodation.objects.create(
            university=self.university,
            name="Test Accommodation",
            description="Test Description",
            latitude=37.7749,
            longitude=-122.4194,
            rent_min=500,
            rent_max=1000
        )
       
        try:
            accommodation.full_clean()  
        except ValidationError:
            self.fail("Accommodation should be valid when rent_max is greater than rent_min")

        accommodation_invalid = Accommodation(
            university=self.university,
            name="Test Accommodation Invalid",
            description="Test Description",
            latitude=37.7749,
            longitude=-122.4194,
            rent_min=1000, 
            rent_max=500
        )
        with self.assertRaises(ValidationError):
            accommodation_invalid.full_clean()  

    def test_slug_creation(self):
        accommodation = Accommodation.objects.create(
            university=self.university,
            name="Test Accommodation",
            description="Test Description",
            latitude=37.7749,
            longitude=-122.4194,
            rent_min=500,
            rent_max=1000
        )
        self.assertEqual(accommodation.slug, "test-accommodation")

    def test_string_representation(self):
        accommodation = Accommodation.objects.create(
            university=self.university,
            name="Test Accommodation",
            description="Test Description",
            latitude=37.7749,
            longitude=-122.4194,
            rent_min=500,
            rent_max=1000
        )
        self.assertEqual(str(accommodation), "Test University - Test Accommodation")

    def test_accommodation_latitude_longitude_range(self):
        accommodation = Accommodation(
            university=self.university,
            name="Test Accommodation",
            description="Test Description",
            latitude=200,  
            longitude=-122.4194,
            rent_min=500,
            rent_max=1000
        )
        with self.assertRaises(ValidationError):
            accommodation.full_clean()

        accommodation.latitude = 37.7749  
        accommodation.longitude = 500 
        with self.assertRaises(ValidationError):
            accommodation.full_clean()

        accommodation.longitude = -122.4194 
        accommodation.full_clean()  

class ReviewModelTest(TestCase):
    def setUp(self):
        self.university = University.objects.create(name='Test University')
        self.accommodation = Accommodation.objects.create(
            name='Test Accommodation',
            description='Test Description',
            latitude=0,
            longitude=0,
            rent_min=100,
            rent_max=200,
            university=self.university
        )
        self.userprofile = UserProfile.objects.create(
            user=User.objects.create_user('testuser', password='testpass')
        )

    def test_create_review(self):
        review = Review.objects.create(
            title='Test Title',
            description='Test Description',
            likes=10,
            rating=3,
            accommodation=self.accommodation,
            user=self.userprofile
        )
        self.assertEqual(review.title, 'Test Title')
        self.assertEqual(review.description, 'Test Description')
        self.assertEqual(review.likes, 10)
        self.assertEqual(review.rating, 3)
        self.assertEqual(review.accommodation, self.accommodation)
        self.assertEqual(review.user, self.userprofile)

    def test_create_review_invalid_rating(self):
        with self.assertRaises(Exception):
            review = Review.objects.create(
                title='Test Title',
                description='Test Description',
                likes=10,
                rating=6,  
                accommodation=self.accommodation,
                user=self.userprofile
            )

class UserProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testpass')
        cls.user_profile = UserProfile.objects.create(user=cls.user, current_student=True)

    def test_current_student_default_value(self):
        user_profile = UserProfile.objects.get(id=1)
        self.assertEqual(user_profile.current_student, True)

    def test_string_representation(self):
        self.assertEqual(str(self.user_profile), self.user.username)

    def test_create_userprofile(self):
        self.assertEqual(self.user_profile.user.username, 'testuser')
        self.assertEqual(self.user_profile.current_student, True)

class UserFormTest(TestCase):
    def test_user_form_password_field(self):
        form = UserForm()
        self.assertTrue(form.fields['password'].widget.input_type == 'password')

class UserProfileFormTest(TestCase):
    def test_user_profile_form_fields(self):
        form = UserProfileForm()
        self.assertTrue('current_student' in form.fields)

class UniversityImageUploadTest(TestCase):
    def test_upload_image(self):
        university = University.objects.create(name='Test University')
        with tempfile.NamedTemporaryFile(suffix='.jpg') as f:
            image = SimpleUploadedFile(name='test_image.jpg', content=f.read(), content_type='image/jpeg')
            university.picture = image
            university.save()
            self.assertTrue(university.picture)

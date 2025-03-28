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

class UserProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='testpass')
        UserProfile.objects.create(user=user, current_student=True)

    def test_current_student_default_value(self):
        user_profile = UserProfile.objects.get(id=1)
        default_value = user_profile._meta.get_field('current_student').default
        self.assertEquals(default_value, False)

class UniversityModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        University.objects.create(name='Test University', latitude=37.7749, longitude=-122.4194, description='Test Description', website='https://testuniversity.com')

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


class UniversityModelTestCase(TestCase):
    def test_latitude_field(self):
        university = University.objects.create(name='Test University', latitude=37.7749, longitude=-122.4194)
        self.assertIsInstance(university.latitude, Decimal)
        self.assertEqual(university.latitude.as_tuple().exponent, -6)

    def test_longitude_field(self):
        university = University.objects.create(name='Test University', latitude=37.7749, longitude=-122.4194)
        self.assertIsInstance(university.longitude, Decimal)
        self.assertEqual(university.longitude.as_tuple().exponent, -9)


class UniversityModelTestCase(TestCase):
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

class UniversityModelTestCase(TestCase):
    def test_default_latitude(self):
        university = University.objects.create(name='Test University')
        self.assertEqual(university.latitude, 0)

    def test_default_longitude(self):
        university = University.objects.create(name='Test University')
        self.assertEqual(university.longitude, 0)

class MigrationTestCase(TestCase):
    migrate_from = 'dorm_guide_app.0001_initial'
    migrate_to = 'dorm_guide_app.0002_add_fields_to_university'

    def setUp(self):
        self.app = apps.get_containing_app_config(type('TempConfig', (object,), {'label': 'dorm_guide_app'}).__dict__['label'])
        self.old_apps = self.app.apps
        self.app.apps = self.new_apps = apps.all_models.copy()

    def tearDown(self):
        self.app.apps = self.old_apps

    def test_add_description_field(self):
        university_model = self.new_apps['dorm_guide_app']['University']
        self.assertIn('description', university_model._meta.get_fields())

    def test_add_picture_field(self):
        university_model = self.new_apps['dorm_guide_app']['University']
        self.assertIn('picture', university_model._meta.get_fields())

    def test_add_website_field(self):
        university_model = self.new_apps['dorm_guide_app']['University']
        self.assertIn('website', university_model._meta.get_fields())


class MigrationTestCase(TestCase):
    
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

    def test_latitude_default_value(self):
        default_value = University._meta.get_field('latitude').default
        self.assertEqual(default_value, 0)

    def test_longitude_default_value(self):
        default_value = University._meta.get_field('longitude').default
        self.assertEqual(default_value, 0)


class UniversityModelTest(TestCase):
    def test_upload_image(self):
        university = University.objects.create(name='Test University')
        with tempfile.NamedTemporaryFile(suffix='.jpg') as f:
            image = SimpleUploadedFile(name='test_image.jpg', content=f.read(), content_type='image/jpeg')
            university.picture = image
            university.save()
            self.assertTrue(university.picture)

class UserProfileModelTest(TestCase):
    def test_create_userprofile(self):
        userprofile = UserProfile.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.assertEqual(userprofile.username, 'testuser')
        self.assertEqual(userprofile.email, 'testuser@example.com')
        self.assertEqual(userprofile.password, 'testpassword')


    def test_create_accommodation(self):
        self.assertEqual(self.accommodation.name, 'Test Accommodation')
        self.assertEqual(self.accommodation.description, 'Test Description')
        self.assertEqual(self.accommodation.latitude, 0)
        self.assertEqual(self.accommodation.longitude, 0)
        self.assertEqual(self.accommodation.rent_min, 100)
        self.assertEqual(self.accommodation.rent_max, 200)
        self.assertEqual(self.accommodation.university, self.university)

    def test_unique_accommodation(self):
        accommodation2 = Accommodation(
            name='Test Accommodation',
            description='Test Description',
            latitude=0,
            longitude=0,
            rent_min=100,
            rent_max=200,
            university=self.university
        )
        with self.assertRaises(Exception):
            accommodation2.save()

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
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
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
            review = Review.objects.create\
            (
                title='Test Title',
                description='Test Description',
                likes=10,
                rating=6,
                accommodation=self.accommodation,
                user=self.userprofile
            )

class UniversityViewTest(TestCase):
    def setUp(self):
        self.university = University.objects.create(name='Test University')
        self.url = reverse('university', args=[self.university.id])

class AccommodationModelTest(TestCase):
    
    def setUp(self):
        self.university = University.objects.create(name='Test University')
    
    def test_name_max_length(self):
        name = 'a' * 129
        accommodation = Accommodation(name=name, university=self.university)
        with self.assertRaises(ValidationError):
            accommodation.full_clean()
    
    def test_name_unique_together_with_university(self):
        name = 'Test Accommodation'
        Accommodation.objects.create(name=name, university=self.university)
        accommodation = Accommodation(name=name, university=self.university)
        with self.assertRaises(ValidationError):
            accommodation.full_clean()

class UniversityModelTest(TestCase):
    def setUp(self):
        self.university = University.objects.create(name="Test University", latitude=51.5074, longitude=0.1278)

    def test_string_representation(self):
        self.assertEqual(str(self.university), "Test University")

    def test_slug_field(self):
        self.assertEqual(self.university.slug, "test-university")


class AccommodationModelTest(TestCase):
    def setUp(self):
        self.university = University.objects.create(name="Test University", latitude=51.5074, longitude=0.1278)
        self.accommodation = Accommodation.objects.create(university=self.university, name="Test Accommodation", latitude=51.5074, longitude=0.1278)

    def test_string_representation(self):
        self.assertEqual(str(self.accommodation), "Test University - Test Accommodation")

    def test_slug_field(self):
        self.assertEqual(self.accommodation.slug, "test-accommodation")


    def test_reviews_no_default(self):
        self.assertEqual(self.accommodation.reviews_no, 0)

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(user=User.objects.create_user("testuser", password="testpass"))

    def test_string_representation(self):
        self.assertEqual(str(self.user), "testuser")


class ReviewModelTest(TestCase):
    def setUp(self):
        self.university = University.objects.create(name="Test University", latitude=51.5074, longitude=0.1278)
        self.accommodation = Accommodation.objects.create(university=self.university, name="Test Accommodation", latitude=51.5074, longitude=0.1278)
        self.user = UserProfile.objects.create(user=User.objects.create_user("testuser", password="testpass"))
        self.review = Review.objects.create(accommodation=self.accommodation, user=self.user, title="Test Review")

class UniversityTestCase(TestCase):
    def setUp(self):
        self.university = University.objects.create(
            name="Test University",
            latitude=37.7749,
            longitude=-122.4194,
            description="Test description",
            website="https://www.testuniversity.com",
            synopsis="Test synopsis"
        )

    def test_slug_creation(self):
        self.assertEqual(self.university.slug, "test-university")

    def test_latitude_validation(self):
        
        with self.assertRaises(ValidationError):
            self.university.latitude = 100.0
            self.university.full_clean()

        with self.assertRaises(ValidationError):
            self.university.latitude = -100.0
            self.university.full_clean()

    def test_longitude_validation(self):
        
        with self.assertRaises(ValidationError):
            self.university.longitude = 200.0
            self.university.full_clean()

        with self.assertRaises(ValidationError):
            self.university.longitude = -200.0
            self.university.full_clean()

class AccommodationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.userprofile = UserProfile.objects.create(user=self.user)
        self.university = University.objects.create(
            name="Test University",
            latitude=37.7749,
            longitude=-122.4194,
            description="Test description",
            website="https://www.testuniversity.com",
            synopsis="Test synopsis"
        )
        self.accommodation = Accommodation.objects.create(
            university=self.university,
            name="Test Accommodation",
            description="Test description",
            latitude=37.7749,
            longitude=-122.4194,
            rent_max=1000.00,
            rent_min=500.00,
            avg_rating=4.5,
            reviews_no=5
        )

    def test_slug_creation(self):
        self.assertEqual(self.accommodation.slug, "test-accommodation")

    def test_rent_validation(self):
        # Test validation for rent range
        with self.assertRaises(ValidationError):
            self.accommodation.rent_max = -100.0
            self.accommodation.full_clean()

        with self.assertRaises(ValidationError):
            self.accommodation.rent_min = -100.0
            self.accommodation.full_clean()

    def test_rating_validation(self):
        
        with self.assertRaises(ValidationError):
            self.accommodation.avg_rating = 6.0
            self.accommodation.full_clean()

        with self.assertRaises(ValidationError):
            self.accommodation.avg_rating = 0.0
            self.accommodation.full_clean()

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.userprofile = UserProfile.objects.create(user=self.user)

    def test_string_representation(self):
        self.assertEqual(str(self.userprofile), self.user.username)

class ReviewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.userprofile = UserProfile.objects.create(user=self.user)
        self.university = University.objects.create(
            name="Test University",
            latitude=37.7749,
            longitude=-122.4194,
            description="Test description",
            website="https://www.testuniversity.com",
            synopsis="Test synopsis"
        )

class UserFormTest(TestCase):
    def test_user_form_password_field(self):
        form = UserForm()
        self.assertTrue(form.fields['password'].widget.input_type == 'password')

class UserProfileFormTest(TestCase):
    def test_user_profile_form_fields(self):
        form = UserProfileForm()
        self.assertTrue('current_student' in form.fields)

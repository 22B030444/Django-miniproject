
from django.test import TestCase
from future.backports.email.headerregistry.Address import username
from rest_framework import status
from django.core.cache import cache
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from students.models import Student
from django.contrib.auth import get_user_model


class StudentCacheTest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='student', email='student@test.com', password='password123')
        self.student_profile = Student.objects.create(
            user=self.user,
            name='Student Name',
            email='student@test.com',
            dob='1995-01-01'
        )

    def test_student_profile_cache(self):
        """Test caching for student profile data."""
        cache_key = f'student_profile_{self.student_profile.id}'
        cached_student = cache.get(cache_key)
        self.assertIsNone(cached_student)

        # Fetch student profile to populate the cache
        url = reverse('student-detail', args=[self.student_profile.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Verify cache is populated
        cached_student = cache.get(cache_key)
        self.assertIsNotNone(cached_student)
        self.assertEqual(cached_student['name'], self.student_profile.name)

        # Invalidate cache by updating the student profile
        data = {'name': 'Updated Name'}
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        cached_student = cache.get(cache_key)
        self.assertIsNone(cached_student)


class StudentViewSetTest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.student_user = User.objects.create_user(username='student', email='student@test.com', password='password123')
        self.admin_user = User.objects.create_superuser(username='admin', email='admin@test.com', password='adminpass123')

        self.student_profile = Student.objects.create(
            user=self.student_user,
            name='Student Name',
            email='student@test.com',
            dob='1995-01-01'
        )

    def test_student_create(self):
        """Test creating a new student profile as an admin."""
        url = reverse('student-list')
        data = {'name': 'New Student', 'email': 'newstudent@test.com', 'dob': '2000-01-01'}
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)

    def test_student_update(self):
        """Test updating a student profile by the student."""
        url = reverse('student-detail', args=[self.student_profile.id])
        data = {'name': 'Updated Student Name'}
        self.client.force_authenticate(user=self.student_user)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student_profile.refresh_from_db()
        self.assertEqual(self.student_profile.name, 'Updated Student Name')

    def test_student_delete(self):
        """Test deleting a student profile as an admin."""
        url = reverse('student-detail', args=[self.student_profile.id])
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.count(), 0)


    def test_role_based_permission(self):
        """Test that a student cannot update another student's profile."""
        another_student_user = get_user_model().objects.create_user(username='anotherstudent', email='anotherstudent@test.com', password='password123')
        another_student_profile = Student.objects.create(
            user=another_student_user,
            name='Another Student',
            email='anotherstudent@test.com',
            dob='1998-01-01'
        )

        url = reverse('student-detail', args=[another_student_profile.id])
        data = {'name': 'Invalid Update'}
        self.client.force_authenticate(user=self.student_user)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class StudentModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='teststudent', email='test@student.com', password='password123')
        self.student = Student.objects.create(
            user=self.user,
            name='John Doe',
            email='john.doe@student.com',
            dob='2000-01-01'
        )

    def test_student_model(self):
        """Test if the student instance is correctly saved."""
        self.assertEqual(self.student.name, 'John Doe')
        self.assertEqual(self.student.user.username, 'teststudent')

    def test_student_email_uniqueness(self):
        """Test that the email field in Student is unique."""
        with self.assertRaises(Exception):
            Student.objects.create(
                user=self.user,
                name='Duplicate Student',
                email='john.doe@student.com',  # Duplicate email
                dob='2001-01-01'
            )

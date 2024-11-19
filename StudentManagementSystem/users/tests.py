from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from students.models import Student

class RegistrationTests(APITestCase):
    """
    Test cases for user registration.
    """
    def test_user_registration(self):
        """
        Ensure a user can register with valid data.
        """
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "strongpassword123",
            "role": "STUDENT",
        }
        response = self.client.post('/users/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['role'], data['role'])

    def test_invalid_registration(self):
        """
        Ensure invalid data returns an appropriate error.
        """
        data = {
            "username": "",
            "email": "invalid-email",
            "password": "short",
            "role": "INVALID_ROLE",
        }
        response = self.client.post('/users/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)
        self.assertIn("role", response.data)


class StudentViewSetTests(APITestCase):
    """
    Test cases for the StudentViewSet.
    """
    def setUp(self):
        """
        Create users and students for testing.
        """
        self.student_user = get_user_model().objects.create_user(
            username="studentuser",
            email="studentuser@example.com",
            password="password123",
            role="STUDENT",
        )
        self.admin_user = get_user_model().objects.create_user(
            username="adminuser",
            email="adminuser@example.com",
            password="password123",
            role="ADMIN",
        )
        self.student = Student.objects.create(user=self.student_user)

    def test_student_access_own_data(self):
        """
        Ensure a student can access their own record.
        """
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(f'/users/students/{self.student.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_cannot_access_others_data(self):
        """
        Ensure a student cannot access another student's record.
        """
        other_student = Student.objects.create(user=get_user_model().objects.create_user(
            username="otherstudent",
            email="otherstudent@example.com",
            password="password123",
            role="STUDENT",
        ))
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(f'/users/students/{other_student.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_access_any_student_data(self):
        """
        Ensure an admin can access any student's record.
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(f'/users/students/{self.student.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_create_student(self):
        """
        Ensure an admin can create a new student.
        """
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "user": {
                "username": "newstudent",
                "email": "newstudent@example.com",
                "password": "password123",
                "role": "STUDENT"
            }
        }
        response = self.client.post('/users/students/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def tearDown(self):
        """
        Clean up after each test.
        """
        get_user_model().objects.all().delete()
        Student.objects.all().delete()
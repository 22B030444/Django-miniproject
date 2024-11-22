from django.test import TestCase
from rest_framework.authtoken.admin import User
from django.core.cache import cache
from rest_framework.test import APITestCase
from courses.models import Course, Enrollment
from students.models import Student
class CourseViewSetTest(APITestCase):
    def setUp(self):
        # Создаем пользователя и студента
        self.user = User.objects.create_user(
            username="student",
            email="student@example.com",
            password="password"
        )
        self.student = Student.objects.create(
            user=self.user,
            name="Test Student",
            email="student@example.com"
        )
        self.course = Course.objects.create(name="Test Course")

    def test_student_enrollment(self):
        """Тест успешного зачисления студента"""
        self.client.login(username="student", password="password")
        response = self.client.post("/courses/api/v1/enrollments/", {
            "student": self.student.id,
            "course": self.course.id
        })
        self.assertEqual(response.status_code, 201)

    def test_duplicate_enrollment(self):
        """Тест предотвращения дублирующего зачисления"""
        Enrollment.objects.create(student=self.student, course=self.course)
        response = self.client.post("/courses/api/v1/enrollments/", {
            "student": self.student.id,
            "course": self.course.id
        })
        self.assertEqual(response.status_code, 400)

    def test_course_retrieval_with_cache(self):
        """Тест получения данных с использованием кеша"""
        cache_key = f"course_{self.course.id}"
        cache.set(cache_key, {"id": self.course.id, "name": "Cached Course"}, timeout=300)

        response = self.client.get(f"/courses/api/v1/courses/{self.course.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Cached Course")

class CourseModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name="Test Course")

    def test_course_creation(self):
        """Тест успешного создания курса"""
        self.assertEqual(str(self.course), "Test Course")

from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from students.models import Student
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class StudentViewSetTest(APITestCase):
    def setUp(self):
        # Создаем администратора
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password"
        )
        # Создаем студента
        self.student_user = User.objects.create_user(
            username="student",
            email="student@example.com",
            password="password"
        )
        self.student = Student.objects.create(
            user=self.student_user,
            name="Test Student",
            email="student@example.com"
        )

    def get_access_token(self, user):
        """Генерация токена для пользователя"""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_student_list_as_admin(self):
        """Администратор может получить список студентов"""
        # Аутентифицируем администратора
        token = self.get_access_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get("/students/api/v1/students/")
        self.assertEqual(response.status_code, 200)

    def test_student_update_permission(self):
        """Студент не может обновить чужие данные"""
        # Аутентифицируем студента
        token = self.get_access_token(self.student_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Отправляем запрос с минимально необходимыми данными
        response = self.client.put(f"/students/api/v1/students/{self.student.id}/", {
            "name": "Updated Name",
            "email": "student@example.com",
            "dob": "2000-01-01",  # Убедитесь, что это поле передается
            "courses": []  # Пустой список курсов, если требуется
        }, format='json')

        # Проверяем код ответа
        self.assertEqual(response.status_code, 403)  # Доступ запрещен


class StudentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password"
        )
        self.student = Student.objects.create(
            user=self.user,
            name="Test Student",
            email="testuser@example.com"
        )

    def test_student_creation(self):
        """Тест успешного создания студента"""
        self.assertEqual(self.student.name, "Test Student")
        self.assertEqual(self.student.email, "testuser@example.com")

    def test_unique_email(self):
        """Тест ограничения уникальности email"""
        with self.assertRaises(Exception):
            Student.objects.create(
                user=self.user,
                name="Another Student",
                email="testuser@example.com"  # Дубликат email
            )

    def test_student_update_permission(self):
        """Студент не может обновить чужие данные"""
        # Аутентифицируем студента
        token = self.get_access_token(self.student_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Отправляем запрос с минимально необходимыми данными
        response = self.client.put(f"/students/api/v1/students/{self.student.id}/", {
            "name": "Updated Name",
            "email": "student@example.com",
        }, format='json')

        # Проверяем код ответа
        self.assertEqual(response.status_code, 403)  # Доступ запрещен

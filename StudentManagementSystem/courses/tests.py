from rest_framework.test import APITestCase
from students.models import Student
from courses.models import Course, Enrollment


class EnrollmentSerializerTest(APITestCase):
    def setUp(self):
        self.student = Student.objects.create(username='test_student', email='test@example.com', role='STUDENT')
        self.course = Course.objects.create(name='Test Course')

    def test_enrollment_creation(self):
        response = self.client.post('/api/v1/enrollments/', {
            'student': self.student.id,
            'course': self.course.id,
        })
        self.assertEqual(response.status_code, 201)  # Проверяем, что создание прошло успешно

    def test_duplicate_enrollment(self):
        Enrollment.objects.create(student=self.student, course=self.course)  # Создаем первое зачисление
        response = self.client.post('/api/v1/enrollments/', {
            'student': self.student.id,
            'course': self.course.id,
        })
        self.assertEqual(response.status_code, 400)  # Должен вернуть ошибку
        self.assertIn("Student is already enrolled in this course.", response.data['non_field_errors'])
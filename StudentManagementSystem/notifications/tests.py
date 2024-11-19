# notifications/tests.py

from django.test import TestCase
from unittest.mock import patch
from notifications.tasks import send_attendance_reminder, send_grade_update_notification
from students.models import Student
from grades.models import Grade
from django.conf import settings

class NotificationsTests(TestCase):

    def setUp(self):
        # Создание студента для тестов
        self.student = Student.objects.create(
            username='testuser',
            email='test@student.com',
            password='password'
        )

    @patch('notifications.tasks.send_mail')  # Mock send_mail to avoid real emails
    def test_send_attendance_reminder(self, mock_send_mail):
        # Вызов задачи Celery
        send_attendance_reminder()

        # Проверка, что email был отправлен
        mock_send_mail.assert_called_once_with(
            'Daily Attendance Reminder',
            f'Hello {self.student.name}, please mark your attendance for today.',
            settings.DEFAULT_FROM_EMAIL,  # Используем настройку отправителя
            [self.student.email],
            fail_silently=False,
        )

    @patch('notifications.tasks.send_mail')
    def test_send_grade_update_notification(self, mock_send_mail):
        # Создание оценки для студента
        grade = Grade.objects.create(
            student=self.student,
            score=90,
            course='Test Course'
        )

        # Вызов задачи Celery
        send_grade_update_notification(grade.id)

        # Проверка, что email был отправлен
        mock_send_mail.assert_called_once_with(
            'Grade Update Notification',
            f'Hello {self.student.name}, your grade for Test Course has been updated.',
            settings.DEFAULT_FROM_EMAIL,  # Используем настройку отправителя
            [self.student.email],
            fail_silently=False,
        )
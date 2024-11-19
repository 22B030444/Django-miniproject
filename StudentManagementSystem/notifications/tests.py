# notifications/tests.py

from django.test import TestCase
from unittest.mock import patch
from notifications.tasks import send_attendance_reminder, send_grade_update_notification
from students.models import Student
from grades.models import Grade


class NotificationsTests(TestCase):

    @patch('notifications.tasks.send_mail')  # Mock send_mail to avoid real emails
    def test_send_attendance_reminder(self, mock_send_mail):
        # Create a student
        student = Student.objects.create(
            username='testuser',
            email='test@student.com',
            password='password'
        )

        # Call the Celery task
        send_attendance_reminder()

        # Check if the email was sent
        mock_send_mail.assert_called_with(
            'Daily Attendance Reminder',
            f'Hello {student.name}, please mark your attendance for today.',
            'from@example.com',
            [student.email],
            fail_silently=False,
        )

    @patch('notifications.tasks.send_mail')
    def test_send_grade_update_notification(self, mock_send_mail):
        # Create a student and a grade
        student = Student.objects.create(
            username='testuser',
            email='test@student.com',
            password='password'
        )
        grade = Grade.objects.create(
            student=student,
            score=90,
            course='Test Course'
        )

        # Call the Celery task
        send_grade_update_notification(grade.id)

        # Check if the email was sent
        mock_send_mail.assert_called_with(
            'Grade Update Notification',
            f'Hello {student.name}, your grade for Test Course has been updated.',
            'from@example.com',
            [student.email],
            fail_silently=False,
        )

from django.test import TestCase
from unittest.mock import patch
from notifications.tasks import send_attendance_reminder, send_grade_update_notification, send_weekly_performance_update
from students.models import Student
from grades.models import Grade
from django.conf import settings

class NotificationsTests(TestCase):

    def setUp(self):
        self.student = Student.objects.create(
            username='testuser',
            email='test@student.com',
            password='password'
        )

    @patch('notifications.tasks.send_mail')
    def test_send_attendance_reminder(self, mock_send_mail):
        send_attendance_reminder()

        mock_send_mail.assert_called_once_with(
            'Daily Attendance Reminder',
            f'Hello {self.student.username}, please mark your attendance for today.',
            settings.DEFAULT_FROM_EMAIL,
            [self.student.email],
            fail_silently=False,
        )

    @patch('notifications.tasks.send_mail')
    def test_send_grade_update_notification(self, mock_send_mail):
        grade = Grade.objects.create(
            student=self.student,
            score=90,
            course='Test Course'
        )

        send_grade_update_notification(grade.id)
        mock_send_mail.assert_called_once_with(
            'Grade Update Notification',
            f'Hello {self.student.username}, your grade for Test Course has been updated.',
            settings.DEFAULT_FROM_EMAIL,
            [self.student.email],
            fail_silently=False,
        )

    @patch('notifications.tasks.send_mail')
    def test_send_weekly_performance_update(self, mock_send_mail):
        send_weekly_performance_update()


        mock_send_mail.assert_called_with(
            'Weekly Performance Summary',
            f'Hello {self.student.username},\n\nHere is your weekly performance summary:\n\n'
            f'Attendance: 0 days\n'
            f'Average Grade: 0.00\n',
            settings.DEFAULT_FROM_EMAIL,
            [self.student.email],
            fail_silently=False,
        )

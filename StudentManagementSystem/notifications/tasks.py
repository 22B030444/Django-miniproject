# notifications/tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Avg
from django.conf import settings
from students.models import Student
from attendance.models import Attendance
from grades.models import Grade
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_attendance_reminder():
    """
    Sends a reminder to all students to mark their attendance.
    This task will be triggered daily.
    """
    students = Student.objects.all()
    for student in students:
        if student.email:  # Проверяем, есть ли у студента email
            try:
                send_mail(
                    'Daily Attendance Reminder',
                    f'Hello {student.name}, please mark your attendance for today.',
                    settings.DEFAULT_FROM_EMAIL,  # Используйте настройку отправителя
                    [student.email],
                    fail_silently=False,
                )
            except Exception as e:
                logger.error(f"Failed to send attendance reminder to {student.email}: {e}")

@shared_task
def send_grade_update_notification(grade_id):
    """
    Sends an email notification to a student when their grade is updated.
    """
    try:
        grade = Grade.objects.get(id=grade_id)
        student = grade.student  # Предполагается, что в Grade есть связь с Student
        if student.email:  # Проверяем, есть ли у студента email
            send_mail(
                'Grade Update Notification',
                f'Hello {student.name}, your grade for {grade.course.name} has been updated.',
                settings.DEFAULT_FROM_EMAIL,  # Используйте настройку отправителя
                [student.email],
                fail_silently=False,
            )
    except Grade.DoesNotExist:
        logger.warning(f"Grade with id {grade_id} does not exist.")
    except Exception as e:
        logger.error(f"Failed to send grade update notification to {student.email}: {e}")

@shared_task
def send_weekly_performance_update():
    """
    Sends a weekly performance update to all students.
    """
    students = Student.objects.all()
    for student in students:
        if student.email:  # Проверяем, есть ли у студента email
            attendance_count = Attendance.objects.filter(student=student).count()
            grades = Grade.objects.filter(student=student).aggregate(avg_grade=Avg('score'))
            avg_grade = grades['avg_grade'] if grades['avg_grade'] is not None else 0  # Обработка случая, когда оценок нет

            try:
                send_mail(
                    'Weekly Performance Summary',
                    f'Hello {student.name},\n\nHere is your weekly performance summary:\n\n'
                    f'Attendance: {attendance_count} days\n'
                    f'Average Grade: {avg_grade:.2f}\n',
                    settings.DEFAULT_FROM_EMAIL,  # Используйте настройку отправителя
                    [student.email],
                    fail_silently=False,
                )
            except Exception as e:
                logger.error(f"Failed to send weekly performance update to {student.email}: {e}")
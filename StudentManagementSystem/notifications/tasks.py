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
    """
    students = Student.objects.all().select_related('profile')  # Предварительная загрузка данных
    for student in students:
        if student.email:
            try:
                send_mail(
                    'Daily Attendance Reminder',
                    f'Hello {student.username}, please mark your attendance for today.',
                    settings.DEFAULT_FROM_EMAIL,
                    [student.email],
                    fail_silently=False,
                )
                logger.info(f"Attendance reminder sent to {student.email}")
            except Exception as e:
                logger.error(f"Failed to send attendance reminder to {student.email}: {e}")


@shared_task
def send_grade_update_notification(grade_id):
    """
    Sends an email notification to a student when their grade is updated.
    """
    try:
        grade = Grade.objects.select_related('student', 'course').get(id=grade_id)
        student = grade.student
        if student.email:
            send_mail(
                'Grade Update Notification',
                f'Hello {student.username}, your grade for {grade.course.name} has been updated.',
                settings.DEFAULT_FROM_EMAIL,
                [student.email],
                fail_silently=False,
            )
            logger.info(f"Grade update notification sent to {student.email}")
    except Grade.DoesNotExist:
        logger.warning(f"Grade with id {grade_id} does not exist.")
    except Exception as e:
        logger.error(f"Failed to send grade update notification: {e}")


@shared_task
def send_weekly_performance_update():
    """
    Sends a weekly performance update to all students.
    """
    students = Student.objects.all().prefetch_related('attendance_set', 'grade_set')
    for student in students:
        if student.email:
            attendance_count = Attendance.objects.filter(student=student).count()
            grades = Grade.objects.filter(student=student).aggregate(avg_grade=Avg('score'))
            avg_grade = grades['avg_grade'] or 0

            try:
                send_mail(
                    'Weekly Performance Summary',
                    f'Hello {student.username},\n\nHere is your weekly performance summary:\n\n'
                    f'Attendance: {attendance_count} days\n'
                    f'Average Grade: {avg_grade:.2f}\n',
                    settings.DEFAULT_FROM_EMAIL,
                    [student.email],
                    fail_silently=False,
                )
                logger.info(f"Weekly performance update sent to {student.email}")
            except Exception as e:
                logger.error(f"Failed to send weekly performance update to {student.email}: {e}")

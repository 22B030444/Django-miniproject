# notifications/tasks.py

from celery import shared_task
from django.core.mail import send_mail
from students.models import Student
from attendance.models import Attendance
from grades.models import Grade


@shared_task
def send_attendance_reminder():
    """
    Sends a reminder to all students to mark their attendance.
    This task will be triggered daily.
    """
    students = Student.objects.all()
    for student in students:
        # Send email reminder (you could include more details here)
        send_mail(
            'Daily Attendance Reminder',
            f'Hello {student.name}, please mark your attendance for today.',
            'from@example.com',
            [student.email],
            fail_silently=False,
        )


@shared_task
def send_grade_update_notification(grade_id):
    """
    Sends an email notification to a student when their grade is updated.
    """
    try:
        grade = Grade.objects.get(id=grade_id)
        student = grade.student  # Assuming Grade model has a 'student' foreign key
        send_mail(
            'Grade Update Notification',
            f'Hello {student.name}, your grade for {grade.course.name} has been updated.',
            'from@example.com',
            [student.email],
            fail_silently=False,
        )
    except Grade.DoesNotExist:
        pass


@shared_task
def send_weekly_performance_update():
    """
    Sends a weekly performance update to all students.
    """
    students = Student.objects.all()
    for student in students:
        # Generate performance summary, e.g. attendance, grades, etc.
        attendance_count = Attendance.objects.filter(student=student).count()
        grades = Grade.objects.filter(student=student)
        avg_grade = grades.aggregate(models.Avg('score'))['score__avg']

        # Send the summary email
        send_mail(
            'Weekly Performance Summary',
            f'Hello {student.name},\n\nHere is your weekly performance summary:\n\n'
            f'Attendance: {attendance_count} days\n'
            f'Average Grade: {avg_grade:.2f}\n',
            'from@example.com',
            [student.email],
            fail_silently=False,
        )

# students/tasks.py

from celery import shared_task
from django.core.mail import send_mail
from students.models import Student

@shared_task
def send_student_welcome_email(student_id):
    try:
        student = Student.objects.get(id=student_id)
        send_mail(
            'Welcome to our platform!',
            f'Hello {student.name}, welcome!',
            'from@example.com',
            [student.email],
            fail_silently=False,
        )
    except Student.DoesNotExist:
        return f"Student with ID {student_id} does not exist."

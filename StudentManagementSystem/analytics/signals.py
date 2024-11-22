# analytics/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from courses.models import Enrollment
from analytics.models import CoursePopularity

@receiver(post_save, sender=Enrollment)
def update_course_popularity(sender, instance, created, **kwargs):
    if created:
        course_popularity, _ = CoursePopularity.objects.get_or_create(course=instance.course)
        course_popularity.enrollments += 1
        course_popularity.save()

import logging

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Attendance
from .serializers import AttendanceSerializer

# Set up logger for attendance app
logger = logging.getLogger('attendance')

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser()]  # Only Admins can mark/update attendance
        return [IsAuthenticated()]  # Everyone can view attendance

    def perform_create(self, serializer):
        # Get the student, course, and status from the validated data
        student = serializer.validated_data['student']
        course = serializer.validated_data['course']
        status = serializer.validated_data['status']

        # Log the attendance marking action
        logger.info(f"Attendance marked for student {student.username} in course {course.name}, status: {status}")

        # Perform the actual create action (save to the database)
        super().perform_create(serializer)
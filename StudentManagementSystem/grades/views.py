
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import logging
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Grade
from .serializers import GradeSerializer
from attendance.models import Attendance
from attendance.serializers import AttendanceSerializer
from courses.models import Enrollment
from courses.serializers import EnrollmentSerializer
from users.permissions import IsTeacher

logger = logging.getLogger('grades')

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated,IsTeacher]

    def perform_create(self, serializer):
        student = serializer.validated_data['student']
        course = serializer.validated_data['course']
        grade = serializer.validated_data['grade']
        logger.info(f"Grade updated for student {student.username} in course {course.name}, grade: {grade}")
        super().perform_create(serializer)
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser()]  # Only Admins can add/edit grades
        return [IsAuthenticated()]  # Everyone can view grades


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsTeacher]  # Only teachers can manage attendance



class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsTeacher]  # Only teachers can enroll students

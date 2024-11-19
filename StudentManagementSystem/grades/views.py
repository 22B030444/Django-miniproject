# grades/views.py

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
    permission_classes = [IsAuthenticated, IsTeacher]  # Teachers can manage grades

    def perform_create(self, serializer):
        # Получаем данные из сериализатора
        student = serializer.validated_data['student']
        course = serializer.validated_data['course']
        grade_value = serializer.validated_data.get('grade_value')
        grade_letter = serializer.validated_data.get('grade_letter')

        # Логируем информацию о создании оценки
        logger.info(f"Grade created for student {student.username} in course {course.name}, "
                    f"grade value: {grade_value}, grade letter: {grade_letter}")

        # Вызываем метод для создания записи
        super().perform_create(serializer)

    def get_permissions(self):
        # Настройка разрешений в зависимости от действия
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser(), IsTeacher()]  # Только администраторы могут добавлять/редактировать оценки
        return super().get_permissions()  # Остальные действия для всех аутентифицированных пользователей

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsTeacher]  # Только учителя могут управлять посещаемостью

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsTeacher]  # Только учителя могут записывать студентов
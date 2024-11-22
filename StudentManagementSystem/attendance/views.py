# attendance/views.py

import logging
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from users.permissions import IsTeacher
from .models import Attendance
from .serializers import AttendanceSerializer

# Настройка логгера для приложения посещаемости
logger = logging.getLogger('attendance')


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Устанавливает разрешения в зависимости от действия.
        """
        if self.action in ['create', 'update', 'destroy']:
            return [IsTeacher()]  # Только администраторы могут создавать/обновлять/удалять посещаемость
        return super().get_permissions()  # Все могут просматривать посещаемость

    def perform_create(self, serializer):
        """
        Логирует создание записи о посещаемости и сохраняет её в базе данных.
        """
        student = serializer.validated_data['student']
        course = serializer.validated_data['course']
        status = serializer.validated_data['status']

        # Логируем действие о регистрации посещаемости
        logger.info(f"Attendance marked for student {student.id} in course {course.id}, status: {status}")

        # Сохраняем запись о посещаемости
        super().perform_create(serializer)

    def perform_update(self, serializer):
        """
        Логирует обновление записи о посещаемости и сохраняет изменения в базе данных.
        """
        attendance_instance = self.get_object()
        logger.info(
            f"Attendance updated for student {attendance_instance.student.id} in course {attendance_instance.course.id}, new status: {serializer.validated_data['status']}")

        super().perform_update(serializer)

    def perform_destroy(self, instance):
        """
        Логирует удаление записи о посещаемости и удаляет её из базы данных.
        """
        logger.info(f"Attendance deleted for student {instance.student.id} in course {instance.course.id}")
        super().perform_destroy(instance)
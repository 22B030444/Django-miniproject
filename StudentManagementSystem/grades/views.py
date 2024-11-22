import logging
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .models import Grade
from .serializers import GradeSerializer
from attendance.models import Attendance
from attendance.serializers import AttendanceSerializer
from courses.models import Enrollment
from users.permissions import IsTeacher
from django.shortcuts import get_object_or_404

# Настройка логирования
logger = logging.getLogger('grades')


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        """
        Перегружаем метод создания для логирования и проверки существования данных.
        """
        student = serializer.validated_data['student']
        course = serializer.validated_data['course']
        grade_value = serializer.validated_data.get('grade_value')
        grade_letter = serializer.validated_data.get('grade_letter')

        logger.info(f"Trying to create grade for student {student.id} in course {course.id}")

        # Проверяем, что студент и курс существуют
        get_object_or_404(Enrollment, student=student, course=course)  # Проверка связи студента и курса
        get_object_or_404(Attendance, student=student, course=course)  # Проверка присутствия на занятиях

        logger.info(f"Grade created for student {student.id} in course {course.id}, "
                    f"grade value: {grade_value}, grade letter: {grade_letter}")

        super().perform_create(serializer)

    def get_permissions(self):
        """
        Настройка разрешений в зависимости от действия.
        """
        if self.action in ['create', 'update', 'destroy']:
            return [IsTeacher()]  # Только учителя могут добавлять/редактировать/удалять оценки
        return super().get_permissions()  # Остальные действия доступны для всех аутентифицированных пользователей

    def list(self, request, *args, **kwargs):
        """
        Перегружаем метод list для фильтрации оценок по студентам (для администраторов и учителей).
        """
        if request.user.is_teacher or request.user.is_staff:
            return super().list(request, *args, **kwargs)
        # Студенты могут просматривать только свои оценки
        grades = Grade.objects.filter(student=request.user.student)  # Предполагаем, что у пользователя есть объект Student
        serializer = self.get_serializer(grades, many=True)
        return Response(serializer.data)

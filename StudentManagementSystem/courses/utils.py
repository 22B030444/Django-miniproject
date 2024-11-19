# courses/utils.py

import logging
from django.core.cache import cache
from .models import Course  # Импортируем модель Course
from .serializers import CourseSerializer  # Импортируем сериализатор

logger = logging.getLogger('cache')


def get_course_list():
    """
    Получает список курсов, используя кэш для оптимизации.
    Если данные есть в кэше, они возвращаются оттуда.
    В противном случае данные извлекаются из базы данных и кэшируются.
    """
    cache_key = 'course_list'
    cached_data = cache.get(cache_key)

    if cached_data:
        logger.debug(f"Cache hit for {cache_key}")
        return cached_data  # Возвращаем кэшированные данные

    logger.debug(f"Cache miss for {cache_key}")

    # Извлекаем данные из базы данных
    courses = Course.objects.all()  # Получаем все курсы
    serialized_courses = CourseSerializer(courses, many=True).data  # Сериализуем курсы

    # Сохраняем данные в кэш на 5 минут
    cache.set(cache_key, serialized_courses, timeout=300)

    return serialized_courses
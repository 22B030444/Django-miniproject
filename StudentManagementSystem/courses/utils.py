# courses/utils.py
import logging
from django.core.cache import cache

logger = logging.getLogger('cache')


def get_course_list():
    cache_key = 'course_list'
    cached_data = cache.get(cache_key)
    if cached_data:
        logger.debug(f"Cache hit for {cache_key}")
    else:
        logger.debug(f"Cache miss for {cache_key}")
        # Retrieve data from DB and cache it
        # Example, you would query the database for courses
        # cached_data = Course.objects.all()
        cached_data = "some data"  # This would be the actual course data
        cache.set(cache_key, cached_data, timeout=300)

    return cached_data

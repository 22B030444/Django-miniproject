# your_project/utils.py

from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    """
    Функция для создания JWT токенов для пользователя.
    Добавляет роль пользователя в токен.
    """
    refresh = RefreshToken.for_user(user)
    refresh['role'] = user.role  # Добавляем роль в токен
    return str(refresh.access_token)  # Возвращаем только access token

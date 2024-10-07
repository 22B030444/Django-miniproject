# users_app/urls.py
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import (
    UserRegistration,
    UserProfileView,
    EditUserProfile,
    FollowUser,
    UnfollowUser, MainPage
)

urlpatterns = [
    path('', MainPage.as_view(), name='main-page'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('register/', UserRegistration.as_view(), name='user-register'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='user-profile'),
    path('profile/<int:user_id>/edit/', EditUserProfile.as_view(), name='user-profile-edit'),
    path('follow/<int:user_id>/', FollowUser.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUser.as_view(), name='unfollow-user'),

]

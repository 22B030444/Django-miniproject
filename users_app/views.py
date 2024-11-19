from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import TemplateView
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from .models import Follow, Profile
from .serializers import UserSerializer, ProfileSerializer
from django.contrib.auth.views import LoginView, LogoutView

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'users/logout.html'


class MainPage(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_id'] = self.request.user.id if self.request.user.is_authenticated else None
        return context


class UserRegistration(APIView):
    def get(self, request, format=None):
        form = UserRegisterForm()
        return render(request, 'users/registration.html', {'form': form})

    def post(self, request, format=None):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the users after registration
            return redirect('post-list')  # Redirect to the post list after successful registration
        return render(request, 'users/registration.html', {'form': form})

class UserProfileView(View):
    def get(self, request, user_id, format=None):
        user = get_object_or_404(User, id=user_id)
        posts = user.post_set.all()

        # Получаем пользователей, которые следуют за данным пользователем
        followers = [follow.follower for follow in user.followers.all()]
        following = [follow.following for follow in user.following.all()]
        # Проверяем, подписан ли текущий пользователь на профиль
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()

        return render(request, 'users/profile.html', {
            'users': user,
            'posts': posts,
            'followers': followers,  # Передаем список пользователей
            'following': following,  # Передаем список подписок
            'is_following': is_following,
        })

class EditUserProfile(APIView):
    def get(self, request, user_id, format=None):
        user = get_object_or_404(User, id=user_id)
        return render(request, 'users/profile.html', {
            'users': user,
            'is_following': request.user.following.filter(id=user.id).exists(),
        })

    def post(self, request, user_id, format=None):
        user = get_object_or_404(User, id=user_id)
        if request.user != user:
            return redirect('users-profile', user_id=user_id)

        # Обновление профиля пользователя
        bio = request.POST.get('bio')
        profile_picture = request.FILES.get('profile_picture')

        # Проверка, существует ли профиль
        if hasattr(user, 'profile'):
            user.profile.bio = bio
            if profile_picture:
                user.profile.profile_picture = profile_picture
            user.profile.save()
        else:
            # Создаем профиль, если его нет
            Profile.objects.create(user=user, bio=bio, profile_picture=profile_picture)

        return redirect('users-profile', user_id=user_id)

class FollowUser(APIView):
    def post(self, request, user_id, format=None):
        user_to_follow = get_object_or_404(User, id=user_id)
        follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
        if created:
            # Redirect back to the users's profile with a success message
            return redirect('users-profile', user_id=user_id)  # Use the appropriate URL name
        return redirect('users-profile', user_id=user_id)
class UnfollowUser(APIView):
    def post(self, request, user_id, format=None):
        user_to_unfollow = get_object_or_404(User, id=user_id)
        follow = Follow.objects.filter(follower=request.user, following=user_to_unfollow).first()

        # Render the profile template with a success message
        if follow:
            follow.delete()
            message = f"You have unfollowed {user_to_unfollow.username}"
        else:
            message = "You are not following this users"

        return render(request, 'users/profile.html', {
            'users': user_to_unfollow,
            'message': message,
            'user_to_follow': user_to_unfollow,  # Pass the users being unfollowed
        })
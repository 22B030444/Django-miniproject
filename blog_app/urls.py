# blog_app/urls.py

from django.urls import path
from .views import (
    PostList,
    PostDetail,
    PostCreate,
    PostEdit,
    PostDelete,
    PostComments,
    AddComment,
    MainPage,
)

urlpatterns = [
    path('', MainPage.as_view(), name='main-page'),
    path('posts/', PostList.as_view(), name='post-list'),
    path('posts/<int:post_id>/', PostDetail.as_view(), name='post-detail'),
    path('posts/create/', PostCreate.as_view(), name='post-create'),
    path('posts/<int:post_id>/edit/', PostEdit.as_view(), name='post-edit'),
    path('posts/<int:post_id>/delete/', PostDelete.as_view(), name='post-delete'),
    path('posts/<int:post_id>/comments/', PostComments.as_view(), name='post-comments'),
    path('posts/<int:post_id>/comments/add/', AddComment.as_view(), name='add-comment'),
]

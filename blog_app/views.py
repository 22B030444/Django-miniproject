from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.views.generic import TemplateView
from .models import Comment, Post
from .serializers import CommentSerializer, PostSerializer
from .forms import PostForm, CommentForm

class MainPage(TemplateView):
    template_name = 'main.html'


class PostList(APIView):
    def get(self, request, format=None):
        posts = Post.objects.all()  # Get all posts
        return render(request, 'blog/post_list.html', {'posts': posts})


class PostDetail(APIView):
    def get(self, request, post_id, format=None):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        comments = post.comments.all()  # Retrieve all comments related to this post
        comment_form = CommentForm()  # Initialize an empty comment form

        # Render the template and pass the post, serialized data, comments, and form
        return render(request, 'blog/post_detail.html', {
            'post': post,
            'post_data': serializer.data,
            'comments': comments,
            'comment_form': comment_form,
        })

    def post(self, request, post_id, format=None):
        post = get_object_or_404(Post, id=post_id)
        comments = post.comments.all()  # Retrieve comments for display
        serializer = PostSerializer(post)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user  # Assuming the users is logged in
            new_comment.save()
            return redirect('post-detail', post_id=post.id)  # Redirect to the same page after posting

        # If the form is invalid, render the same page with errors
        return render(request, 'blog/post_detail.html', {
            'post': post,
            'post_data': serializer.data,
            'comments': comments,
            'comment_form': comment_form,
        })

class PostCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        form = PostForm()
        return render(request, 'blog/post_form.html', {'form': form})

    def post(self, request, format=None):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the author dynamically
            post.save()
            return redirect('post-detail', post_id=post.id)  # Redirect to post detail page
        return render(request, 'blog/post_form.html', {'form': form})


class PostEdit(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id, format=None):
        post = get_object_or_404(Post, id=post_id)
        form = PostForm(instance=post)
        return render(request, 'blog/post_form.html', {
            'form': form,
            'is_edit': True,  # Indicate that this is an edit action
            'post': post  # Pass the post object for further context if needed
        })

    def post(self, request, post_id, format=None):
        post = get_object_or_404(Post, id=post_id)
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect('post-detail', post_id=post.id)

        # Render the form again with error messages if the form is invalid
        return render(request, 'blog/post_form.html', {
            'form': form,
            'is_edit': True,  # Maintain the edit state
            'post': post  # Pass the post object for further context if needed
        })
class PostDelete(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id, format=None):
        post = get_object_or_404(Post, id=post_id)
        if post.author != request.user:
            return Response({"detail": "You do not have permission to delete this post."},
                            status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return redirect('post-list')

class PostComments(APIView):
    def get(self, request, post_id, format=None):
        post = get_object_or_404(Post, id=post_id)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddComment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id, format=None):
        post = get_object_or_404(Post, id=post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)  # Set the author dynamically
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

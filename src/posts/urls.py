from django.urls import path

from .views import (
    PostDetailView,
    AllPostsView,
    CreatePostView,
    ReviewPostsView,
    approve_post,
    delete_post,
    ReviewPostView,
    EditPostView,
    like_post,
    bookmark_post,
    author_posts_view,
    TagPostsView,
    filtered_posts_view
)

urlpatterns = [
    path(
        'post/<int:pk>/<slug:slug>/',
        PostDetailView.as_view(), name='post_detail'),
    path(
        'all/', AllPostsView.as_view(), name='all_posts'),
    path(
        'create/', CreatePostView.as_view(), name='create_post'),
    path(
        'review_posts/', ReviewPostsView.as_view(), name='review_posts'),
    path(
        'review_post/<int:pk>/<slug:slug>/',
        ReviewPostView.as_view(), name='review_post'),
    path(
        'approve/<int:pk>/<slug:slug>/', approve_post, name='approve_post'),
    path(
        'delete/<int:pk>/', delete_post, name='delete_post'),
    path(
        'edit/<int:pk>/<slug:slug>/',
        EditPostView.as_view(), name='edit_post'),
    path(
        'like/<int:pk>/', like_post, name="like_post"),
    path(
        'bookmark/<int:pk>/', bookmark_post, name="bookmark_post"),
    path(
        'author/<int:pk>/',
        author_posts_view, name="posts_by_author"),
    path(
        'tag/<int:pk>/', TagPostsView.as_view(), name="posts_by_tag"),
    path('filtered/', filtered_posts_view, name="filtered_posts")
]

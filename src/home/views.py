from django.db.models import Count
from django.shortcuts import render
from posts.models import Post


def home_view(request):
    """
    Render home page with 4 most recent posts and 4 most popular posts
    """
    recent_posts = Post.objects.filter(
        status="Published").order_by('-created_on')[:4]
    favourite_posts = Post.objects.filter(
        status="Published"
    ).annotate(
        like_count=Count('likes')).order_by('-like_count')[:4]

    context = {
        'recent_posts': recent_posts,
        'favourite_posts': favourite_posts
    }

    return render(request, 'home/index.html', context)

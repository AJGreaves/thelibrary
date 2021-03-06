from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres import search
from django.contrib.postgres.search import (
    SearchVector, SearchQuery, SearchRank)
from django.db.models import Q
from django.views.generic import ListView

from posts.models import Post


class SearchResultsView(ListView):
    """ Render search results with pagination """
    template_name = "search/search_results.html"
    paginate_by = 12
    context_object_name = 'posts'

    def get_queryset(self):
        """
        Checks if keywords specifying the course is in search query.
        If True, strips these keywords out of the query and filters
        results for course specified.

        Uses search vectors from Post model fields:
        title, summary, body, category and tags.
        Ranks them in this order with title being most important
        and category/tags least important.
        """

        q = self.request.GET.get('q')

        # For this code, I followed this tutorial from
        # https://testdriven.io/blog/django-search/

        if not any(course in q.lower() for course in ['4p', '5p']):
            q = q.lower().replace('4p', '').replace('5p', '')
            search_vector = SearchVector(
                "title", weight="A"
            ) + SearchVector(
                "summary", weight="B"
            ) + SearchVector(
                "body", weight="C"
            )
            search_query = SearchQuery(q)
            queryset = Post.objects.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(
                search=search_query,
                status="Published"
            ).order_by("-rank")

        else:
            course = '1' if '4p' in q.lower() else '2'
            q = q.lower().replace('4p', '').replace('5p', '')

            search_vector = SearchVector(
                "title", weight="A"
            ) + SearchVector(
                "summary", weight="B"
            ) + SearchVector(
                "body", weight="C"
            )
            search_query = SearchQuery(q)
            queryset = Post.objects.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(
                search=search_query,
                status="Published",
                course=course
            ).order_by("-rank")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context

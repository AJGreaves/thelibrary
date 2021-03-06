import re
from slugify import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from courses.models import Course
from users.models import User, UserProfile
from .forms import FlagForm, AddOrEditPostForm
from .models import Post, PostFlag, PostTag, Bookmark


class AllPostsView(ListView):
    """ Basic view to see all posts, ordered by most recently created first """
    template_name = 'posts_listview.html'
    paginate_by = 12
    queryset = Post.objects.filter(status='Published').order_by('-created_on')

    def get_context_data(self, *args, **kwargs):

        context = super(
            AllPostsView, self).get_context_data(**kwargs)
        context['pg_title'] = 'All Posts'
        context['courses'] = Course.objects.all()

        return context


def filtered_posts_view(request, *args, **kwargs):
    """
    View to handle filtering all posts by category and sort method.
    Results paginated by 12 items. Default category "all", sort method
    by most recently created first and default course selection set to "all.
    Users can sort by single categories,
    newest, oldest or most liked.
    """
    category_pk = request.GET.get('category', 'all')
    sort_method = request.GET.get('sort_method', '-created_on')
    course_selection = request.GET.get('course_selection', 'all')

    if course_selection == '3':
        course_selection = 'all'

    if sort_method == 'likes':
        if category_pk == 'all':
            if course_selection == 'all':
                sorted_posts = Post.objects.filter(
                    status="Published").annotate(
                        like_count=Count('likes')
                    ).order_by('-like_count')
            else:
                sorted_posts = Post.objects.filter(
                    status="Published", course=course_selection
                ).annotate(
                    like_count=Count('likes')
                ).order_by('-like_count')
        else:
            if course_selection == 'all':
                sorted_posts = Post.objects.filter(
                    category=category_pk,
                    status="Published",
                ).annotate(
                    like_count=Count('likes')
                ).order_by('-like_count')
            else:
                sorted_posts = Post.objects.filter(
                    category=category_pk,
                    course=course_selection,
                    status="Published",
                ).annotate(
                    like_count=Count('likes')
                ).order_by('-like_count')

    elif category_pk == 'all':
        if course_selection == 'all':
            sorted_posts = Post.objects.filter(
                status="Published").order_by(sort_method)
        else:
            sorted_posts = Post.objects.filter(
                status="Published",
                course=course_selection
            ).order_by(sort_method)
    else:
        if course_selection == 'all':
            sorted_posts = Post.objects.filter(
                category=category_pk, status="Published"
            ).order_by(sort_method)
        else:
            sorted_posts = Post.objects.filter(
                category=category_pk,
                course=course_selection,
                status="Published"
            ).order_by(sort_method)

    # Code for pagination with function based views from
    # https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html
    page = request.GET.get('page', 1)
    paginator = Paginator(sorted_posts, 12)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    courses = Course.objects.all()

    context = {
        'page_obj': page_obj,
        'category_pk': category_pk,
        'sort_method': sort_method,
        'course_selection': course_selection,
        'courses': courses,
    }
    return render(request, 'posts_listview.html', context)


def author_posts_view(request, pk, *args, **kwargs):
    """
    Renders author posts page. Sets defaults on first loading the page
    to show all of the authors posts, with their most recent first.
    When a GET request is made, the results are filtered by category
    and sort method.
    """
    category_pk = request.GET.get('category', 'all')
    sort_method = request.GET.get('sort_method', '-created_on')
    course_selection = request.GET.get('course_selection', 'all')

    if course_selection == '3':
        course_selection = 'all'

    if sort_method == 'likes':
        if category_pk == 'all':
            if course_selection == 'all':
                sorted_posts = Post.objects.filter(
                    author=pk,
                    status="Published").annotate(
                        like_count=Count('likes')
                    ).order_by('-like_count')
            else:
                sorted_posts = Post.objects.filter(
                    author=pk,
                    status="Published",
                    course=course_selection
                ).annotate(
                    like_count=Count('likes')
                ).order_by('-like_count')
        else:
            if course_selection == 'all':
                sorted_posts = Post.objects.filter(
                    author=pk,
                    category=category_pk,
                    status="Published",
                ).annotate(
                    like_count=Count('likes')
                ).order_by('-like_count')
            else:
                sorted_posts = Post.objects.filter(
                    author=pk,
                    category=category_pk,
                    course=course_selection,
                    status="Published",
                ).annotate(
                    like_count=Count('likes')
                ).order_by('-like_count')

    elif category_pk == 'all':
        if course_selection == 'all':
            sorted_posts = Post.objects.filter(
                author=pk,
                status="Published").order_by(sort_method)
        else:
            sorted_posts = Post.objects.filter(
                author=pk,
                status="Published",
                course=course_selection
            ).order_by(sort_method)
    else:
        if course_selection == 'all':
            sorted_posts = Post.objects.filter(
                author=pk,
                category=category_pk, status="Published"
            ).order_by(sort_method)
        else:
            sorted_posts = Post.objects.filter(
                author=pk,
                category=category_pk,
                course=course_selection,
                status="Published"
            ).order_by(sort_method)

    # Build pagination object (see code credit above)
    page = request.GET.get('page', 1)
    paginator = Paginator(sorted_posts, 12)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    courses = Course.objects.all()

    userprofile = get_object_or_404(UserProfile, pk=pk)
    context = {
        'page_obj': page_obj,
        'category_pk': category_pk,
        'sort_method': sort_method,
        'pg_title': f"Posts by {userprofile.user.username}",
        'extra_filter': 'author',
        'author_pk': pk,
        'course_selection': course_selection,
        'courses': courses,
    }
    return render(request, 'posts_listview.html', context)


class PostDetailView(DetailView, SuccessMessageMixin):
    """
    Create view for single post detail page. Shows the post information, and
    displays details about the author from their profile. Also loads the flag
    form which is displayed in a modal, for users who wish to flag the post for
    innappropriate or outdated content.
    """
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    success_message = "Thank you for flagging this post,\
        an admin will review it shortly"

    def get_context_data(self, *args, **kwargs):
        context = super(
            PostDetailView, self).get_context_data(**kwargs)
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        context['total_likes'] = post.total_likes()
        context['liked'] = post.likes.filter(
            id=self.request.user.id).exists()
        context['kudos_badge'] = post.author.kudos_badge()
        context['author_name'] = post.author.get_author_name()
        context['form'] = FlagForm()

        # Regex code solution for capturing only the hosted
        # Youtube video ID written by Sean Murphy, taken from
        # project by JimLynx https://github.com/JimLynx/Channel-Lead-Resources
        if post.youtube is not None:
            context['youtube_id'] = ''.join(re.findall(
                '(?<=v=)(.{11})', post.youtube))

        if self.request.user.is_authenticated:
            context['bookmarked'] = Bookmark.objects.filter(
                post=self.kwargs['pk'],
                user=self.request.user).exists()

        # Get related posts
        context['related_posts'] = Post.objects.filter(
            status="Published", category=post.category
        ).exclude(pk=post.pk).annotate(
            like_count=Count('likes')).order_by('-like_count')[:4]

        return context

    def post(self, request, *args, **kwargs):
        """ Handles submission of the FlagForm """
        form = FlagForm(request.POST)
        if form.is_valid():
            post = get_object_or_404(Post, id=self.kwargs['pk'])

            # If older flag exists on the post, delete it before attaching
            # a new one. Saves database from being populated with duplicates
            if post.flag:
                post.flag.delete()

            # Add flagger details to PostFlag instance
            form.instance.flagger = get_object_or_404(
                User, pk=self.request.user.pk
            )
            form.save()

            # Attach PostFlag instance to relevant Post
            post.flag = get_object_or_404(PostFlag, pk=form.instance.pk)
            post.save()

            # Create context, set success message and render
            self.object = self.get_object()
            context = super(PostDetailView, self).get_context_data(**kwargs)
            context['form'] = FlagForm
            messages.success(self.request, self.success_message)
            return self.render_to_response(context=context)

        else:
            self.object = self.get_object()
            context = super(PostDetailView, self).get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context=context)

    def get_success_url(self):
        return reverse(
            'detail_view',
            kwargs={
                'pk': self.object.pk,
                'slug': self.object.slug})


class CreatePostView(LoginRequiredMixin, CreateView):
    """ Renders view to create a new post """
    model = Post
    template_name = 'create_post.html'
    form_class = AddOrEditPostForm

    def form_valid(self, form):
        form.instance.author = self.request.user.userprofile
        form.instance.slug = slugify(form.instance.title)

        # CI Staff posts immediately published, no review process.
        if self.request.user.userprofile.is_staff:
            form.instance.status = "Published"

        # Code to solve saving m2m instances issue kindly provided by
        # Willem Van Onsem on Stack Overflow:
        # https://stackoverflow.com/questions/67391651/saving-instances-of-model-to-manytomany-field-thows-attributeerror-post-object
        post = form.save()

        new_tags = self.request.POST.get('new_tags')
        tags_list = new_tags.split()

        for new_tag in tags_list:
            post.tags.add(PostTag.objects.get_or_create(name=new_tag)[0])

        return HttpResponseRedirect(self.get_success_url(post))

    def get_success_url(self, post):
        if self.request.user.userprofile.is_staff:
            messages.add_message(
                self.request, messages.SUCCESS, "Post successfully published")
            return reverse(
                'post_detail', kwargs={'pk': post.pk, 'slug': post.slug})
        else:
            return reverse(
                'review_post', kwargs={'pk': post.pk, 'slug': post.slug})


class EditPostView(LoginRequiredMixin, UpdateView):
    """ Renders view to edit an existing post """
    model = Post
    template_name = 'edit_post.html'
    context_object_name = 'post'
    form_class = AddOrEditPostForm

    def form_valid(self, form):
        if form.instance.status == 'Review':
            form.instance.status = 'Submitted'

        form.instance.updated_on = timezone.now()
        form.instance.mod_message = ''

        post = form.save()

        new_tags = self.request.POST.get('new_tags')
        tags_list = new_tags.split()

        for new_tag in tags_list:
            post.tags.add(PostTag.objects.get_or_create(name=new_tag)[0])

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.object.status == 'Submitted':
            return reverse(
                    'review_post',
                    kwargs={'pk': self.object.pk, 'slug': self.object.slug})
        else:
            return reverse(
                    'post_detail',
                    kwargs={'pk': self.object.pk, 'slug': self.object.slug})


class ReviewPostsView(LoginRequiredMixin, ListView):
    """
    Renders view for moderators to review submitted posts. If non-mod
    tries to access this view, they are reidrected to the home page.
    """
    template_name = 'review_posts.html'
    paginate_by = 24

    def get_queryset(self, *args, **kwargs):
        # Get all submitted posts, excluding ones by the author
        queryset = Post.objects.filter(
            status='Submitted'
        ).exclude(
            author=self.request.user.userprofile).order_by('-created_on')
        return queryset

    def get(self, *args, **kwargs):
        user = self.request.user
        if user.userprofile.is_mod is not True:
            return redirect('home')
        return super(ReviewPostsView, self).get(*args, **kwargs)


@login_required
def approve_post(request, pk, slug):
    """
    Checks if user approving the post is a moderator and is not the author of
    the post, if this is True the post is set to published. Otherwise the user
    is redirected to the home page.
    """
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user and request.user.userprofile.is_mod:
        post.status = 'Published'
        post.created_on = timezone.now()
        post.save()
        return redirect('review_posts')
    else:
        return redirect('home')


@login_required
def delete_post(request, pk):
    """
    Check if author of post is the logged in user.
    If so, delete the selected post. If not, redirect user to home.
    """
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user.userprofile:
        post.delete()
        messages.add_message(
            request, messages.SUCCESS, "Post successfully deleted")

        next_pg = request.GET.get('next', '/')
        return HttpResponseRedirect(next_pg)

    else:
        return redirect('home')  # add message for user here.


class ReviewPostView(LoginRequiredMixin, DetailView, UpdateView):
    """
    Render single post for moderator review.
    """
    model = Post
    template_name = 'post_review.html'
    context_object_name = 'post'
    fields = ['mod_message']

    def get_form(self, Post=None):
        form = super(ReviewPostView, self).get_form(Post)
        form.fields['mod_message'].required = True
        return form

    def get(self, *args, **kwargs):
        user = get_object_or_404(User, pk=self.request.user.pk)
        post = get_object_or_404(Post, pk=self.kwargs['pk'])

        # comparison with user.id needed here to solve bug.
        # More info in README.md (bug #4)
        if post.author.user.id is user.id or user.userprofile.is_mod:
            return super(ReviewPostView, self).get(*args, **kwargs)
        else:
            return redirect('home')

    def form_valid(self, form):
        form.instance.moderator = self.request.user
        form.instance.status = 'Review'

        form.save()

        if form.instance.flag:
            flag = PostFlag.objects.filter(pk=form.instance.flag.id)
            flag.delete()

        return HttpResponseRedirect(reverse('review_posts'))


class TagPostsView(SingleObjectMixin, ListView):
    """
    Render all posts that have the selected tag
    """
    paginate_by = 12
    template_name = 'post_by_tag.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=PostTag.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.object
        return context

    def get_queryset(self):
        return self.object.post_tags.all()


@login_required
def like_post(request, pk):
    """ Add like to post, tied to specific user """
    post = get_object_or_404(Post, pk=pk)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post_detail', args=[pk, post.slug]))


@login_required
def bookmark_post(request, pk):
    """ Add post to users bookmarks """
    post = get_object_or_404(Post, pk=pk)

    bookmark, created = Bookmark.objects.get_or_create(
        post=post,
        user=request.user
    )

    if not created:
        bookmark.delete()

    return HttpResponseRedirect(reverse('post_detail', args=[pk, post.slug]))

from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

import datetime

# Create your models here.
class Post(models.Model):
    """
    Create instance of Post
    """
    WAITING = 'Waiting'
    APPROVED = 'Approved'
    REVIEW = 'Review'
    DEACTIVATED = 'Deactivated'
    STATUS_CHOICES = (
        (WAITING, "Awaiting Approval"),
        (APPROVED, "Approved"),
        (REVIEW, "Review"),
        (DEACTIVATED, "Deactivated")
    )
    title = models.CharField(
        max_length=200,
        unique=True,
        error_messages={
            'unique':"This post title already exists, please choose another."
        })
    slug = models.SlugField(max_length=200, unique=True)
    body = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_field')
    created_on = models.DateField(default=datetime.date.today)
    updated_on = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=WAITING)
    mod_message = models.TextField(max_length=300, null=True)
    moderator = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=False, related_name='mod_field')
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk, 'slug': self.slug})
"""models.py for the dcDemoBlog."""
from django.db import models
from django.core.urlresolvers import reverse


# Create your models here.
class Post(models.Model):
    """class Post."""

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.CharField(max_length=255)
    content = models.TextField()
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """."""

        ordering = ['-created']

from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    body = models.TextField()
    publish = models.DataTimeField(default=timezone.now)
    created = models.DataTimeField(auto_now_add=True)
    updated = models.DataTimeField(auto_now=True)

    class Meta:
        ordering = ("-publish")

    def __str__(self):
        return self.title

from django.apps import AppConfig


class BlogPostConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog_post'
    verbose_name = "Посты"

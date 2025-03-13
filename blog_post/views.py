from django.shortcuts import get_object_or_404, render
from .models import Post
from django.http import Http404

def post_list(request):
    posts = Post.published.all()
    return render(
        request, "blog_post/post/list.html",
        {"posts": posts}
    )

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, status=Post.Status.PUBLISHED)
    return render(
        request, "blog_post/post/detail.html",
        {"post": post}
    )
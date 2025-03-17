from django.shortcuts import get_object_or_404, render
from .models import Post

def post_list(request):
    posts = Post.published.all()
    return render(
        request, "blog/post/list.html",
        {"posts": posts}
    )

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, status=Post.Status.PUBLISHED)
    return render(
        request, "blog/post/detail.html",
        {"post": post}
    )

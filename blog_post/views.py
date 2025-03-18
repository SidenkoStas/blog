from django.shortcuts import get_object_or_404, render
from .models import Post
from django.core.paginator import Paginator

def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get("page", 1)
    posts = paginator.get_page(page_number)
    return render(
        request, "blog/post/list.html",
        {"posts": posts}
    )

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, publish__year=year, publish__month=month, publish__day=day,
        slug=post, status=Post.Status.PUBLISHED
    )
    return render(
        request, "blog/post/detail.html",
        {"post": post}
    )

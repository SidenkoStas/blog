from django.shortcuts import get_object_or_404, render
from .models import Post
from django.core.paginator import Paginator
from django.views.generic import ListView
from .forms import EmailPostForm

class PostList(ListView):
    """
    Представление-класс для обработки всех постов.
    """
    queryset = Post.objects.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"

def post_list(request):
    """
    Представление для обработки всех постов.
    """
    posts = Post.published.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get("page", 1)
    posts = paginator.get_page(page_number)
    return render(
        request, "blog/post/list.html",
        {"posts": posts}
    )

def post_detail(request, year, month, day, post):
    """
    Представление для обработки поста в отдельности.
    """
    post = get_object_or_404(
        Post, publish__year=year, publish__month=month, publish__day=day,
        slug=post, status=Post.Status.PUBLISHED
    )
    return render(
        request, "blog/post/detail.html",
        {"post": post}
    )

def post_share(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk, status=Post.Status.PUBLISHED)
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
    else:
        form = EmailPostForm()
    return  render(
        request, "blog/post/share.html",
        {"post": post, "form": form}
    )
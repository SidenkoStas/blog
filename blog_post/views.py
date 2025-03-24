from django.shortcuts import get_object_or_404, render
from .models import Post
from django.core.paginator import Paginator
from django.core.mail import send_mail
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
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            post_url =  (post.get_absolute_url())
            subject = (
                f"{clean_data["name"]} ({clean_data["email"]}) "
                f"Рекомендую тебе почитать {post.title}"
            )
            message = (
                f"Прочти {post.title} по ссылке {post_url}\n"
                f"Коментарии {clean_data["name"]}: {clean_data["comment"]}"
            )
            send_mail(
                subject, message, from_email="My blog <volondss@gmail.com>",
                recipient_list=[clean_data["to"]]
            )
            sent = True
    else:
        form = EmailPostForm()
    return  render(
        request, "blog/post/share.html",
        {"post": post, "form": form, "sent": sent}
    )
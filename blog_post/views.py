from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from .forms import EmailPostForm, CommentForm
from .models import Post, Comment
from taggit.models import Tag

class PostList(ListView):
    """
    Представление-класс для обработки всех постов.
    """
    queryset = Post.objects.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            tag_slug = self.request.GET.tag_slug
        except AttributeError:
            tag_slug = None
        if tag_slug:
            pass
        context["tags"] = Tag.objects.all()
        print(self.request.GET)
        return context

def post_detail(request, year, month, day, post):
    """
    Представление для обработки поста в отдельности.
    """
    post = get_object_or_404(
        Post, publish__year=year, publish__month=month, publish__day=day,
        slug=post, status=Post.Status.PUBLISHED
    )
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(
        request, "blog/post/detail.html",
        {"post": post, "comments": comments, "form": form}
    )

@require_POST # Разрешает тоько метод ПОСТ
def post_comment(request, post_id):
    post = get_object_or_404(
        Post, id=post_id, status=Post.Status.PUBLISHED
    )
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request, "blog/post/comment.html",
        {"post": post, "form": form, "comment": comment}
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

def post_list(request, tag_slug=None):
    """
    Представление для обработки всех постов.
    """
    posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts, 3)
    page_number = request.GET.get("page", 1)
    posts = paginator.get_page(page_number)
    return render(
        request, "blog/post/list.html",
        {"posts": posts, "tag": tag}
    )
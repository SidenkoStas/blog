from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from .forms import EmailPostForm, CommentForm, SearchForm
from .models import Post
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

class PostList(ListView):
    """
    Представление-класс для обработки всех постов.
    """
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            tag_slug = self.request.GET["tag_slug"]
        except AttributeError:
            tag_slug = None
        if tag_slug:
            pass
        context["tags"] = Tag.objects.all()
        print(self.request.GET)
        return context

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

    # Список похожих постов по тегам
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids
    ).exclude(id=post.id)
    similar_posts = similar_posts.annotate(
        same_tags=Count("tags"),
    ).order_by("-same_tags", "-publish")[:4]

    return render(
        request, "blog/post/detail.html",
        {"post": post, "comments": comments, "form": form,
         "similar_posts": similar_posts}
    )

@require_POST # Разрешает тоько метод ПОСТ
def post_comment(request, post_id):
    """
    Опубликовать комментарий к посту.
    Только POST разрешён.
    """
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
    """
    Поделиться постом по почте.
    """
    post = get_object_or_404(Post, pk=post_pk, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            post_url =  request.build_absolute_uri(post.get_absolute_url())
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

def post_search(request):
    """
    Поисковик в постах.
    """
    form = SearchForm()
    search = None
    results = []

    if "search" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            search = form.cleaned_data["search"]
            search_vector = SearchVector(
                "title", "body", config="russian"
            )
            search_query = SearchQuery(search, config="russian")
            results = Post.published.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by("-rank")
    return render(
        request, "blog/post/search.html",
        {"form": form, "search": search, "results": results}
    )
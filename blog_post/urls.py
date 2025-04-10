from django.urls import path
from . import views
from .feeds import LatestPostFeed

app_name = "blog"

urlpatterns = [
    # path("", PostList.as_view(), name="post_list"),
    path("", views.post_list, name="post_list"),
    path("tag/<slug:tag_slug>/", views.post_list, name="post_list_by_tag"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/", views.post_detail,
        name="post_detail"
    ),
    path("<int:post_pk>/share/", views.post_share, name="post_share"),
    path("<int:post_id>/comment/", views.post_comment, name="post_comment"),
    path("searching/", views.post_search, name="post_search"),
    path("feed/", LatestPostFeed(), name="post_feed"),
]
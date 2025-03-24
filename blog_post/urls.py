from django.urls import path
from .views import post_detail, post_share, PostList

app_name = "blog"

urlpatterns = [
    path("", PostList.as_view(), name="post_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/", post_detail,
        name="post_detail"
    ),
    path("<int:post_pk>/share/", post_share, name="post_share")
]
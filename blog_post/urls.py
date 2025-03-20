from django.urls import path
from .views import post_list, post_detail, PostList

app_name = "blog"

urlpatterns = [
    path("", PostList.as_view(), name="post_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/", post_detail,
        name="post_detail"
    ),
]
import  markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatechars_html
from django.urls import reverse_lazy
from .models import Post

class LatestPostFeed(Feed):
    title = "My Blog Post"
    link = reverse_lazy("blog:post_list")
    description = "My Post of My Blog"

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatechars_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item):
        return item.publish
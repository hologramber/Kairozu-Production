from django.contrib.syndication.views import Feed
from news.models import Post
from django.utils.feedgenerator import Atom1Feed
from django.utils.html import strip_tags

class RssSiteNewsFeed(Feed):
    title = "Kairozu Blog & Site Updates"
    link = "/news/"
    description = "Adventures in understanding Japanese with programmed learning & natural language processing."

    def items(self):
        return Post.objects.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return strip_tags(item.indextext)

class AtomSiteNewsFeed(RssSiteNewsFeed):
    feed_type = Atom1Feed
    subtitle = RssSiteNewsFeed.description

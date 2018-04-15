from django.contrib.syndication.views import Feed
from news.models import Post
from django.utils.feedgenerator import Atom1Feed
from django.utils.html import strip_tags

class RssSiteNewsFeed(Feed):
    title = "Kairozu Blog & Site Updates"
    link = "/news/"
    description = "回路図 uses programmed learning to build an understanding of Japanese grammar using English-to-Japanese sentence construction. Site updates, random thoughts, and adventures in natural language processing with Japanese and Python."

    def items(self):
        return Post.objects.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return strip_tags(item.indextext)

class AtomSiteNewsFeed(RssSiteNewsFeed):
    feed_type = Atom1Feed
    subtitle = RssSiteNewsFeed.description

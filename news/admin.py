from django.contrib import admin
from .models import Post, FAQ, KnownIssue, SiteIssue


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'published', 'published_date']
    # list_filter = ['published']
    # search_fields = ['title','text']
    # date_hierarchy = ['published_date']
    prepopulated_fields = {"slug":("title",)}

admin.site.register(KnownIssue)
admin.site.register(Post, PostAdmin)
admin.site.register(FAQ)
admin.site.register(SiteIssue)
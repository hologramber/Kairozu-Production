from django.contrib import admin
from .models import Sandcastle, Resource


class SandcastleAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'location']


class ResourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'type']


admin.site.register(Sandcastle, SandcastleAdmin)
admin.site.register(Resource, ResourceAdmin)


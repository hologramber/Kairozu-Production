from django.contrib import admin
from .models import Sandcastle

class SandcastleAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'location']

admin.site.register(Sandcastle, SandcastleAdmin)


from django.db import models

class Sandcastle(models.Model):
    title = models.CharField(max_length=250, blank=False)
    description = models.CharField(max_length=250, blank=False)
    location = models.CharField(max_length=250, blank=False)
    iconname = models.CharField(max_length=250, default="fa-puzzle-piece", blank=False)

    def __str__(self):
        return self.title

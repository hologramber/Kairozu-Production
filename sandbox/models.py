from django.db import models
from model_utils import Choices


class Sandcastle(models.Model):
    title = models.CharField(max_length=250, blank=False)
    description = models.CharField(max_length=250, blank=False)
    location = models.CharField(max_length=250, blank=False)
    iconname = models.CharField(max_length=250, default="fa-puzzle-piece", blank=False)

    def __str__(self):
        return self.title


class Resource(models.Model):
    name = models.CharField(max_length=250, unique=False, blank=False)
    description = models.CharField(max_length=250, unique=False, blank=True)
    RESOURCE_TYPE_CHOICES = Choices('general', 'edutility', 'dictionary', 'kanji', 'kana', 'edureading', 'reference', 'video', 'japan', 'exchange', 'technical', 'other')
    type = models.CharField(choices=RESOURCE_TYPE_CHOICES, default=RESOURCE_TYPE_CHOICES.other, max_length=20)
    MEDIUM_CHOICES = Choices('globe', 'desktop', 'apple', 'android', 'book', 'gear', 'blank')
    medium_one = models.CharField(choices=MEDIUM_CHOICES, default=MEDIUM_CHOICES.blank, max_length=15)
    url_one = models.CharField(max_length=250, unique=False, blank=True)
    medium_two = models.CharField(choices=MEDIUM_CHOICES, default=MEDIUM_CHOICES.blank, max_length=15)
    url_two = models.CharField(max_length=250, unique=False, blank=True)
    medium_three = models.CharField(choices=MEDIUM_CHOICES, default=MEDIUM_CHOICES.blank, max_length=15)
    url_three = models.CharField(max_length=250, unique=False, blank=True)

    class Meta:
        ordering = ['type']

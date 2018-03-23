from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=250, blank=False)
    slug = models.SlugField(unique=True, max_length=250)
    indextext = models.TextField(default='')
    text = models.TextField(blank=False)
    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(auto_now_add=True)

    POST_CATEGORY_CHOICES = (
        ('KAI', 'Kairozu'),     # 1
        ('NLP', 'NLP'),     # 2
        ('JPN', 'Japanese'),         # 4
    )
    post_category = models.CharField(max_length=8, choices=POST_CATEGORY_CHOICES, default='KAI', blank=False)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:newspost', kwargs={'slug': self.slug})


class FAQ(models.Model):
    question = models.CharField(max_length=250, blank=False)
    answer = models.TextField(blank=False)
    vieworder = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ['vieworder']

    def __str__(self):
        return self.question


class KnownIssue(models.Model):
    ISSUE_TYPE_CHOICES = (
        ('FRONTEND', 'Front-End / Design'),
        ('BACKEND', 'Back-End / Database'),
        ('GRAMMAR', 'Grammar / Japanese'),
        ('FUTURE', 'Future Feature'),
        ('NONE', 'Uncategorized'),
        ('OTHER', 'Other Issue'),
    )
    issue_type = models.CharField(max_length=10, choices=ISSUE_TYPE_CHOICES, default='NONE', blank=False)
    issue_date = models.DateTimeField(auto_now_add=True, blank=True)
    issue_description = models.TextField(max_length=800, default='', blank=True)

    ISSUE_STATUS_CHOICES = (
        ('UNFIXED', 'Unfixed'),     # 1
        ('TESTING', 'Testing'),     # 2
        ('FIXED', 'Fixed'),         # 4
        ('NONE', 'No Status'),      # 3
    )
    issue_status = models.CharField(max_length=10, choices=ISSUE_STATUS_CHOICES, default='NONE', blank=False)

    ISSUE_PRIORITY_CHOICES = (
        ('XFUTURE', 'Future'),      # 4
        ('QLOW', 'Low'),            # 3
        ('NORMAL', 'Normal'),       # 2
        ('HIGH', 'High'),           # 1
    )
    issue_priority = models.CharField(max_length=10, choices=ISSUE_PRIORITY_CHOICES, default='NONE', blank=False)

    class Meta:
        ordering = ['-issue_status', 'issue_priority', 'issue_type', 'issue_date']

    def __str__(self):
        return self.issue_description

class SiteIssue(models.Model):
    report_by_user = models.PositiveIntegerField(default=0, blank=False)
    report_from_url = models.URLField(max_length=250, default='', blank=True)
    report_datetime = models.DateTimeField(auto_now_add=True, blank=True)
    report_comment = models.TextField(max_length=800, default='', blank=True)

    GRAMMAR = 'G'
    TYPO = 'P'
    TECHNICAL = 'T'
    OTHER = 'O'
    REPORT_TYPE_CHOICES = (
        (GRAMMAR, 'Incorrect grammar (English or Japanese).'),
        (TYPO, 'Typo (missing or misspelled words).'),
        (TECHNICAL, 'Technical issues (something is broken).'),
        (OTHER, 'None of the above.'),
    )
    report_type = models.CharField(max_length=1, choices=REPORT_TYPE_CHOICES, default=OTHER, blank=False)

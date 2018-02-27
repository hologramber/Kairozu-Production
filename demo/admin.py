from django.contrib import admin
from .models import DemoVocab, DemoPractice, DemoSentence, DemoExpression, BetaEmail


class DemoVocabAdmin(admin.ModelAdmin):
    list_display = ['english', 'kana']


class DemoExpressionAdmin(admin.ModelAdmin):
    list_display = ['english', 'kana']


class DemoPracticeAdmin(admin.ModelAdmin):
    list_display = ['pone_english', 'ptwo_english']


class DemoSentenceAdmin(admin.ModelAdmin):
    list_display = ['english', 'kana']


class BetaEmailAdmin(admin.ModelAdmin):
    list_display = ['user_beta_email', 'user_beta_submitted']

admin.site.register(DemoVocab, DemoVocabAdmin)
admin.site.register(DemoPractice, DemoPracticeAdmin)
admin.site.register(DemoSentence, DemoSentenceAdmin)
admin.site.register(DemoExpression, DemoExpressionAdmin)
admin.site.register(BetaEmail, BetaEmailAdmin)
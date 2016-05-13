from django.contrib import admin
from .models import *
import sys
reload(sys)
sys.setdefaultencoding("utf8")                  # http://www.binss.me/blog/unicode-decode-error-when-access-django-admin/

# Register your models here.
class NoteAdmin(admin.ModelAdmin):
    fields = ["word", "user", "content", "time"]
    list_display = ["content", "word", "user"]


class WordAdmin(admin.ModelAdmin):
    list_display = ["content"]


class LearningWordAdmin(admin.ModelAdmin):
    list_display = ["word", "user"]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "daily_words_amount", "current_vocabulary"]


admin.site.register(Word, WordAdmin)
admin.site.register(Vocabulary)
admin.site.register(Note, NoteAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(LearningWord, LearningWordAdmin)

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Word)
admin.site.register(Vocabulary)
admin.site.register(Memo)
admin.site.register(UserProfile)

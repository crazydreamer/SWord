from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Word(models.Model):
    content = models.CharField("Content", max_length=100)
    description = models.TextField("Description")
    example = models.TextField("Example Sentence", default="")
    vocabulary = models.ManyToManyField("Vocabulary", default="")

    def __str__(self):
        return self.content


class Vocabulary(models.Model):
    name = models.CharField("Name", max_length=100)
    description = models.TextField("Description", default="")

    def __str__(self):
        return self.name


class Memo(models.Model):
    word = models.ForeignKey("Word", on_delete=models.CASCADE)
    content = models.TextField("Content", default="")
    user = models.ForeignKey(User)

    def __str__(self):
        return self.word


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    memorized_words = models.ManyToManyField("Word", blank=True)
    current_vocabulary = models.ForeignKey("Vocabulary", 
                    on_delete=models.SET_NULL, null=True)
    daily_words_amount = models.SmallIntegerField("Daily Words Amount", default=100)

    def __str__(self):
        return self.user.username


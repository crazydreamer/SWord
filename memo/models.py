# coding: utf-8

from __future__ import unicode_literals

from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Word(models.Model):
    """单词"""

    content = models.CharField("Content", max_length=100, unique=True)
    description = models.TextField("Description", )
    example = models.TextField("Example Sentence", default="")
    vocabulary = models.ManyToManyField("Vocabulary")

    def information(self):
        return {
            "id": self.id,
            "content": self.content,
            "description": self.description,
            "example": self.example,
        }

    def __str__(self):
        return self.content


class Vocabulary(models.Model):
    """词库"""

    name = models.CharField("Name", max_length=100)
    description = models.TextField("Description", default="")

    def __str__(self):
        return self.name


class Note(models.Model):
    """笔记"""

    word = models.ForeignKey("Word", on_delete=models.CASCADE, null=False)
    content = models.TextField("Content", default="")
    time = models.DateTimeField("Publish time", default=datetime.now())
    user = models.ForeignKey(User, null=False)

    def information(self):
        return {
            "content": self.content,
            "user": self.user.username
        }

    def __str__(self):
        return " " .join([self.word.content.encode("utf-8"), self.content.encode("utf-8")])


class UserProfile(models.Model):
    """用户信息"""

    user = models.OneToOneField(User)
    memorized_words = models.ManyToManyField("Word", blank=True, 
                            related_name="memorized_words")
    current_vocabulary = models.ForeignKey("Vocabulary", 
                    on_delete=models.SET_NULL, null=True)
    daily_words_amount = models.SmallIntegerField("Daily Words Amount", default=20)

    def __str__(self):
        return self.user.username

class LearningWord(models.Model):
    """本日正在学习的单词"""

    word = models.ForeignKey("Word")
    user = models.ForeignKey(User)
    status = models.SmallIntegerField("Word Status", default=3)                 # 0, 1, 2, 3 分别代表背过，对一次，不对，未背
    # 可以在此添加学习次数等

    def __str__(self):
        return self.user.username+" - "+self.word.content

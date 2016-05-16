# coding: utf-8

from memo.models import Word, Note
from django.contrib.auth.models import User

def add_note():
    user = User.objects.get(username='user')
    words = Word.objects.all()
    for word in words:
        c = word.content
        note = Note(word=word, content="Note of %s"%c, user=user)
        note.save()
        print word.content

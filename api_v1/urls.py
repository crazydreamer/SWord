# coding: utf-8

from django.conf.urls import include, url
import words
import memorize as memo

app_name = 'api_v1'
urlpatterns = [
    url(r'^word/(?P<word_id>[0-9]+)/note/?$', words.note, name='note'),
    url(r'^word/(?P<word_id>[0-9]+)/?$', words.word, name='word'),
    url(r'^search/?$', words.search, name='search'),
    url(r'^memo_status/(?P<learning_id>[0-9]+)?/?$', memo.status, name='status'),
    url(r'^memo_finish/?$', memo.finish, name='finish'),
]

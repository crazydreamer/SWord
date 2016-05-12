# coding: utf-8

from django.conf.urls import include, url
import views
import memorize as memo

app_name = 'api_v1'
urlpatterns = [
    url(r'^word/(?P<word_id>[0-9]+)/note/?$', views.note, name='note'),
    url(r'^word/(?P<word_id>[0-9]+)/?$', views.word, name='word'),
    # TODO: 添加 Search API
    url(r'^memo_status/(?P<learning_id>[0-9]+)?/?$', memo.status, name='status'),
    url(r'^memo_finish/?$', memo.finish, name='finish'),
]

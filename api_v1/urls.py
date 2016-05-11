from django.conf.urls import include, url
import views
import memorize as memo

app_name = 'api_v1'
urlpatterns = [
    url(r'^note/(?P<word_id>[0-9]+)/?$', views.note, name='note'),
    url(r'^word/(?P<word_id>[0-9]+)/?$', views.word, name='word'),
    url(r'^memo/status/?$', memo.status, name='status'),
    url(r'^memo/word/(?P<word_id>[0-9]+)/?$', memo.word_status, name='word_status'),
    url(r'^memo/finish/?$', memo.finish, name='finish'),
]

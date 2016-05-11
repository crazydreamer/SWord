from django.conf.urls import include, url
import views

app_name = 'api_v1'
urlpatterns = [
    url(r'^note/(?P<word_id>[0-9]+)/?$', views.note, name='note'),
    url(r'^word/(?P<word_id>[0-9]+)/?$', views.word, name='word'),
]

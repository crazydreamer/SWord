from django.conf.urls import include, url
import views, auth

app_name = 'memo'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/?$', views.profile, name='profile'),
    url(r'^word/(?P<word>([A-Za-z\'\-\.]+)|(\d+))/?$', views.word, name="word"),
    url(r'^memo/?$', views.memorizing, name="memorizing"),
]

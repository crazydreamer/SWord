from django.conf.urls import include, url
import views, auth

app_name = 'memo'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/?$', views.profile, name='profile'),
    url(r'^word/(?P<word>[A-Za-z\'\-\.]+)?$', views.find_word, name="find_word"),
    url(r'^memo/?$', views.memorizing, name="memorizing"),
]

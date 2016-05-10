from django.conf.urls import include, url
import views, auth

app_name = 'memo'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]

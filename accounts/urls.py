from django.conf.urls import include, url
import views

app_name = 'accounts'
urlpatterns = [
    url(r'^login/?$', views.user_login, name='login'),
    url(r'^logout/?$', views.user_logout, name='logout'),
    url(r'^register/?$', views.user_register, name='register'),
]

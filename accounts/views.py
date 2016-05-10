# coding: utf-8

from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.conf import settings


def user_login(request):
    if not request.user.is_active:
        next_url = request.GET.dict().get("next", "/")

        if request.method == "GET":
            return render(request, "accounts/login.html")
        elif request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if (user is not None) and user.is_active:
                login(request, user)
                return HttpResponseRedirect(next_url)
            else:
                error_message = "Invalid username or password (╯3╰)"
                return render(request, "accounts/login.html", {
                        "error": error_message
                    })
                # return HttpResponseRedirect(request.get_full_path())
    else:
        return HttpResponseRedirect(reverse("memo:index"))


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("memo:index"))

    
def user_register(request):
    return HttpResponseRedirect(reverse("memo:index"))

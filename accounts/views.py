# coding: utf-8

import re
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from memo.models import UserProfile


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
    if not request.user.is_active:
        if request.method == "GET":
            return render(request, "accounts/register.html")

        elif request.method == "POST":
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password']
            password2 = request.POST['repeat-password']

            # 数据合法性检查
            if password1 != password2:
                error_message = "Password doesn't match!"

            elif len(password1) < 6:
                error_message = "Password must be as least 6 characters!"

            elif not re.match(r"^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$", email):
                error_message = "Email is not valid!"

            else:
                try:
                    user = User.objects.create_user(username, email, password1)
                except IntegrityError:
                    error_message = "User already exists!"
                else:
                    user_profile = UserProfile(user=user)
                    user_profile.save()
                    user = authenticate(username=username, password=password1)
                    login(request, user)
                    return HttpResponseRedirect(reverse("memo:index"))

            return render(request, "accounts/register.html", {
                        "error": error_message
                    })
            
    else:
        return HttpResponseRedirect(reverse("memo:index"))

# coding: utf-8

from django.http import JsonResponse


def authenticated_required(func):
    """验证用户是否登录"""
    def _wrapped_func(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)
        else:
            return JsonResponse({
                    "success": False,
                    "reason": "Login required"
                }, status=401)

    return _wrapped_func

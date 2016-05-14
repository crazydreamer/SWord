# coding: utf-8

from django.http import JsonResponse
from memo.models import Word, Note
from .decorator import authenticated_required


@authenticated_required
def note(request, word_id):
    """获取及添加单词笔记"""
    try:
        word = Word.objects.get(pk=word_id)
    except Word.DoesNotExist:
        return JsonResponse({
                    "success": False, 
                    "reason": "Word does not exist"
                }, status=404)
    if request.method == "GET":
        start = int(request.GET.get("from", 0))
        end = int(request.GET.get("to", start+10))

        if start >= 0 and end >= 0 and start >= end:
            return JsonResponse({
                        "success": False, 
                        "reason": "start or end parameter error"
                    }, status=400)
        else:
            notes = word.note_set.order_by("-time")[start:end]
            note_data = [note.information() for note in notes]
            
            return JsonResponse({ "success": True, "note": note_data })

    elif request.method == "POST":
        content = request.POST.get("content", None)

        if not content:
            return JsonResponse({
                        "success": False, 
                        "reason": "Empty content"
                    }, status=400)

        note = Note(word=word, content=content, user=request.user)
        note.save()
        return JsonResponse({
                    "success": True,
                    "note": note.information()
                }, status=201)


@authenticated_required
def word(request, word_id):
    """通过 ID 获取单词信息"""
    try:
        word = Word.objects.get(pk=word_id)
    except Word.DoesNotExist:
        return JsonResponse({
                    "success": False, 
                    "reason": "Word does not exist"
                }, status=404)

    return JsonResponse({
            "success": True,
            "word": word.information()
            })


def search(request):
    """单词查询"""
    if request.method == "GET":
        content = request.GET.get("word", None)
        if content is not None:
            try:
                word = Word.objects.get(content=content)
            except Word.DoesNotExist:
                return JsonResponse({"success": False, "reason": "Word does not exist"},
                                status=404)
            return JsonResponse({
                        "success": True,
                        "word": word.information()
                    })
        else:
            return JsonResponse({
                    "success": False,
                    "reason": "Invalid query"
                })

    return JsonResponse({
            "success": True,
            "word": word.information()
            })

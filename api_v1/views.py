from django.http import JsonResponse
from django.shortcuts import render
from memo.models import Word, Note


def note(request, word_id):
    if request.user.is_authenticated():
        try:
            word = Word.objects.get(pk=word_id)
        except Word.DoesNotExist:
            return JsonResponse({"success": False, "reason": "Word does not exist"},
                            status=404)

        if request.method == "GET":
            start = int(request.GET.get("from", 0))
            end = int(request.GET.get("to", start+10))

            if start >= 0 and end >= 0 and start >= end:
                return JsonResponse({
                        "success": False, 
                        "reason": "start or end parameter error"
                    }, status=400)
            else:
                notes = word.note_set.all()[start:end]
                note_data = [note.information() for note in notes]
                
                return JsonResponse({ "success": True, "notes": note_data })

        elif request.method == "POST":
            content = request.POST.get("content", None)

            if not content:
                return JsonResponse({
                        "success": False, 
                        "reason": "Empty content"
                    }, status=400)
            note = Note(word=word, content=content, user=request.user)
            note.save()
            return JsonResponse({ "success": True })

    else:
        return JsonResponse({
            "success": False,
            "reason": "Login required"
        }, status=401)


def word(request, word_id):
    if request.user.is_authenticated():
        try:
            word = Word.objects.get(pk=word_id)
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
            "reason": "Login required"
        }, status=401)

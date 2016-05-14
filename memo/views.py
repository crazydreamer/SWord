# coding: utf-8

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import Vocabulary, UserProfile, Word


def index(request):
    return render(request, "memo/index.html")


@login_required
def profile(request):
    profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        try:
            voc_id = int(request.POST["vocabulary"])
        except ValueError:
            voc_id = -1
        try:
            daily_words = int(request.POST["daily_words"])
        except ValueError:
            daily_words = -1

        if daily_words > 0:
            profile.daily_words_amount = daily_words
        else:
            messages.add_message(request, messages.WARNING, '词数设置错误！')

        try:
            voc = Vocabulary.objects.get(pk=voc_id)
            profile.current_vocabulary = voc
        except Vocabulary.DoesNotExist:
            messages.add_message(request, messages.WARNING, '词书选择错误！')

        profile.save()

    vocs = Vocabulary.objects.all()
    current_voc = profile.current_vocabulary

    context = { 
            "vocs": vocs,
            "current_voc": current_voc,
            "daily_words": profile.daily_words_amount,
            "total_words": profile.memorized_words.count()
        }
    return render(request, "memo/profile.html", context)


def word(request, word):
    try:
        word_id = int(word)
        word = get_object_or_404(Word, pk=word_id)
    except ValueError:
        word = get_object_or_404(Word, content=word)

    context = word.information()
    notes = []
    for note in word.note_set.order_by("-time")[:5]:
        notes.append({
                "content": note.content,
                "user": note.user.username
            })

    context["notes"] = notes
    return render(request, "memo/word.html", context)


@login_required
def memorizing(request):
    voc = UserProfile.objects.get(user=request.user).current_vocabulary
    if voc is None:
        messages.add_message(request, messages.INFO, '请选择词书~')
        return HttpResponseRedirect(reverse("memo:profile"))
        
    return render(request, "memo/memorizing.html")

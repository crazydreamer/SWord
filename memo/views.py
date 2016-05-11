from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Vocabulary, UserProfile

def index(request):
    return render(request, "memo/index.html", {})


@login_required
def profile(request):
    profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        voc_name = request.POST["vocabulary"]
        voc = Vocabulary.objects.get(name=voc_name)
        profile.current_vocabulary = voc
        profile.save()

    vocs = [v.name for v in Vocabulary.objects.all()]
    current_voc = profile.current_vocabulary


    vocs.remove(current_voc.name)
    vocs.insert(0, current_voc.name)

    context = { 
            "vocs": vocs,
            "total_words": profile.memorized_words.count()
        }
    return render(request, "memo/profile.html", context)


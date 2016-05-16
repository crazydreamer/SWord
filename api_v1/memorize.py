# coding: utf-8

from django.http import JsonResponse
from memo.models import Word, Note, LearningWord
from django.http import QueryDict
from .decorator import authenticated_required


def __select_word(user):
    return Word.objects.raw("""
    SELECT MW.*
    FROM memo_word AS MW, memo_word_vocabulary AS MWV, memo_userprofile AS UP
    WHERE MW.id = MWV.word_id                 
        AND MWV.vocabulary_id = UP.current_vocabulary_id
        AND UP.user_id = {id_}
        AND MW.id NOT IN (SELECT word_id
                        FROM memo_userprofile_memorized_words AS MUMW, memo_userprofile AS UP
                        WHERE MUMW.userprofile_id = UP.id
                            AND UP.user_id = {id_})
    ORDER BY random()
    LIMIT (SELECT UP.daily_words_amount
            FROM memo_userprofile AS UP
            WHERE UP.user_id = {id_});""".format(id_=user.id))


@authenticated_required
def status(request, learning_id=None):
    """返回或更新用户当前的背单词情况以及单词信息"""
    if request.method == "GET":
        current_user = request.user
        learning_words = LearningWord.objects.filter(user=current_user)
        if not learning_words.count():                                          # 存在未背完的单词
            words = __select_word(current_user)                                 # 随机生成一组单词
            learning_words = [LearningWord(user=current_user, word=w) for w in words]
            map(lambda x: x.save(), learning_words)                             # 将单词加入 LearningWord 中

        data = {
            "success": True,
            "words": []
        }
        for lw in learning_words:
            word = lw.word
            inf = word.information()
            inf["status"] = lw.status
            inf["word_id"] = word.id
            inf["learning_id"] = lw.id

            notes = Note.objects.filter(word=word)
            inf["notes"] = [n.information() for n in notes]
            data["words"].append(inf)

        return JsonResponse(data)

    elif request.method == "PUT":
        put = QueryDict(request.body)                                       # 手动获取 PUT 信息
        status = int(put.get('status'))

        learning = LearningWord.objects.get(pk=int(learning_id))
        if learning.user != request.user:
            return JsonResponse({
                    "success": False,
                    "reason": "Unauthorized"
                }, status=401)

        learning.status = status
        learning.save()

        return JsonResponse({
                "success": True
            })

    else:
        return JsonResponse({
        "success": False,
        "reason": "Method not allowed"
    }, status=405)


@authenticated_required
def finish(request):
    """用户已完成，将用户所有正在学习的单词转移至已掌握，只接受POST"""
    if request.method == "POST":
        user = request.user
        profile = user.userprofile
        learning_words = LearningWord.objects.filter(user=user)
        for lw in learning_words:
            word = lw.word
            profile.memorized_words.add(word)
        learning_words.delete()
        return JsonResponse({ "success": True })
    else:
        return JsonResponse({
        "success": False,
        "reason": "Method not allowed"
    }, status=405)


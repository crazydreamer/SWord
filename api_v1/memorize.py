# coding: utf-8

from django.http import JsonResponse
from memo.models import Word, Note, UserProfile, LearningWord

def __select_word(user):
    return Word.objects.raw("""
    SELECT MW.*
    FROM memo_word AS MW, memo_word_vocabulary AS MWV, memo_userprofile AS UP, auth_user AS AU
    WHERE MW.id = MWV.word_id                 
        AND MWV.vocabulary_id = UP.current_vocabulary_id
        AND UP.user_id = AU.id
        AND AU.id = {id_}
        AND MW.id NOT IN (SELECT word_id
                        FROM memo_userprofile_memorized_words AS MUMW, memo_userprofile AS UP, auth_user AS AU
                        WHERE MUMW.userprofile_id = UP.id
                            AND UP.user_id = AU.id
                            AND AU.id = {id_})
    ORDER BY random()
    LIMIT (SELECT UP.daily_words_amount
            FROM memo_userprofile AS UP, auth_user AS AU
            WHERE UP.user_id = AU.id
                AND AU.id = {id_});""".format(id_=user.id))


def status(request):
    """返回用户当前的背单词情况以及单词信息，只允许 GET"""

    if request.user.is_authenticated():
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

    else:
        return JsonResponse({
            "success": False,
            "reason": "Login required"
        }, status=401)


def word_status(request, word_id):
    """更新用户单词状态，只允许 POST"""
    if request.user.is_authenticated():                                         # 考虑加一个装饰器
        if request.method == "POST":
            status = int(request.POST["status"])
            learning = LearningWord.objects.get(pk=int(word_id))                # TODO: 数据合法性判断！
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

    else:
        return JsonResponse({
            "success": False,
            "reason": "Login required"
        }, status=401)


def finish(request):
    """用户已完成"""
    pass
# coding: utf-8

from django.http import JsonResponse
from memo.models import Word, Note, UserProfile

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
                AND AU.id = {id_});""".format(_id=user.id))


def status(request):
    """返回用户当前的背单词情况以及单词信息，只允许 GET"""

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




def word_status(request):
    """更新用户单词状态，只允许 POST"""
    pass


def finish(request):
    """用户已完成"""
    pass

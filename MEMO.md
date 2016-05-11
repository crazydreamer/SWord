直接用 raw SQL 生成单词

```SQL
SELECT MW.*
    FROM memo_word AS MW, memo_word_vocabulary AS MWV, memo_userprofile AS UP, auth_user AS AU
    WHERE MW.id = MWV.word_id                 
        AND MWV.vocabulary_id = UP.current_vocabulary_id
        AND UP.user_id = AU.id
        AND AU.id = 1
        AND MW.id NOT IN (SELECT word_id
                        FROM memo_userprofile_memorized_words AS MUMW, memo_userprofile AS UP, auth_user AS AU
                        WHERE MUMW.userprofile_id = UP.id
                            AND UP.user_id = AU.id
                            AND AU.id = 1)
ORDER BY random()
LIMIT (SELECT UP.daily_words_amount
        FROM memo_userprofile AS UP, auth_user AS AU
        WHERE UP.user_id = AU.id
            AND AU.id = 1);
```

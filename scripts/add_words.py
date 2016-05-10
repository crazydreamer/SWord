# coding: utf-8

# import re
import random
from memo.models import Word, Vocabulary

def add_word(word):
    """添加单词"""

    f = file("scripts/vocabulary.txt", "r")
    # f = file("vocabulary.txt", "r")

    for line in f:
        word, exp = line.strip().split(" ", 1)
        sentence = "I'm memorizing word \"%s\""%word

        w = Word(content=word, description=exp, example=sentence)
        w.save()
        # if not re.match(r"^[a-zA-Z.\-']+$", word):
        #     print word
        
    f.close()


def make_vocabulary():
    """将单词随机添加至词库
    第一次添词添反了，囧
    """

    vs = list(Vocabulary.objects.all())

    for w in Word.objects.all():
        vocs = []

        for i, v in enumerate(vs):
            if random.random() <= (0.9-0.2*i):
                vocs.append(v)
        w.vocabulary = vocs

        print w

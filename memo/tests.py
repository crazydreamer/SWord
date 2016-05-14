# coding: utf-8

from django.test import TestCase
from django.utils import timezone
from .models import Note, Word, Vocabulary, UserProfile
from django.contrib.auth.models import User
from api_v1.memorize import __select_word as select_word


# Create your tests here.
class NoteTests(TestCase):
    def setUp(self):
        self.test_user = User(username="user", password="password")
        self.test_user.save()
        self.test_word = Word(content="word", description=u"单词")
        self.test_word.save()

    def test_default_note_creation_time(self):
        """Default creation time should be now"""
        note = Note(content="", user=self.test_user, word=self.test_word)
        now = timezone.now()
        note.save()
        self.assertTrue(-1<=(note.time-now).seconds<=1)


class UserProfileTests(TestCase):
    def setUp(self):
        self.user = User(username="user", password="password")
        self.user.save()
        self.up = UserProfile(user=self.user)
        self.up.save()

    def test_default_params(self):
        """Testing the default parameters of UserProfile"""
        self.assertEqual(self.up.daily_words_amount, 20)
        self.assertEqual(self.up.memorized_words.count(), 0)
        self.assertIsNone(self.up.current_vocabulary)


class WordSelectingTests(TestCase):
    def setUp(self):
        self.voc = Vocabulary(name="voc")
        self.voc.save()
        self.user = User(username="user", password="password")
        self.user.save()
        self.up = UserProfile(user=self.user,
                                current_vocabulary=self.voc,
                                daily_words_amount=35)
        self.up.save()
        f = file("scripts/vocabulary.txt", "r")

        for lno, line in enumerate(f):
            word, exp = line.strip().split(" ", 1)

            w = Word(content=word, description=exp)
            w.save()
            w.vocabulary = [self.voc]
            w.save()
            if lno >= 49:                                                       # 只添加 50 个单词
                break

        f.close()

    def test_select_words(self):
        u"""Testing the words selected randomly"""
        words = select_word(self.user)
        words_set = list(words)
        self.assertEqual(len(words_set), self.up.daily_words_amount)

        for w in words_set:                                                     # 将第一组单词添加到已掌握单词
            self.up.memorized_words.add(w)

        words = select_word(self.user)
        words_set = list(words)
        # 共 50 单词，已掌握 35 个，第二组只能选出 15 个
        self.assertEqual(len(words_set), 15)

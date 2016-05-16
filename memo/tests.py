# coding: utf-8

from datetime import timedelta
from django.utils import timezone
from django.test import TestCase, Client
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Note, Word, Vocabulary, UserProfile


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
        self.assertTrue(-2<=(note.time-now).seconds<=2)


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


class ProfileViewTests(TestCase):
    u"""个人资料页面测试"""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user("user", "", "password")
        self.up = UserProfile(user=self.user)
        self.up.save()
        self.voc = Vocabulary(name="voc")
        self.voc.save()

    def test_profile_view(self):
        u"""访问性测试"""
        response = self.client.get("/home", follow=True)                        # 未登录跳转
        self.assertEqual(response.redirect_chain, [("/accounts/login/?next=/home", 302)])

        self.client.force_login(self.user)
        response = self.client.get("/home")
        self.assertEqual(response.status_code, 200)

    def test_post_parameter(self):
        u"""POST 参数测试"""
        self.client.force_login(self.user)
        response = self.client.post("/home", {
                "daily_words": "",                                              # 空参数
                "vocabulary": ""
            })
        messages = [str(m) for m in list(response.context["messages"])]
        self.assertEqual(len(messages), 2)
        self.assertTrue(u'词数设置错误！' in messages)
        self.assertTrue(u'词书选择错误！' in messages)

        response = self.client.post("/home", {
                "daily_words": "0",                                             # word <= 0
                "vocabulary": "100"                                             # 词书不存在
            })
        messages = [str(m) for m in list(response.context["messages"])]
        self.assertEqual(len(messages), 2)
        self.assertTrue(u'词数设置错误！' in messages)
        self.assertTrue(u'词书选择错误！' in messages)

        response = self.client.post("/home", {
                "daily_words": "100",                                           # 正常参数
                "vocabulary": str(self.voc.id)
            })
        self.assertEqual(response.context["current_voc"], self.voc)
        self.assertEqual(response.context["daily_words"], 100)
        self.assertEqual(response.context["user"].userprofile.daily_words_amount,
                                100)
        self.assertEqual(response.context["user"].userprofile.current_vocabulary,
                                self.voc)


class WordViewTests(TestCase):
    u"""单词页面测试"""
    def setUp(self):
        self.client = Client()
        self.word = Word(content="word", description="word")
        self.word.save()
        self.user = User.objects.create_user("user", "", "password")
        self.notes = []

        start_time = timezone.now()
        for i in range(3):
            n = Note(word=self.word, content="content%d"%i, 
                        user=self.user, time=start_time+timedelta(0, i, 0))     # 三次笔记间隔 1s
            self.notes.append(n)
            n.save()

    def test_word_view(self):
        u"""访问性测试"""
        notes_data = []
        for note in reversed(self.notes):
            notes_data.append({
                    "content": note.content,
                    "user": note.user.username
                })

        response = self.client.get("/word/"+self.word.content)                  # 通过内容访问
        self.assertEqual(response.context["content"], self.word.content)
        self.assertEqual(response.context["notes"], notes_data)

        response = self.client.get("/word/"+str(self.word.id))                  # 通过 id 访问
        self.assertEqual(response.context["content"], self.word.content)
        self.assertEqual(response.context["notes"], notes_data)

        response = self.client.get("/word/abc")                                 # 404
        self.assertEqual(response.status_code, 404)


class MemorizingViewTests(TestCase):
    u"""背单词页面测试"""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user("user", "email", "password")
        self.up = UserProfile(user=self.user)
        self.up.save()
        self.voc = Vocabulary(name="test_voc")
        self.voc.save()

    def test_memorizing_view(self):
        u"""访问性测试"""
        response = self.client.get("/memo", follow=True)                        # 未登录跳转
        self.assertEqual(response.redirect_chain, [("/accounts/login/?next=/memo", 302)])

        self.client.force_login(self.user)                                      # 登录但未选择词书跳转
        response = self.client.get("/memo", follow=True)
        self.assertEqual(response.redirect_chain, [("/home", 302)])
        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), u"请选择词书~")

        self.up.current_vocabulary = self.voc                                   # 正常访问
        self.up.save()
        response = self.client.get("/memo", follow=True)
        self.assertEqual(response.redirect_chain, [])                           # 不知道这俩哪个好…
        self.assertTrue(u"开始" in response.content)

# coding: utf-8

import json
from datetime import timedelta
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from .memorize import __select_word as select_word
from memo.models import Vocabulary, UserProfile, Word, Note

# Create your tests here.
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
        u"""单词随机选择测试"""
        words = select_word(self.user)
        words_set = list(words)
        self.assertEqual(len(words_set), self.up.daily_words_amount)

        for w in words_set:                                                     # 将第一组单词添加到已掌握单词
            self.up.memorized_words.add(w)

        words = select_word(self.user)
        words_set = list(words)
        # 共 50 单词，已掌握 35 个，第二组只能选出 15 个
        self.assertEqual(len(words_set), 15)


class WordAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user("user", "", "password")
        self.word = Word(content="word", description="des_word")
        self.word.save()

    def test_word_api(self):
        u"""单词 API 测试"""
        response = self.client.get("/api/v1/word/"+str(self.word.id))           # 未登录
        self.assertEqual(response.status_code, 401)
        response = self.client.get("/api/v1/word/13213")
        self.assertEqual(response.status_code, 401)

        self.client.force_login(self.user)
        response = self.client.get("/api/v1/word/"+str(self.word.id))           # 正常查询
        self.assertEqual(response.status_code, 200)
        ret_data = { "success": True, "word": self.word.information() }
        self.assertEqual(json.loads(response.content), ret_data)

        response = self.client.get("/api/v1/word/13213")                        # 查询不存在的 ID
        self.assertEqual(response.status_code, 404)


    def test_search_api(self):
        u"""单词查询 API 测试"""
        response = self.client.get("/api/v1/search?word=word")
        self.assertEqual(response.status_code, 200)
        ret_data = { "success": True, "word": self.word.information() }
        self.assertEqual(json.loads(response.content), ret_data)

        response = self.client.get("/api/v1/search?word=test")
        self.assertEqual(response.status_code, 404)
        response = self.client.get("/api/v1/search?word=123")
        self.assertEqual(response.status_code, 404)


class NoteAPITests(TestCase):
    def setUp(self):
        self.maxDiff = None

        self.client = Client()
        self.user = User.objects.create_user("user", "", "password")
        self.word = Word(content="word", description="des_word")
        self.word.save()
        self.notes = []
        now = timezone.now()
        for i in range(13):
            note = Note(word=self.word,
                        content="Content %d"%i,
                        time=now+timedelta(0, -(20-i), 0),                      # 将所有 note 创建时间设置为开始测试之前
                        user=self.user)
            self.notes.append(note)
            note.save()
        self.notes.reverse()

    def test_unauthorized(self):
        u"""未登录返回 401"""
        response = self.client.get("/api/v1/word/%d/note"%self.word.id)
        self.assertEqual(response.status_code, 401)

    def test_word_not_found(self):
        u"""测试 404"""
        self.client.force_login(self.user)
        response = self.client.get("/api/v1/word/2/note")
        self.assertEqual(response.status_code, 404)

    def test_get(self):
        u"""GET 功能测试"""
        self.client.force_login(self.user)

        response = self.client.get("/api/v1/word/%d/note"%self.word.id)
        self.assertEqual(response.status_code, 200)
        ret_data = {
            "success": True,
            "note": [note.information() for note in self.notes[:10]]
            }
        self.assertEqual(json.loads(response.content), ret_data)

        response = self.client.get("/api/v1/word/%d/note?from=3&to=5"%self.word.id)
        self.assertEqual(response.status_code, 200)
        ret_data = {
            "success": True,
            "note": [note.information() for note in self.notes[3:5]]
            }
        self.assertEqual(json.loads(response.content), ret_data)

        response = self.client.get("/api/v1/word/%d/note?from=3&to=500"%self.word.id)
        self.assertEqual(response.status_code, 200)
        ret_data = {
            "success": True,
            "note": [note.information() for note in self.notes[3:]]
            }
        self.assertEqual(json.loads(response.content), ret_data)

        # 错误参数测试
        response = self.client.get("/api/v1/word/%d/note?from=-2&to=-1"%self.word.id)
        self.assertEqual(response.status_code, 400)
        response = self.client.get("/api/v1/word/%d/note?from=5&to=3"%self.word.id)
        self.assertEqual(response.status_code, 400)
        response = self.client.get("/api/v1/word/%d/note?from=abc&to=def"%self.word.id)
        self.assertEqual(response.status_code, 400)
        
    def test_post(self):
        u"""POST 功能测试"""
        self.client.force_login(self.user)

        response = self.client.post("/api/v1/word/%d/note"%self.word.id)        # 空参数
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)["reason"], "Empty content")

        response = self.client.post("/api/v1/word/%d/note"%self.word.id,
                { "content": "Testing note" }
            )
        self.assertEqual(response.status_code, 201)
        ret_data = {
            "success": True,
            "note": {
                "content": "Testing note",
                "user": self.user.username
            }
        }
        self.assertEqual(json.loads(response.content), ret_data)
        note = self.word.note_set.order_by("-time")[0]
        self.assertEqual(ret_data["note"], note.information())                  # 笔记已添加

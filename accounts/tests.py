# coding: utf-8

from django.test import TestCase
from django.contrib.auth.models import User, AnonymousUser
from django.test import Client
from memo.models import UserProfile


# Create your tests here.
class LoginTests(TestCase):
    u"""登录相关测试"""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user("user", "email", "password")

    def test_views_before_login(self):
        u"""登录前页面访问测试"""
        response = self.client.get("/accounts/login")
        self.assertTrue(u"登录到 SWord" in response.content)

        # 登陆后访问登录页面会跳转到主页
        response = self.client.get("/accounts/logout", follow=True)             # 登录前访问注销页面会跳转到主页
        self.assertEqual(response.redirect_chain, [("/", 302)])

    def test_views_after_login(self):
        u"""登录后页面访问测试"""
        self.client.force_login(self.user)
        response = self.client.get("/accounts/login", follow=True)
        self.assertEqual(response.redirect_chain, [("/", 302)])

    def test_login(self):
        u"""登录测试"""
        response = self.client.post("/accounts/login", {                        # 登录失败
                "username": "user",
                "password": "pass"
            })
        self.assertEqual(response.context["error"], "Invalid username or password (╯3╰)")

        response  = self.client.post("/accounts/login", {                       # 登陆成功，跳转
                "username": "user",
                "password": "password"
            }, follow=True)
        self.assertEqual(response.redirect_chain, [("/", 302)])
        self.assertEqual(response.context["user"], self.user)

    def test_logout(self):
        u"""注销测试"""
        self.client.force_login(self.user)
        response = self.client.get("/accounts/logout", follow=True)             # 注销，logout, 跳转
        self.assertEqual(response.redirect_chain, [("/", 302)])
        self.assertEqual(response.context["user"], AnonymousUser())


class RegisterTests(TestCase):
    u"""注册相关测试"""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user("user", "email", "password")

    def test_register_view(self):
        u"""注册页面访问测试"""
        response = self.client.get("/accounts/register")
        self.assertTrue(u"注册" in response.content)

        self.client.force_login(self.user)
        response = self.client.get("/accounts/register", follow=True)
        self.assertEqual(response.redirect_chain, [("/", 302)])

    def test_register_error(self):
        u"""注册错误判定测试"""
        response = self.client.post("/accounts/register", {
                "username": "test",
                "email": "a@a.com",
                "password": "password1",
                "repeat-password": "password2",
            })
        self.assertEqual(response.context["error"], "Password doesn't match!")

        response = self.client.post("/accounts/register", {
                "username": "test",
                "email": "a@a.com",
                "password": "pass",
                "repeat-password": "pass",
            })
        self.assertEqual(response.context["error"], "Password must be as least 6 characters!")

        response = self.client.post("/accounts/register", {
                "username": "test",
                "email": "a",
                "password": "password",
                "repeat-password": "password",
            })
        self.assertEqual(response.context["error"], "Email is not valid!")

        response = self.client.post("/accounts/register", {
                "username": "user",
                "email": "a@a.com",
                "password": "password",
                "repeat-password": "password",
            })
        self.assertEqual(response.context["error"], "User already exists!")

    def test_register_success(self):
        u"""注册功能测试"""
        response = self.client.post("/accounts/register", {
                "username": "test_user",
                "email": "test@test.com",
                "password": "password",
                "repeat-password": "password",
            }, follow=True)
        self.assertEqual(response.redirect_chain, [("/", 302)])                 # 注册成功跳转
        user = response.context["user"]
        self.assertEqual(user.username, "test_user")                            # 注册用户自动登录
        self.assertIsNotNone(user.userprofile)                                  # 自动添加用户信息 model

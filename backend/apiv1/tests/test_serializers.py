from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import localtime

from apiv1.models import Post, Category, Comment, Like
from apiv1.serializers import PostSerializer, UserSerializer, CategorySerializer, CommentSerializer


class TestUserSerializer(TestCase):
    """UserSerializerのテストクラス"""

    def test_input_valid(self):
        """入力データのバリデーション（OK） """

        # シリアライザの作成
        input_data = {
            "username": "user1",
            "email": 'user1@example.com',
            "password": "secret1",
        }
        serializer = UserSerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), True)

    def test_input_invalid_if_username_is_blank(self):
        """入力データのバリデーション（NG: usernameが空文字）"""

        # シリアライザを作成
        input_data = {
            "username": "",
            "email": 'user1@example.com',
            "password": "secret1",
        }
        serializer = UserSerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ['username'])
        self.assertCountEqual(
            [x.code for x in serializer.errors['username']], ['blank'])


class TestCategorySerializer(TestCase):
    """CategorySerializerのテストクラス"""

    def test_input_valid(self):
        """入力データのバリデーション（OK） """

        # シリアライザの作成
        input_data = {
            "name": '橋',
            "slug": 'bridge'
        }
        serializer = CategorySerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), True)

    def test_input_invalid_if_name_is_blank(self):
        """入力データのバリデーション（NG: nameが空文字）"""

        # シリアライザを作成
        input_data = {
            "name": '',
            "slug": 'bridge'
        }
        serializer = CategorySerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ['name'])
        self.assertCountEqual(
            [x.code for x in serializer.errors['name']], ['blank'])


class TestPostSerializer(TestCase):
    """PostSerializerのテストクラス"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user1 = get_user_model().objects.create(
            username="user1",
            email='user1@example.com',
            password="secret",
        )
        cls.category1 = Category.objects.create(
            name='橋',
            slug='bridge'
        )

    def test_input_valid(self):
        """入力データのバリデーション（OK） """

        # シリアライザの作成
        input_data = {
            "category": 1,
            "author_name": 1,
            "title": '飛騨トンネル',
            "content": 'あいうえお',
        }
        serializer = PostSerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), True)

    def test_input_invalid_if_title_is_blank(self):
        """入力データのバリデーション（NG: titleが空文字）"""

        # シリアライザを作成
        input_data = {
            "category": 1,
            "author_name": 1,
            "title": '',
            "content": 'あいうえお',
        }
        serializer = PostSerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ['title'])
        self.assertCountEqual(
            [x.code for x in serializer.errors['title']], ['blank'])


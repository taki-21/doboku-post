from django.contrib.auth import get_user_model
from django.utils.timezone import localtime
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apiv1.models import Category, Post

from unittest import TestCase
TestCase.maxDiff = None


class TestPostListCreateAPIView(APITestCase):
    """PostListCreateAPIViewのテストクラス"""

    TARGET_URL = '/api/v1/posts/'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(
            username="user",
            email='user@example.com',
            password="secret",
        )
        cls.category1 = Category.objects.create(
            name='橋',
            slug='bridge'
        )
        cls.category2 = Category.objects.create(
            name='ダム',
            slug='dam'
        )

    def test_create_success(self):
        """投稿モデルの登録APIへのPOSTリクエスト(正常系)"""

        # テストユーザーでログイン
        token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        # APIリクエストを実行
        params = {
            'category': self.category1.id,
            'author_name': self.user.id,
            'title': 'へのへのもへじ',
            'content': 'あいうえおかきくけこ',
        }
        response = self.client.post(self.TARGET_URL, params, format='json')
        # データベースの状態を検証
        self.assertEqual(Post.objects.count(), 1)
        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 201)
        post = Post.objects.get()
        user = get_user_model().objects.filter(username='user').values()[0]
        expected_json_dict = {
            'id': post.id,
            'category': post.category.id,
            'author': {
                'date_joined': str(
                    localtime(
                        user['date_joined'])).replace(
                    ' ',
                    'T'),
                'email': 'user@example.com',
                'first_name': '',
                'groups': [],
                'home_image': 'http://testserver/media/images/custom_user/home_image/home.png',
                'icon_image': 'http://testserver/media/images/custom_user/icon_image/default_icon.png',
                'id': 1,
                'introduction': None,
                'is_active': True,
                'is_staff': False,
                'is_superuser': False,
                'last_login': None,
                'last_name': '',
                'password': user['password'],
                'user_permissions': [],
                'username': 'user'},
            'title': post.title,
            'content': post.content,
            'published_at': str(
                localtime(
                    post.published_at)).replace(
                ' ',
                'T'),
            'comments_count': 0,
            'image': None,
            'likes_count': 0,
            'prefecture': post.prefecture,
            'address': post.address,
            'lat': post.lat,
            'lng': post.lat,
        }
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_create_bad_request(self):
        """投稿モデルの登録APIへのPOSTリクエスト（異常系：バリデーションNG）"""

        # APIリクエストを実行
        params = {
            'category': self.category1.id,
            'author_name': self.user.id,
            'title': '',
            'content': 'あいうえおかきくけこ',
        }
        response = self.client.post(self.TARGET_URL, params, format='json')

        # データベースの状態を検証
        self.assertEqual(Post.objects.count(), 0)
        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 400)

from django.contrib.auth import get_user_model
from django.utils.timezone import localtime
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apiv1.models import Category, Post

from unittest import TestCase
TestCase.maxDiff = None


# GET(正常系: 2, 異常系: 0)
# POST(正常系: 1, 異常系: 1)
class TestPostListCreateAPIView(APITestCase):
    """PostListCreateAPIViewのテストクラス"""

    TARGET_URL = '/api/v1/posts/'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create(
            username="user",
            email='user@example.com',
            password="secret",
        )
        cls.category1 = Category.objects.create(
            name='橋',
            slug='bridge'
        )
        cls.post1 = Post.objects.create(
            category=cls.category1,
            author=cls.user,
            title='飛騨トンネル',
            content='あいうえお',
        )

    def test_get_success(self):
        """投稿モデルの取得（一覧）・投稿APIへのGETリクエスト(正常系)"""

        # テストユーザーでログイン
        token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        # 投稿一覧をリクエスト
        response = self.client.get(self.TARGET_URL)

        # データベースの状態を検証
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Category.objects.count(), 1)

        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 200)

        # 予想されるレスポンスを作成
        post = Post.objects.get()
        user = get_user_model().objects.filter(username='user').values()[0]
        expected_json_dict = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [{
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
                'raw_image': None,
                'image': None,
                'likes_count': 0,
                'prefecture': post.prefecture,
                'address': post.address,
                'lat': post.lat,
                'lng': post.lat,
            }]}
        self.assertJSONEqual(response.content, expected_json_dict)
    def test_get_unauthorized_success(self):
        """投稿モデルの取得（一覧）・投稿APIへのGETリクエスト(正常系：ログインしていないユーザーでも閲覧可能)"""

        # テストユーザーでログインしない

        # 投稿一覧をリクエスト
        response = self.client.get(self.TARGET_URL)

        # データベースの状態を検証
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Category.objects.count(), 1)

        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 200)

        # 予想されるレスポンスを作成
        post = Post.objects.get()
        user = get_user_model().objects.filter(username='user').values()[0]
        expected_json_dict = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [{
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
                'raw_image': None,
                'image': None,
                'likes_count': 0,
                'prefecture': post.prefecture,
                'address': post.address,
                'lat': post.lat,
                'lng': post.lat,
            }]}
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_create_success(self):
        """投稿モデルの取得（一覧）・投稿APIへのPOSTリクエスト(正常系)"""

        # テストユーザーでログイン
        token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        # APIリクエストを実行
        params = {
            'category': self.category1.id,
            'author_name': self.user.id,
            'title': '明石海峡大橋',
            'content': 'かきくけこ',
        }
        response = self.client.post(self.TARGET_URL, params, format='json')
        # データベースの状態を検証
        self.assertEqual(Post.objects.count(), 2)
        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 201)
        post = Post.objects.get(id=2)
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
            'raw_image': None,
            'image': None,
            'likes_count': 0,
            'prefecture': post.prefecture,
            'address': post.address,
            'lat': post.lat,
            'lng': post.lat,
        }
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_create_bad_request(self):
        """投稿モデルの取得（一覧）・投稿APIへのPOSTリクエスト（異常系：バリデーションNG）"""

        # APIリクエストを実行
        params = {
            'category': self.category1.id,
            'author_name': self.user.id,
            'title': '',
            'content': 'あいうえおかきくけこ',
        }
        response = self.client.post(self.TARGET_URL, params, format='json')

        # データベースの状態を検証
        self.assertEqual(Post.objects.count(), 1)
        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 400)


# GET(正常系: 2, 異常系: 0)
# PATCH(正常系: 1, 異常系: 1)
# DELETE(正常系: 0, 異常系: 0)
class TestPostRetrieveUpdateDestroyAPIView(APITestCase):
    """PostRetrieveUpdateDestroyAPIViewのテストクラス"""

    TARGET_URL_WITH_PK = '/api/v1/posts/{}/'

    @ classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user1 = get_user_model().objects.create(
            username="user1",
            email='user1@example.com',
            password="secret1",
        )
        cls.user2 = get_user_model().objects.create(
            username="user2",
            email='user2@example.com',
            password="secret2",
        )
        cls.category1 = Category.objects.create(
            name='橋',
            slug='bridge'
        )
        cls.post1 = Post.objects.create(
            category=cls.category1,
            author=cls.user1,
            title='へのへのもへじ',
            content='あいうえおかきくけこ',
        )

    def test_get_success(self):
        """投稿モデルの取得（詳細）・更新・削除APIへのGETリクエスト(正常系)"""

        # テストユーザーでログイン(JWT認証)
        token = str(RefreshToken.for_user(self.user1).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        # 投稿詳細をリクエスト
        response = self.client.get(
            self.TARGET_URL_WITH_PK.format(self.post1.id))
        # データベースの状態を検証
        # self.assertEqual(Post.objects.count(), 1)
        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 200)
        post = Post.objects.get()
        user = get_user_model().objects.filter(username='user1').values()[0]
        expected_json_dict = {
            'id': post.id,
            'category': post.category.id,
            'author': {
                'date_joined': str(
                    localtime(
                        user['date_joined'])).replace(
                    ' ',
                    'T'),
                'email': 'user1@example.com',
                'first_name': '',
                'groups': [],
                'icon_image': 'http://testserver/media/images/custom_user/icon_image/default_icon.png',
                'id': 2,
                'introduction': None,
                'is_active': True,
                'is_staff': False,
                'is_superuser': False,
                'last_login': None,
                'last_name': '',
                'password': user['password'],
                'user_permissions': [],
                'username': 'user1'},
            'title': post.title,
            'content': post.content,
            'published_at': str(
                localtime(
                    post.published_at)).replace(
                ' ',
                'T'),
            'comments_count': 0,
            'raw_image': None,
            'image': None,
            'likes_count': 0,
            'prefecture': post.prefecture,
            'address': post.address,
            'lat': post.lat,
            'lng': post.lat,
        }
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_get_unauthorized_success(self):
        """投稿モデルの登録APIへのPOSTリクエスト（正常系：ログインしていないユーザーでも閲覧可能）"""

        response = self.client.get(
            self.TARGET_URL_WITH_PK.format(self.post1.id))
        # データベースの状態を検証
        # self.assertEqual(Post.objects.count(), 1)
        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 200)
        post = Post.objects.get()
        user = get_user_model().objects.filter(username='user1').values()[0]
        expected_json_dict = {
            'id': post.id,
            'category': post.category.id,
            'author': {
                'date_joined': str(
                    localtime(
                        user['date_joined'])).replace(
                    ' ',
                    'T'),
                'email': 'user1@example.com',
                'first_name': '',
                'groups': [],
                'icon_image': 'http://testserver/media/images/custom_user/icon_image/default_icon.png',
                'id': 2,
                'introduction': None,
                'is_active': True,
                'is_staff': False,
                'is_superuser': False,
                'last_login': None,
                'last_name': '',
                'password': user['password'],
                'user_permissions': [],
                'username': 'user1'},
            'title': post.title,
            'content': post.content,
            'published_at': str(
                localtime(
                    post.published_at)).replace(
                ' ',
                'T'),
            'comments_count': 0,
            'raw_image': None,
            'image': None,
            'likes_count': 0,
            'prefecture': post.prefecture,
            'address': post.address,
            'lat': post.lat,
            'lng': post.lat,
        }
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_patch_success(self):
        """投稿モデルの取得（詳細）・更新・削除APIへのPATCHリクエスト(正常系)"""

        # テストユーザーでログイン(JWT認証)
        token = str(RefreshToken.for_user(self.user1).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        params = {
            'id': self.post1.id,
            'category': self.category1.id,
            'author_name': self.user1.id,
            'title': 'あいうえお',
            'content': 'かきくけこ',
        }
        response = self.client.patch(
            self.TARGET_URL_WITH_PK.format(
                self.post1.id), params, format='json')
        # データベースの状態を検証
        # self.assertEqual(Post.objects.count(), 1)
        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 200)
        post = Post.objects.get()
        user = get_user_model().objects.filter(username='user1').values()[0]
        expected_json_dict = {
            'id': post.id,
            'category': post.category.id,
            'author': {
                'date_joined': str(
                    localtime(
                        user['date_joined'])).replace(
                    ' ',
                    'T'),
                'email': 'user1@example.com',
                'first_name': '',
                'groups': [],
                'icon_image': 'http://testserver/media/images/custom_user/icon_image/default_icon.png',
                'id': 2,
                'introduction': None,
                'is_active': True,
                'is_staff': False,
                'is_superuser': False,
                'last_login': None,
                'last_name': '',
                'password': user['password'],
                'user_permissions': [],
                'username': 'user1'},
            'title': post.title,
            'content': post.content,
            'published_at': str(
                localtime(
                    post.published_at)).replace(
                ' ',
                'T'),
            'comments_count': 0,
            'raw_image': None,
            'image': None,
            'likes_count': 0,
            'prefecture': post.prefecture,
            'address': post.address,
            'lat': post.lat,
            'lng': post.lat,
        }
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_patch_bad_request(self):
        """投稿モデルの登録APIへのPATCHリクエスト（異常系：バリデーションNG）"""

        # # APIリクエストを実行
        # post = Post.objects.create(
        #     category=self.category1,
        #     author=self.user1,
        #     title='へのへのもへじ',
        #     content='あいうえおかきくけこ',
        # )

        params = {
            'id': self.post1.id,
            'category': self.category1.id,
            'author_name': self.user1.id,
            'title': '',
            'content': 'かきくけこ',
        }
        response = self.client.patch(self.TARGET_URL_WITH_PK.format(
            self.post1.id), params, format='json')

        # データベースの状態を検証
        # self.assertEqual(Post.objects.count(), 1)
        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 400)


    # def test_patch_unauthorized_bad_request(self):
    #     """投稿モデルの登録APIへのPATCHリクエスト（異常系：投稿者とリクエストユーザーが異なるとき）"""

    #     # テストユーザーでログイン(JWT認証)
    #     token = str(RefreshToken.for_user(self.user2).access_token)
    #     self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    #     params = {
    #         'id': self.post1.id,
    #         'category': self.category1.id,
    #         'author_name': self.user2.id,
    #         'title': '瀬戸大橋',
    #         'content': 'かきくけこ',
    #     }
    #     response = self.client.patch(self.TARGET_URL_WITH_PK.format(
    #         self.post1.id), params, format='json')

    #     # レスポンスの内容を検証
    #     self.assertEqual(response.status_code, 400)

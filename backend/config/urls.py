from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', TemplateView.as_view(template_name='index.html')),
    path('api/v1/', include('apiv1.urls')),
    # re_path('', RedirectView.as_view(url='/')),
]

# 開発環境でのメディアファイルの配信設定
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)


# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
#     + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)


    # path('', include('apiv1.urls')),

    # # Djangoがあらかじめ提供しているurls.pyへ
    # path('accounts/', include('django.contrib.auth.urls')),

    # # 自分が作成したurls.pyへ
    # path('accounts/', include('accounts.urls')),

    # ## djangorestframework
    # # path('', include(router.urls)),

    # # 認証用のURL設定
    # path('auth/', obtain_jwt_token),

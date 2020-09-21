import os
# from django.conf import settings
from tempfile import SpooledTemporaryFile
from storages.backends.s3boto3 import S3Boto3Storage


# 画像は同ファイル名での上書きを許さない
class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False

    """
    https://github.com/matthewwithanm/django-imagekit/issues/391#issuecomment-275367006
    https://github.com/boto/boto3/issues/929
    https://github.com/matthewwithanm/django-imagekit/issues/391
    """

    def _save(self, name, content):
        """
        We create a clone of the content file as when this is passed to
        boto3 it wrongly closes the file upon upload where as the storage
        backend expects it to still be open
        """
        # Seek our content back to the start
        content.seek(0, os.SEEK_SET)

        # Create a temporary file that will write to disk after a specified
        # size. This file will be automatically deleted when closed by
        # boto3 or after exiting the `with` statement if the boto3 is fixed
        with SpooledTemporaryFile() as content_autoclose:

            # Write our original content into our copy that will be closed by
            # boto3
            content_autoclose.write(content.read())

            # Upload the object which will auto close the
            # content_autoclose instance
            return super(MediaStorage, self)._save(name, content_autoclose)

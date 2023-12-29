import os

from b2sdk.v1 import *
from flask import current_app

from utils.Utils import calc_md5, is_image, convert_to_webp


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class B2Uploader(metaclass=Singleton):
    def __init__(self):
        self.bucket = None
        application_key_id = current_app.config['B2_KEY_ID']
        application_key = current_app.config['B2_KEY']
        self.bucket_name = current_app.config['B2_BUCKET']
        self.host = current_app.config['B2_HOST']
        self.init_b2(application_key_id, application_key, self.bucket_name)

    def init_b2(self, application_key_id, application_key, bucket_name):
        info = InMemoryAccountInfo()
        b2_api = B2Api(info)
        b2_api.authorize_account("production", application_key_id, application_key)
        self.bucket = b2_api.get_bucket_by_name(bucket_name)

    def upload_file(self, file_to_upload):
        try:
            if not is_image(file_to_upload):
                print("只能上传图片文件")
                return
            # 转换为WebP格式
            file_to_upload = convert_to_webp(file_to_upload)
            if not file_to_upload:
                return

            md5_file_name = calc_md5(file_to_upload)
            sub_dir = md5_file_name[:2]
            b2_file_path = os.path.join('app', sub_dir, md5_file_name + '.webp')
            self.bucket.upload_local_file(
                local_file=file_to_upload,
                file_name=b2_file_path
            )
            print("文件成功上传到路径：" + b2_file_path)
            return os.path.join(self.host, b2_file_path)
        except Exception as e:
            print("上传文件过程中出错：" + str(e))

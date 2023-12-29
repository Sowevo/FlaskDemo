# coding=utf-8
import hashlib
import os

from PIL import Image


def is_image(file_path):
    """
    检查文件是否是图片
    :param file_path:
    :return:
    """
    # 简单的方式检查文件是否是图片，你可以根据需要添加更复杂的逻辑
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() in image_extensions


def convert_to_webp(input_path):
    """
    将图片转换为 WebP 格式
    :param input_path:
    :return:
    """
    try:
        _, file_extension = os.path.splitext(input_path)

        if file_extension.lower() == '.webp':
            # 如果已经是 WebP 格式，直接返回路径
            return input_path
        image = Image.open(input_path)
        output_path = os.path.splitext(input_path)[0] + '.webp'
        image.save(output_path, 'webp')
        return output_path
    except Exception as e:
        print("转换图片为WebP格式时出错：" + str(e))
        return input_path


def calc_md5(file_path):
    """
    计算文件的md5值
    :param file_path:
    :return:
    """
    with open(file_path, 'rb') as f:
        md5_obj = hashlib.md5()
        while True:
            data = f.read(8192)
            if not data:
                break
            md5_obj.update(data)
        hash_code = md5_obj.hexdigest()
    return str(hash_code).lower()

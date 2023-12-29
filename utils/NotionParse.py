# coding=utf-8
import csv
import os
import re
import shutil
import zipfile
from datetime import datetime

"""
处理notion导出的zip文件
"""

# 只考虑小写的UUID的正则表达式
pattern = re.compile(r' [a-f0-9]{32}')
key_mapping = {
    "一级区划": "state",
    "二级区划": "city",
    "国家": "country",
    "上次编辑时间": "last_update",
    "名字": "name",
    "图片": "images",
    "地图链接": "google_street_view_url",
    "坐标": "coordinates",
    "备注": "remarks",
    "网址": "google_map_url",
    "耗时": "duration",
    "舞台": "stage",
    "门票": "ticket",
    "附近车站": "station_url"
}


def unzip(zip_file, unzip_path):
    """
    解压zip文件
    并返回文件名的公共串
    """
    # 打开 zip 文件
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        # 解压到临时目录
        zip_ref.extractall(unzip_path)
    # 解压之后,如果文件和文件夹的个数大于3,则报个错
    if len(os.listdir(unzip_path)) > 3:
        raise Exception("导出文件格式不正确,请检查导出文件")
    remove_uuid_and_rename(unzip_path)
    return find_common_string(os.listdir(unzip_path))


def find_common_string(file_names):
    """
    查找多个文件名的公共串
    """
    # 使用 zip 函数将三个文件名同时迭代，获取每个位置上的字符
    for i, chars in enumerate(zip(*file_names)):
        # 如果这个位置上的字符不相同，则将公共串截断到这里
        if len(set(chars)) > 1:
            return file_names[0][:i]

    # 如果所有位置的字符都相同，则返回整个文件名
    return file_names[0]


def remove_uuid_and_rename(path):
    """
    递归遍历指定路径下的所有文件和文件夹
    如果文件名包含32位uuid，则去掉uuid并改名
    path: 要遍历的路径
    target_depth: 目标深度,从1开始
    current_depth: 当前深度,从1开始
    """
    # 遍历指定路径下的所有文件和文件夹
    for old_name in os.listdir(path):
        old_name_path = os.path.join(path, old_name)

        # 如果是文件夹且深度等于目标深度，那么对文件夹name处理
        if os.path.isdir(old_name_path) and pattern.search(old_name):
            # 如果文件名包含32位uuid，则去掉uuid并改名
            new_name = pattern.sub('', old_name)
            new_name_path = os.path.join(path, new_name)
            # 重命名文件或文件夹
            shutil.move(old_name_path, new_name_path)
            remove_uuid_and_rename(new_name_path)

        # 如果是文件名且深度等于目标深度，那么对文件name处理
        elif os.path.isfile(old_name_path) and pattern.search(old_name):
            # 如果文件名包含32位uuid，则去掉uuid并改名
            new_name = pattern.sub('', old_name)
            new_name_path = os.path.join(path, new_name)
            # 重命名文件或文件夹
            os.rename(old_name_path, new_name_path)


def read_csv(_work_dir, _file_id):
    """
    读取csv文件
    """
    # 打开csv文件
    csv_path = os.path.join(_work_dir, _file_id + '_all.csv')
    with open(csv_path, mode='r', encoding='utf-8-sig') as file:
        # 读取csv文件
        reader = csv.DictReader(file)
        # 转换为字典
        _result = [row for row in reader]
    return _result


def find_google_url(_db_id, _name, _work_dir):
    """
    从md文件中查找地图链接
    """
    file_path = os.path.join(_work_dir, _db_id, _name + '.md')
    if os.path.isfile(file_path):
        # 以读取模式打开文件，并将内容读取到变量 text 中
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        # 使用正则表达式找到地图的链接
        search = re.search(r'\(https://www.google.com/maps/embed.+?\)', text)
        if search is not None:  # 判断是否匹配到
            # 删除两边的括号
            return re.sub(r'[()]', '', search.group())
    return ''


def find_image(_db_id, _name, _work_dir):
    file_path = os.path.join(_work_dir, _db_id, _name)
    _file_list = []
    # os.walk() 会遍历指定的目录及其所有的子目录，
    # 这个函数返回的是一个生成器，它会生成包含目录路径，目录名列表，文件名列表的元组
    for dirpath, _, filenames in os.walk(file_path):
        for f in filenames:
            # 使用 os.path.join() 函数将目录路径和文件名组合成一个完整的文件路径
            full_path = os.path.join(dirpath, f)
            _file_list.append(full_path)
    return _file_list


def parse(zip_file):
    """
    解析notion导出的zip文件
    :param zip_file:
    :return:
    """
    # 解压目录
    unzip_path = os.path.join(os.path.dirname(zip_file), 'tmp')
    # 解压文件
    common_name = unzip(zip_file, unzip_path)
    # 读取csv文件
    result = read_csv(unzip_path, common_name)
    # 过滤掉没有名字的数据
    result = list(filter(lambda d: d['名字'], result))
    # 补充地图链接
    for e in result:
        embedded_url = find_google_url(common_name, e['名字'], unzip_path)
        file_list = find_image(common_name, e['名字'], unzip_path)
        e['地图链接'] = embedded_url
        e['图片'] = file_list
        e['上次编辑时间'] = datetime.strptime(e['上次编辑时间'], "%B %d, %Y %I:%M %p")
    # 换一下key
    change_key = [{key_mapping.get(k, k): v for k, v in row.items()} for row in result]
    return change_key

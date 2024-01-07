# coding=utf-8
import pandas as pd


def parse(save_path):
    """
    解析Excel文件
    Excel文件来自于: https://www.soumu.go.jp/denshijiti/code.html
    :param save_path:
    :return:
    """
    # 读取Excel文件
    df = pd.read_excel(save_path, sheet_name='R5.4.1現在の団体')
    df.drop('都道府県名\n（カナ）', axis=1, inplace=True)
    df.drop('市区町村名\n（カナ）', axis=1, inplace=True)
    df.drop('団体コード', axis=1, inplace=True)
    df.rename(columns={'都道府県名\n（漢字）': 'state', '市区町村名\n（漢字）': 'city', '観光地名\n（漢字）': 'name'},
              inplace=True)
    df['country'] = '日本'
    df['sort'] = 0
    return df.to_dict('records')

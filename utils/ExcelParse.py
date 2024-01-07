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
    df = pd.read_excel(save_path, sheet_name='R5.4.1現在の団体', dtype={'団体コード': str})
    df.drop('都道府県名\n（カナ）', axis=1, inplace=True)
    df.drop('市区町村名\n（カナ）', axis=1, inplace=True)
    df.rename(columns={
        '団体コード': 'code',
        '都道府県名\n（漢字）': 'state',
        '市区町村名\n（漢字）': 'city'
    }, inplace=True)
    # 追加一条数据,使用concat方法
    new_data = pd.DataFrame([{'code': '000000'}])
    df = pd.concat([df, new_data], ignore_index=True)
    # 所有的国家都是日本
    df['country'] = '日本'

    # 编码前面加上81...区号吧
    df['code'] = '81' + df['code']
    return df.to_dict('records')

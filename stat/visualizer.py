import aiosqlite
import asyncio
import json
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patheffects import withStroke
import numpy as np
import os
import pandas as pd
import requests
# import seaborn as sns
import sqlite3
import shutil
import time
from html2image import Html2Image
from io import BytesIO
from PIL import Image
import concurrent.futures

STAT_ROOT = os.path.dirname(os.path.abspath(__file__))
print(__file__, 'STAT_ROOT', STAT_ROOT)

class SetuVisualizer:
    def __init__(self):
        pass

    def init(self, setu_db_path, message_db_path, setu_root):
        self.setu_db_path = setu_db_path
        self.message_db_path = message_db_path
        self.setu_root = setu_root

    async def get_data(self):
        # 连接到SQLite数据库
        async with aiosqlite.connect(self.setu_db_path) as db:
            # 查询色图贡献榜 #'start of day'
            query = """
            SELECT user_id, COUNT(*) as count
            FROM setu
            WHERE type = 'recv' AND datetime(timestamp, 'localtime', '+8 hours') >= datetime('now', '-1 days')
            GROUP BY user_id
            ORDER BY count DESC
            LIMIT 10
            """
            # 使用aioodbc执行异步查询
            async with db.execute(query) as cursor:
                # 获取查询结果
                rows = await cursor.fetchall()
                # 如果查询结果为空，返回一个空的 DataFrame
                if not rows:
                    setu_recv_rank_df = pd.DataFrame(columns=['user_id', 'count'])
                else:
                    # 将结果转换为DataFrame
                    setu_recv_rank_df = pd.DataFrame(rows, columns = [column[0] for column in cursor.description])

            # 查询色图需求榜
            query = """
            SELECT user_id, COUNT(*) as count
            FROM setu
            WHERE type = 'send' AND datetime(timestamp, 'localtime', '+8 hours') >= datetime('now', '-1 days')
            GROUP BY user_id
            ORDER BY count DESC
            LIMIT 10
            """
            async with db.execute(query) as cursor:
                # 获取查询结果
                rows = await cursor.fetchall()
                # 如果查询结果为空，返回一个空的 DataFrame
                if not rows:
                    setu_send_rank_df = pd.DataFrame(columns=['user_id', 'count'])
                else:
                    # 将结果转换为DataFrame
                    setu_send_rank_df = pd.DataFrame(rows, columns = [column[0] for column in cursor.description])

            # 查询1日内type='recv'的记录，按group_id统计数量，取前10
            query = """
            SELECT group_id, COUNT(*) as count
            FROM setu
            WHERE type = 'recv' AND datetime(timestamp, 'localtime', '+8 hours') >= datetime('now', '-1 days')
            GROUP BY group_id
            ORDER BY count DESC
            LIMIT 10
            """
            async with db.execute(query) as cursor:
                # 获取查询结果
                rows = await cursor.fetchall()
                # 如果查询结果为空，返回一个空的 DataFrame
                if not rows:
                    setu_recv_group_rank_df = pd.DataFrame(columns=['group_id', 'count'])
                else:
                    # 将结果转换为DataFrame
                    setu_recv_group_rank_df = pd.DataFrame(rows, columns = [column[0] for column in cursor.description])

            # 查询1日内type='send'的记录，按group_id统计数量，取前10
            query = """
            SELECT group_id, COUNT(*) as count
            FROM setu
            WHERE type = 'send' AND datetime(timestamp, 'localtime', '+8 hours') >= datetime('now', '-1 days')
            GROUP BY group_id
            ORDER BY count DESC
            LIMIT 10
            """
            async with db.execute(query) as cursor:
                # 获取查询结果
                rows = await cursor.fetchall()
                # 如果查询结果为空，返回一个空的 DataFrame
                if not rows:
                    setu_send_group_rank_df = pd.DataFrame(columns=['group_id', 'count'])
                else:
                    # 将结果转换为DataFrame
                    setu_send_group_rank_df = pd.DataFrame(rows, columns = [column[0] for column in cursor.description])
            
            # 查询色图记录数量
            query = """
            SELECT strftime('%Y-%m-%d %H', timestamp, 'localtime') AS hour, type, COUNT(*) AS count
            FROM setu
            WHERE timestamp > datetime('now', '-1 day') AND (type = 'recv' OR type = 'send')
            GROUP BY hour, type
            ORDER BY hour
            """
            async with db.execute(query) as cursor:
                setu_count_df = pd.DataFrame(await cursor.fetchall())
                setu_count_df.columns = [column[0] for column in cursor.description]

            # 查询热门色图
            query = """
            SELECT file, COUNT(*) as count
            FROM setu
            WHERE type = 'recv' AND datetime(timestamp, 'localtime', '+8 hours') >= datetime('now', '-7 day')
            GROUP BY file
            ORDER BY count DESC
            LIMIT 4
            """
            async with db.execute(query) as cursor:
                pop_setu_df = pd.DataFrame(await cursor.fetchall())
                pop_setu_df.columns = [column[0] for column in cursor.description]
                
        return setu_recv_rank_df, setu_send_rank_df, setu_recv_group_rank_df, setu_send_group_rank_df, setu_count_df, pop_setu_df

    def get_user_image_url(self, id):
        # 头像尺寸：
        # s/spec	px
        # 1	    40 × 40
        # 2	    40 × 40
        # 3	    100 × 100
        # 640	350 × 350
        # 5	    640 × 640
        # 40	40 × 40
        # 100	100 × 100
        img_url = f"http://q1.qlogo.cn/g?b=qq&nk={id}&s=100"
        return img_url

    def get_group_image_url(self, id):
        img_url = f"http://p.qlogo.cn/gh/{id}/{id}/100"
        return img_url

    def write_js(self, data):
        # 将数据转换为JSON格式
        json_data = data.to_json(orient='records')
        # 将数据写入JS文件
        with open(self.js_path, 'w') as js_file:
            js_file.write(f'var data = {json_data};')

    async def do_visualize(self, show_group = False):
        # 准备数据
        setu_recv_rank_df, setu_send_rank_df, setu_recv_group_rank_df, setu_send_group_rank_df, setu_count_df, pop_setu_df = await self.get_data()
        # print(setu_recv_rank_df, setu_send_rank_df, setu_count_df, pop_setu_df)

        # 补齐10个
        for df in [setu_recv_rank_df, setu_send_rank_df, setu_recv_group_rank_df, setu_send_group_rank_df]:
            if len(df) < 10:
                # 创建一个新的DataFrame，其中所有值都是0，列数与原始DataFrame相同
                new_rows = pd.DataFrame('0', index=range(10 - len(df)), columns=df.columns)
                # 将新行添加到原始DataFrame
                df = pd.concat([df, new_rows], ignore_index=True)

        # 补齐4个
        if len(pop_setu_df) < 4:
            # 创建一个新的DataFrame，其中所有值都是0，列数与原始DataFrame相同
            new_rows = pd.DataFrame('', index=range(4 - len(pop_setu_df)), columns=pop_setu_df.columns)
            # 将新行添加到原始DataFrame
            pop_setu_df = pd.concat([pop_setu_df, new_rows], ignore_index=True)

        # 解析数据
        setu_recv_rank_df['image'] = setu_recv_rank_df['user_id'].apply(self.get_user_image_url)
        setu_send_rank_df['image'] = setu_send_rank_df['user_id'].apply(self.get_user_image_url)
        setu_recv_group_rank_df['image'] = setu_recv_group_rank_df['group_id'].apply(self.get_group_image_url)
        setu_send_group_rank_df['image'] = setu_send_group_rank_df['group_id'].apply(self.get_group_image_url)
        setu_recv_rank_dict = setu_recv_rank_df.to_dict(orient='list')
        setu_send_rank_dict = setu_send_rank_df.to_dict(orient='list')
        setu_recv_group_rank_dict = setu_recv_group_rank_df.to_dict(orient='list')
        setu_send_group_rank_dict = setu_send_group_rank_df.to_dict(orient='list')
        # 转换 'hour' 列的时间格式
        setu_count_df['hour'] = pd.to_datetime(setu_count_df['hour']).dt.strftime('%Y/%m/%d %H:%M:%S')
        setu_count_dict = {
            'send': [[row['hour'], row['count']] for index, row in setu_count_df[setu_count_df['type'] == 'send'].iterrows()],
            'recv': [[row['hour'], row['count']] for index, row in setu_count_df[setu_count_df['type'] == 'recv'].iterrows()]
        }
        # 复制所需图片到webpage/static/img目录
        for index, row in pop_setu_df.iterrows():
            # 使用 copy2() 函数复制文件并尽量保留元数据
            if len(row['file']) == 0:
                continue
            shutil.copy2(f"{self.setu_root}/data/image/{row['file']}", f"{STAT_ROOT}/webpage/static/img/{row['file']}")
        pop_setu_df['image'] = pop_setu_df['file'].apply(lambda file: f'static/img/{file}')
        pop_setu_dict = pop_setu_df.to_dict(orient='list')

        # 写出js
        #写入drawdata.js文件
        with open(f'{STAT_ROOT}/webpage/static/js/drawdata.js', 'w', encoding='utf-8') as f:
            f.write('todaySetuInc_data = ' + json.dumps(setu_count_dict) + ';\n\n')
            f.write('todaySetuGiveRank_data = ' + json.dumps(setu_recv_rank_dict) + ';\n\n')
            f.write('todaySetuGetRank_data = ' + json.dumps(setu_send_rank_dict) + ';\n\n')
            f.write('todaySetuGiveGroupRank_data = ' + json.dumps(setu_recv_group_rank_dict) + ';\n\n')
            f.write('todaySetuGetGroupRank_data = ' + json.dumps(setu_send_group_rank_dict) + ';\n\n')
            f.write('todayPopSetu_data = ' + json.dumps(pop_setu_dict) + ';\n\n')

        # 渲染图片
        webpage_url=f'file://{STAT_ROOT}/webpage/index.html'
        webpage_size = [1200, 2800]
        if show_group:
            webpage_url=f'file://{STAT_ROOT}/webpage/index_group.html'
            webpage_size[1] += 820
        
        print(webpage_url)
        time_stamp = int(time.time())
        out_file = f'{STAT_ROOT}/image/{time_stamp}.png'
        print(out_file)

        # for windows
        # hti = Html2Image(browser='chrome', browser_executable=r'C:\Users\fyr\AppData\Local\Chromium\Application\chrome.exe', size=webpage_size, 
        #                 custom_flags=['--virtual-time-budget=5000', '--hide-scrollbars'], 
        #                 output_path=f'{STAT_ROOT}/image'
        # )
        hti = Html2Image(browser='chrome', browser_executable=r'/E/liqi/chrome-headless-shell/linux-130.0.6723.58/chrome-headless-shell-linux64/chrome-headless-shell', size=webpage_size, 
                        custom_flags=['--virtual-time-budget=5000', '--hide-scrollbars'], 
                        output_path=f'{STAT_ROOT}/image'
        )
        hti.screenshot(url=webpage_url, save_as=f'{time_stamp}.png')

        return out_file

stat_visualizer = SetuVisualizer()

# 使用示例
if __name__ == '__main__':
    import os
    LOG_ROOT = os.path.dirname(os.path.abspath(__file__)) + '/../log'
    SETU_ROOT = os.path.dirname(os.path.abspath(__file__)) + '/../setu'
    print('LOG_ROOT', LOG_ROOT)
    print('SETU_ROOT', SETU_ROOT)
    visualizer = SetuVisualizer()
    visualizer.init(setu_db_path=LOG_ROOT + '/setu/db.sqlite', 
                    message_db_path=LOG_ROOT + '/message/db.sqlite',
                    setu_root=SETU_ROOT
                )

    asyncio.run(visualizer.do_visualize(show_group=True))
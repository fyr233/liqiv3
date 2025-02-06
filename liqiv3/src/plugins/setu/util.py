from nonebot.adapters.onebot.v11 import Message, MessageSegment

import time
import os
from collections import defaultdict, deque

# {'message':
# [
#     {
#         'type': 'node', 'data': {
#             'user_id': '1094950020', 'nickname': '哥们要玩mhwilds', 'content': [
#                 {
#                     'type': 'image', 'data': {'file': 'http://gchat.qpic.cn/gchatpic_new/1094950020/4174840486-3194097636-9A9EE08FA9646D3E2A4081F787927E20/0?term=255&is_origin=0', 'url': 'http://gchat.qpic.cn/gchatpic_new/1094950020/4174840486-3194097636-9A9EE08FA9646D3E2A4081F787927E20/0?term=255&is_origin=0', 'summary': '[图片]', 'subType': 0}
#                 }
#             ]
#         }
#     },
#     {'type': 'node', 'data': {'user_id': '1094950020', 'nickname': '哥们要玩mhwilds', 'content': [{'type': 'image', 'data': {'file': 'http://gchat.qpic.cn/gchatpic_new/1094950020/4174840486-3168076186-A618F9B00F6FA3FA4AE94231F57969D9/0?term=255&is_origin=0', 'url': 'http://gchat.qpic.cn/gchatpic_new/1094950020/4174840486-3168076186-A618F9B00F6FA3FA4AE94231F57969D9/0?term=255&is_origin=0', 'summary': '[图片]', 'subType': 0}}]}}, {'type': 'node', 'data': {'user_id': '1094950020', 'nickname': '哥们要玩mhwilds', 'content': [{'type': 'image', 'data': {'file': 'http://gchat.qpic.cn/gchatpic_new/1094950020/4174840486-2800888762-5AFC39EABEBF4676038E9A249A753A48/0?term=255&is_origin=0', 'url': 'http://gchat.qpic.cn/gchatpic_new/1094950020/4174840486-2800888762-5AFC39EABEBF4676038E9A249A753A48/0?term=255&is_origin=0', 'summary': '[图片]', 'subType': 0}}]}}, {'type': 'node', 'data': {'user_id': '1094950020', 'nickname': '哥 们要玩mhwilds', 'content': [{'type': 'image', 'data': {'file': 'http://gchat.qpic.cn/gchatpic_new/1094950020/4174840486-2255763370-7A06BF505B646ED20592C4910E0E0248/0?term=255&is_origin=0', 'url': 'http://gchat.qpic.cn/gchatpic_new/1094950020/4174840486-2255763370-7A06BF505B646ED20592C4910E0E0248/0?term=255&is_origin=0', 'summary': '[图片]', 'subType': 0}}]}}, {'type': 'node', 'data': {'user_id': '1094950020', 'nickname': '哥们要玩mhwilds', 'content': [{'type': 'image', 'data': {'file': 'http://gchat.qpic.cn/gchatpic_new/1094950020/4174840486-2546791960-36A38C608D59A7A67694F6CEC91E4CA4/0?term=255&is_origin=0', 'url': 'http://gchat.qpic.cn/gchatpic_new/1094950020/4174840486-2546791960-36A38C608D59A7A67694F6CEC91E4CA4/0?term=255&is_origin=0', 'summary': '[图片]', 'subType': 0}}]}}
# ]
# }

# QQNT llonebot
# {
#     'messages': [{
#         'self_id':
#         2799314467,
#         'user_id':
#         1094950020,
#         'time':
#         1719281511,
#         'message_id':
#         -2147483455,
#         'message_type':
#         'group',
#         'sender': {
#             'user_id': 1094950020,
#             'nickname': '杏',
#             'card': ''
#         },
#         'raw_message':
#         '[CQ:image,file=8BA93C6D0E56DA68648B1B8C6CCC7903.png,url=https://multimedia.nt.qq.com.cn/download?appid=1407&amp;fileid=CgoxMzI1Mjc1NDI5EhRzzz6JeDZ4fkJFyit-2RMMIKgVcxikpQYg_wooh5Pw9t31hgNQgL2jAQ&amp;spec=0&amp;rkey=CAISKKSBekjVG1fMPY36My6-Yz8OVgtaTMqSDkcdYAt3fLFhxGjFpnvwh5Q,file_size=103076]',
#         'font':
#         14,
#         'sub_type':
#         'normal',
#         'message_format':
#         'array',
#         'post_type':
#         'message',
#         'group_id':
#         284840486,
#         'content': [{
#             'data': {
#                 'file': '8BA93C6D0E56DA68648B1B8C6CCC7903.png',
#                 'url':
#                 'https://multimedia.nt.qq.com.cn/download?appid=1407&fileid=CgoxMzI1Mjc1NDI5EhRzzz6JeDZ4fkJFyit-2RMMIKgVcxikpQYg_wooh5Pw9t31hgNQgL2jAQ&spec=0&rkey=CAISKKSBekjVG1fMPY36My6-Yz8OVgtaTMqSDkcdYAt3fLFhxGjFpnvwh5Q',
#                 'file_size': '103076'
#             },
#             'type': 'image'
#         }]
#     }]
# }

# {
#     'messages': [{
#         'self_id':
#         2155679839,
#         'user_id':
#         1094950020,
#         'time':
#         1728304783,
#         'message_id':
#         -2147457671,
#         'message_type':
#         'group',
#         'sender': {
#             'user_id': 1094950020,
#             'nickname': 'non-dalao',
#             'card': ''
#         },
#         'raw_message':
#         '[CQ:file,file=4b37607d-d1d3-4461-aa43-269f1c7ed5e6.png,path=,file_id=/46f1667e-8512-11ef-b193-5254005c24aa,file_size=11074776]',
#         'font':
#         14,
#         'sub_type':
#         'normal',
#         'message_format':
#         'array',
#         'post_type':
#         'message',
#         'group_id':
#         284840486,
#         'content': [{
#             'data': {
#                 'file': '4b37607d-d1d3-4461-aa43-269f1c7ed5e6.png',
#                 'path': '',
#                 'file_id': '/46f1667e-8512-11ef-b193-5254005c24aa',
#                 'file_size': '11074776'
#             },
#             'type': 'file'
#         }]
#     }, {
#         'self_id':
#         2155679839,
#         'user_id':
#         1094950020,
#         'time':
#         1728320903,
#         'message_id':
#         -2147457656,
#         'message_type':
#         'group',
#         'sender': {
#             'user_id': 1094950020,
#             'nickname': 'mqy',
#             'card': ''
#         },
#         'raw_message':
#         '[CQ:image,file=A4EA72D6FF66313FD02610C256A30D86.jpg,subType=0,url=https://multimedia.nt.qq.com.cn/download?appid=1407&amp;fileid=CgoxMzI1Mjc1NDI5EhSjbnO00UK_owx6GwWUEQTdMYqDTxiDrQog_woon9HJj839iAMyBHByb2RQgL2jAQ&amp;spec=0&amp;rkey=CAISKKSBekjVG1fMQFRYCm7MIV1w-o_PSJs3iWPw5z8MSBRMobAWipiee0k,file_size=169603]',
#         'font':
#         14,
#         'sub_type':
#         'normal',
#         'message_format':
#         'array',
#         'post_type':
#         'message',
#         'group_id':
#         284840486,
#         'content': [{
#             'data': {
#                 'file': 'A4EA72D6FF66313FD02610C256A30D86.jpg',
#                 'subType': 0,
#                 'url':
#                 'https://multimedia.nt.qq.com.cn/download?appid=1407&fileid=CgoxMzI1Mjc1NDI5EhSjbnO00UK_owx6GwWUEQTdMYqDTxiDrQog_woon9HJj839iAMyBHByb2RQgL2jAQ&spec=0&rkey=CAISKKSBekjVG1fMQFRYCm7MIV1w-o_PSJs3iWPw5z8MSBRMobAWipiee0k',
#                 'file_size': '169603'
#             },
#             'type': 'image'
#         }]
#     }]
# }

def dict_to_message(forward_msg: dict) -> Message:
    if 'messages' in forward_msg:
        return dict_to_message_llonebot(forward_msg)
    else :
        return dict_to_message_lagrange(forward_msg)

def dict_to_message_lagrange(forward_msg: dict) -> Message:
    message = Message()
    for node in forward_msg['message']:
        for content in node['data']['content']:
            if content['type'] == 'text':
                message.append(MessageSegment.text(content['data']['text']))
            elif content['type'] == 'image':
                message.append(MessageSegment.image(content['data']['url']))
            elif content['type'] == 'at':
                message.append(MessageSegment.at(content['data']['qq']))
            elif content['type'] == 'reply':
                message.append(MessageSegment.reply(content['data']['id']))
            elif content['type'] == 'face':
                message.append(MessageSegment.face(content['data']['id']))
            elif content['type'] == 'forward':
                message.append(MessageSegment.forward(content['data']['id']))
            elif content['type'] == 'share':
                message.append(MessageSegment.share(content['data']['url']))
            elif content['type'] == 'json':
                message.append(MessageSegment.json(content['data']['data']))
            elif content['type'] == 'xml':
                message.append(MessageSegment.xml(content['data']['data']))
            # ... 添加其他类型的处理 ...
    return message

def dict_to_message_llonebot(forward_msg: dict) -> Message:
    message = Message()
    for node in forward_msg['messages']:
        for content in node['content']:
            if content['type'] == 'text':
                message.append(MessageSegment.text(content['data']['text']))
            elif content['type'] == 'image':
                message.append(MessageSegment.image(content['data']['url']))
            elif content['type'] == 'at':
                message.append(MessageSegment.at(content['data']['qq']))
            elif content['type'] == 'reply':
                message.append(MessageSegment.reply(content['data']['id']))
            elif content['type'] == 'face':
                message.append(MessageSegment.face(content['data']['id']))
            elif content['type'] == 'forward':
                message.append(MessageSegment.forward(content['data']['id']))
            elif content['type'] == 'share':
                message.append(MessageSegment.share(content['data']['url']))
            elif content['type'] == 'json':
                message.append(MessageSegment.json(content['data']['data']))
            elif content['type'] == 'xml':
                message.append(MessageSegment.xml(content['data']['data']))
            # ... 添加其他类型的处理 ...
    return message

# 限流
class RateLimiter:

    def __init__(self, window_sec, call_limit, CD_sec):
        self.N = window_sec  # 秒
        self.M = call_limit
        self.K = CD_sec  # 秒
        self.message_times = defaultdict(lambda: deque(maxlen=self.M))
        self.cooldown_until = defaultdict(lambda: 0)

    def is_allowed(self, group_id) -> bool:
        current_time = time.time()

        # 检查是否在冷却时间内
        if current_time < self.cooldown_until[group_id]:
            return False

        # 移除过期的时间戳
        while self.message_times[group_id] and self.message_times[group_id][
                0] < current_time - self.N:
            self.message_times[group_id].popleft()

        # 检查是否超过限制
        if len(self.message_times[group_id]) >= self.M:
            self.cooldown_until[group_id] = current_time + self.K
            return False

        # 记录当前消息时间
        self.message_times[group_id].append(current_time)
        return True


# 自动创建文件夹
def create_path_if_not_exists(path):
    """
    判断路径是否存在，如果不存在则自动创建该路径。

    :param path: 要检查并创建的路径字符串
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"路径 '{path}' 已创建。")
    else:
        print(f"路径 '{path}' 已存在。")

# 示例用法
#create_path_if_not_exists("/path/to/your/directory")
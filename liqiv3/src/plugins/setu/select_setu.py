from nonebot import get_plugin_config
from nonebot import on_command
from nonebot import on_message
from nonebot.adapters import Bot, Event
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, MessageSegment
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.matcher import Matcher

from PIL import Image
import requests
import json
import random
from datetime import datetime
import math
import re
import aiohttp
import aiofiles
import html
from io import BytesIO
import sys

sys.path.append('../setu')
sys.path.append('../log')
from vector_db import *
from log import *
from CLIP.run import SETU_ROOT
# from nsfw_image_detection.run import CheckOneImage as CheckOneImage_nsfw_image_detection
# from stable_diffusion_safety_checker.run import CheckOneImage as CheckOneImage_stable_diffusion_safety_checker
from CLIP.run import GetTextFeature

from .util import *
from config import *

rl = RateLimiter(30, 8, 60)

def weighted_random_pick(sorted_list, decay_param):
    # 计算权重列表
    weights = [math.exp(-decay_param * i) for i in range(len(sorted_list))]
    # 根据权重随机选择一个元素的索引
    index = random.choices(range(len(sorted_list)), weights=weights)[0]
    # 返回元素及其索引
    return (sorted_list[index], index)

async def handle_text(bot, event, message):
    reply_message = []
    debug_message = []

    # 时间限制
    # 获取当前的当地时间
    now = datetime.now()

    # 设置时间范围
    start_time = now.replace(hour=6, minute=0, second=0, microsecond=0)
    end_time = now.replace(hour=22, minute=0, second=0, microsecond=0)

    # 判断当前时间是否在这个范围内
    # if start_time <= now <= end_time:
    #     return reply_message, debug_message

    start_list = [
        'setu',
        '色图', '来张色图', '发张色图',
        '涩图', '来张涩图', '发张涩图',
        '来点',
    ]
    # 匹配触发词
    query_text = ''
    for msg_seg in message:
        if msg_seg.type == 'text':
            text = msg_seg.data['text']
            if any(text.startswith(start) for start in start_list):
                query_text = text
    if len(query_text) == 0:
        return reply_message, debug_message

    # 检查白名单
    if not str(event.group_id) in setu_config['white_list']:
        return reply_message, debug_message
    
    # 判断限流
    if not rl.is_allowed(event.group_id):
        limit_reply_list = [
            '歇会', '等下', '真没有了', '营养跟不上了', '冲太快啦', '慢点', '疼疼疼'
        ]
        reply_message = [random.choice(limit_reply_list)]
        return reply_message, debug_message
    
    file_name = ''
    # random mode
    if query_text in start_list:
        query_result = ivss.random_choose()
        file_name = query_result
        reply_message = [MessageSegment.image(file=f"{SETU_ROOT}/data/image/{query_result}")]

    # query mode
    elif query_text.startswith('来点') and len(query_text) > 2:
        query_text = query_text[2:]
        query_vector = GetTextFeature(query_text)
        query_result = ivss.search_by_vector(query_vector, n_results=101)
        random_id, random_id_index = weighted_random_pick(query_result['ids'][0], 0.046)

        # 详细debug信息
        if event.group_id == int(setu_config['debug_group']):
            ids = query_result['ids'][0][0::25]
            debug_message.append(query_text)
            for i, id in enumerate(ids):
                debug_message.append(MessageSegment.image(file=f"{SETU_ROOT}/data/image/{id}"))
                debug_message.append(f"{i*25} {query_result['distances'][0][i]:.4f}")
            debug_message.append(MessageSegment.image(file=f"{SETU_ROOT}/data/image/{random_id}"))
            debug_message.append(f"random{random_id_index} {query_result['distances'][0][random_id_index]:.4f}")
        else:
            reply_message = [
                query_text,
                MessageSegment.image(file=f"{SETU_ROOT}/data/image/{random_id}")
            ]
            # debug_message = [
            #     query_text,
            #     MessageSegment.image(file=f"{SETU_ROOT}/data/image/{random_id}"),
            #     f'{random_id_index} {query_result['distances'][0][random_id_index]:.4f}'
            # ]

    if len(reply_message) > 0:
        # log
        await logger.log_setu(type='send', user_id=event.user_id, group_id=event.group_id, file=file_name, message=str(msg_seg))
    
    return reply_message, debug_message

async def handle_select(bot, event, message):
    reply_message, debug_message = await handle_text(bot, event, message)

    # 发送至群debug_group
    if (len(debug_message) > 0):
        message = Message()
        for msg in debug_message:
            message += msg
        print(message)
        for msg_seg in message:
            print(msg_seg.data['file']) if 'file' in msg_seg.data else 0
        try:
            await bot.call_api("send_group_msg", group_id=int(setu_config['debug_group']), message=message)
            # 记录消息
            await logger.log_message(type='send_msg', user_id=event.self_id, group_id=event.group_id, content=str(message))
        except Exception as e:
            print(e)

    # 回复至源群
    if len(reply_message) > 0:
        message = Message()
        for msg in reply_message:
            message += msg
        print(message)
        try:
            await bot.call_api("send_group_msg", group_id=event.group_id, message=message)
            # 记录消息
            await logger.log_message(type='send_msg', user_id=event.self_id, group_id=event.group_id, content=str(message))
        except Exception as e:
            print(e)
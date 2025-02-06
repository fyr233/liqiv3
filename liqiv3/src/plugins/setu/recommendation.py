from nonebot import get_plugin_config
from nonebot import on_command
from nonebot import on_message
from nonebot import on_fullmatch
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
import re
import aiohttp
import aiofiles
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
import time
import torch
import sys
sys.path.append('../setu')
sys.path.append('../log')
sys.path.append('../config')
from vector_db import *
from log import *
from CLIP.run import SETU_ROOT

from .util import *
from config import *

_config_matcher = on_fullmatch(('开启相关推荐', '关闭相关推荐'), ignorecase=False)

@_config_matcher.handle()
async def handle_recommendation_config(bot: Bot, event: MessageEvent, state: T_State):
    reply_text = ''
    # 判断是否为群聊消息
    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id
        msg_text = event.message.extract_plain_text()
        if '开启' in msg_text:
            setu_config['recommendations'][str(group_id)] = True
            reply_text = '已开启相关推荐'
        elif '关闭' in msg_text:
            setu_config['recommendations'][str(group_id)] = False
            reply_text = '已关闭相关推荐'

    # 保存
    save_config(f'{CONFIG_ROOT}/setu/config.json', setu_config)

    # 回复至源群
    message = Message()
    message += MessageSegment.text(reply_text)
    try:
        await bot.call_api("send_group_msg", group_id=event.group_id, message=message)
        # 记录消息
        await logger.log_message(type='send_msg', user_id=event.self_id, group_id=event.group_id, content=str(message))
    except Exception as e:
        print(e)


async def handle_recommendation(bot, event, msg_seg, image_features, file_name):
    group_records = ivss_group.search_by_vector(query_vector=image_features.tolist(), n_results = 21)

    target_groups = []
    for group_id, distance in zip(group_records['ids'][0], group_records['distances'][0]):
        if distance < 0.1 and group_id != str(event.group_id):
            if group_id in setu_config['white_list'] and group_id in setu_config['recommendations'] and setu_config['recommendations'][group_id] == True:
                target_groups.append(group_id)

    if len(target_groups) == 0:
        return
    
    # target_groups = random.sample(target_groups, min(len(target_groups), 3))

    message = Message()
    message += MessageSegment.text('猜你喜欢')
    message += msg_seg

    for group in target_groups:
        if random.random() > 0.05:
            continue
        try:
            await bot.call_api("send_group_msg", group_id=int(group), message=message)
            # 记录消息
            await logger.log_message(type='send_msg', user_id=event.self_id, group_id=int(group), content=str(message))
            await logger.log_setu(type='send', user_id=-event.user_id, group_id=int(group), file=file_name, message=str(msg_seg))
        except Exception as e:
            print(e)
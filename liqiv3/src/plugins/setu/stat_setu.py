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

import sys
sys.path.append('../stat')
sys.path.append('../log')
from log import *
from CLIP.run import SETU_ROOT

from .util import *

from visualizer import *
stat_visualizer.init(setu_db_path=LOG_ROOT + '/setu/db.sqlite',
                    message_db_path=LOG_ROOT + '/message/db.sqlite',
                    setu_root=SETU_ROOT
                )


async def handle_stat(bot, event, message):
    start_list = [
        '统计',
    ]
    # 匹配触发词
    query_text = ''
    for msg_seg in message:
        if msg_seg.type == 'text':
            text = msg_seg.data['text']
            if any(text.startswith(start) for start in start_list):
                query_text = text
    if len(query_text) == 0:
        return

    stat_image_file = await stat_visualizer.do_visualize(show_group = True)

    # 回复至源群
    if True:
        message = Message()
        message += MessageSegment.image(file=stat_image_file)
        print(message)
        try:
            await bot.call_api("send_group_msg",
                               group_id=event.group_id,
                               message=message)
            # 记录消息
            await logger.log_message(type='send_msg',
                                     user_id=event.self_id,
                                     group_id=event.group_id,
                                     content=str(message))
        except Exception as e:
            print(e)
    

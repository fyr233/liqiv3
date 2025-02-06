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
import re
import aiohttp
import aiofiles
from io import BytesIO
import sys
sys.path.append('../setu')
sys.path.append('../log')
from vector_db import *
from log import *

from .plugin_config import Config
from .util import *
from .check_setu import *
from .select_setu import *
from .stat_setu import *
from .recommendation import *

create_path_if_not_exists(LOG_ROOT + '/message')
create_path_if_not_exists(LOG_ROOT + '/setu')

logger.init_db()
ivss.init(db_path=SETU_ROOT + '/CLIP/data/setudb_purify_240606', collection_name='setu')
ivss_group.init(db_path=SETU_ROOT + '/CLIP/data/setudb_group_240708', collection_name='setu')

__plugin_meta__ = PluginMetadata(
    name="setu",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

mb = on_command("mb")

@mb.handle()
async def handle_function(args: Message = CommandArg()):
    print('mb')
    await mb.finish("MB")

# 创建一个on_message事件响应器
match_all = on_message()

@match_all.handle()
async def handle_all(bot: Bot, event: MessageEvent, state: T_State):
    # 判断是否为群聊消息
    if isinstance(event, GroupMessageEvent):
        # 来点色图
        await handle_select(bot, event, event.message)

        # 识别色图
        await handle_check(bot, event, event.message)

        # 统计
        await handle_stat(bot, event, event.message)

        # 记录消息
        await logger.log_message(type='recv_msg', user_id=event.user_id, group_id=event.group_id, content=str(event.message))
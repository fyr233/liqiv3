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
import matplotlib.pyplot as plt
import numpy as np
import time
import torch
import sys
sys.path.append('../setu')
sys.path.append('../log')
from vector_db import *
from log import *
from CLIP.run import SETU_ROOT
# from nsfw_image_detection.run import CheckOneImage as CheckOneImage_nsfw_image_detection
# from stable_diffusion_safety_checker.run import CheckOneImage as CheckOneImage_stable_diffusion_safety_checker
from CLIP.run import CheckOneImage as CheckOneImage_CNCLIP

from .util import *
from .recommendation import *

create_path_if_not_exists(f'{SETU_ROOT}/CLIP/tmp')
create_path_if_not_exists(f"{SETU_ROOT}/data/image")

Classes_And_Prompts = [
    {'无暴力': '不含暴力的画面', '轻度暴力': '含轻度暴力的画面', '严重暴力': '含严重暴力的画面:'},
    {'无恶心': '不含恶心的画面', '恶心': '恶心'},
    {'实拍': '一张实拍照片', '插画': '一张插画', '截图': '一张屏幕截图', '表情': '一张聊天表情'},
    {'无血腥': '没有血腥、肢解等画面', '血腥': '含有血腥、肢解等画面'},
    {'高质量': '高质量', '低质量': '低质量'},
    {'高画质': '高画质', '低画质': '低画质'},
    {'高分辨率': '高分辨率', '低分辨率': '低分辨率'},
    {'水印': '有水印', '无水印': '无水印'},
    {'无裸露': '无裸露内容', '半裸': '含有半裸内容', '全裸': '含有全裸内容'},
    {'无sex': 'image', 'sex': 'sex'},
    {'无nude': 'image', 'nude': 'nude'},
    {'男': '男人', '女': '女人'},
    {'无性暗示': '不含挑逗或性暗示', '性暗示': '含有挑逗或性暗示'},
    {'二次元': '二次元', '三次元': '三次元'},
    {'美丽': '美丽', '丑陋': '丑陋'},
    {'不含文字': '不含文字或有少量文字', '文字': '含有大量文字'},
    # {'贫乳': 'small breasts', '中乳': 'medium breasts', '巨乳': ' big breasts'},
    {'无乳': '没有胸部画面', '贫乳': '包含贫乳画面', '巨乳': '包含巨乳画面'},
    {'成年': '成年', '青少年': '青少年', '幼年': '幼年'},
    {'单人': '图中只有一个人', '多人': '图中有多个人'},
    {'无性爱': '无性爱画面', '少量性爱': '少量性爱画面', '性爱': '露骨的性爱画面',}
]

async def handle_setu(img: Image):
    setu_score = 0.0# should be >0 if setu
    reply_text = ''
    debug_text = ''
    result = {}
    image_features = None

    # 尺寸太小
    width, height = img.size
    if min(width, height) < 400:
        return setu_score, reply_text, '', result, image_features

    # 调用色图识别
    # setu_score = CheckOneImage_nsfw_image_detection(img)
    # safety_result = CheckOneImage_stable_diffusion_safety_checker(img)
    # is_setu = len(safety_result[0]['bad_concepts']) > 0 or setu_score > 0.6
    # print(safety_result)
    result, image_features = CheckOneImage_CNCLIP(img, Classes_And_Prompts)
    # 根据结果分析
    if result['严重暴力'] > 0.7:
        setu_score -= 10.0
        debug_text += f"严重暴力{result['严重暴力']:.2f} "
    if result['恶心'] > 0.7:
        setu_score -= 10.0
        debug_text += f"恶心{result['恶心']:.2f} "
    if result['截图'] > 0.5:
        setu_score -= 10.0
        debug_text += f"截图{result['截图']:.2f} "
    if result['血腥'] > 0.5:
        setu_score -= 1.0
        debug_text += f"血腥{result['血腥']:.2f} "
    if result['表情'] > 0.8:
        setu_score -= 0.8
        debug_text += f"表情{result['表情']:.2f} "
    
    if result['丑陋'] > 0.8:
        setu_score -= 0.4
        debug_text += f"丑陋{result['丑陋']:.2f} "
    if result['低质量'] > 0.9:
        setu_score -= 0.2
        debug_text += f"低质量{result['低质量']:.2f} "
    if result['低画质'] > 0.7:
        setu_score -= 0.2
        debug_text += f"低画质{result['低画质']:.2f} "
    if result['实拍'] > 0.7:
        setu_score -= 0.2
        debug_text += f"实拍{result['实拍']:.2f} "
    if result['低分辨率'] > 0.8:
        setu_score -= 0.1
        debug_text += f"低分辨率{result['低分辨率']:.2f} "

    if result['男'] > 0.7:
        setu_score -= 0.1
        debug_text += f"男{result['男']:.2f} "
    if result['水印'] > 0.7:
        setu_score -= 0.1
        debug_text += f"水印{result['水印']:.2f} "
    if result['无裸露'] > 0.6:
        setu_score -= 0.1
        debug_text += f"无裸露{result['无裸露']:.2f} "
    if result['文字'] > 0.8:
        setu_score -= 0.1
        debug_text += f"文字{result['文字']:.2f} "
    if result['实拍'] > 0.8 and result['无性爱'] > 0.65:
        setu_score -= 0.1
        debug_text += f"实拍+无性爱{result['无性爱']:.2f} "
    if result['男'] > 0.8 and result['无性爱'] > 0.7:
        setu_score -= 0.1
        debug_text += f"男+无性爱{result['无性爱']:.2f} "
    if result['nude'] < 0.5 and result['sex'] < 0.5:
        setu_score -= 0.3
        debug_text += f"nude{result['nude']:.2f}+sex{result['sex']:.2f} "

    if result['nude'] > 0.8 and result['sex'] > 0.8:
        setu_score += 0.1
        debug_text += f"nude{result['nude']:.2f}+sex{result['sex']:.2f} "
    if result['性暗示'] > 0.7:
        setu_score += 0.1
        debug_text += f"性暗示{result['性暗示']:.2f} "
    if result['性爱'] > 0.7 or result['少量性爱'] > 0.7:
        setu_score += 0.1
        debug_text += f"性爱{result['性爱']:.2f} "
    if result['二次元'] > 0.8:
        setu_score += 0.1
        debug_text += f"二次元{result['二次元']:.2f} "
        # if result['实拍'] > 0.7:
        #     setu_score -= 0.1
        #     debug_text += f"二次元+实拍{result['实拍']:.2f} "
    if result['美丽'] > 0.8:
        setu_score += 0.1
        debug_text += f"美丽{result['美丽']:.2f} "

    if result['贫乳'] > 0.7:
        debug_text += f"贫乳{result['贫乳']:.2f} "
    if result['巨乳'] > 0.7:
        debug_text += f"巨乳{result['巨乳']:.2f} "

    # 距离评估
    distances = ivss.search_by_vector(query_vector=image_features.tolist(), n_results = 101)['distances'][0]
    if distances[10] > 0.2:
        setu_score -= 0.2
    elif distances[10] > 0.1:
        pass
    elif distances[10] > 0.08:
        setu_score += 0.2
    elif distances[10] > 0.07:
        setu_score += 0.4
    else:
        setu_score += 0.4
    debug_text += f'10距离{distances[10]:.3f} 100距离{distances[100]:.3f} '

    if setu_score > 1e-3:
        reply_text = '色！'

    return setu_score, reply_text, debug_text, result, image_features

async def handle_image(bot, event, msg_seg):
    reply_text = ''
    assert(msg_seg.type == 'image')
    print(msg_seg)
    # 获取图片URL
    # https://multimedia.nt.qq.com.cn/download?appid=1407&fileid=CgoxMDUwMjE0NzQ0EhTiMHN9rolWudYwB1Y5TnIL9vZdHxi27E0g_woopq_K_9aihgNQgL2jAQ&rkey=CAQSKAB6JWENi5LMQ5fTkroVdpJLlpXJsRhu2P9P4m_BFCjOeRNjMmiwocU&spec=0
    # http://gchat.qpic.cn/gchatpic_new/3439146599/3972581808-2982186922-C76FE876F2E7DC3BD9EF9E39159778B3/0?term=255&amp;is_origin=0
    # http://gchat.qpic.cn/gchatpic_new/632787458/799733244-2151378960-69CC05D365B05E711D83341DA4E86B64/0?term=255&amp;is_origin=0
    # http://gchat.qpic.cn/offpic_new/1094950020/0A99E52E87110216AF19B982B17621C4.jpg/0?term=255&amp;is_origin=0
    # https://multimedia.nt.qq.com.cn/download?appid=1407&amp;fileid=CgoxMzI1Mjc1NDI5EhR9-AWbu__hLLAheJOb_3PtAr9ATxjVqwYg_wooxcip--awhgNQgL2jAQ&amp;rkey=CAISKKSBekjVG1fMsjLiRNMnlS2Z9r6ky36DOKmQ8WsHydSyK87hRsBvJXE&amp;spec=0
    # https://gchat.qpic.cn/offpic_new/1094950020/{C15D75FB-BC22-E9EB-D132-45399A34ED44}.jpg/0?term=255&amp;is_origin=0
    # https://gchat.qpic.cn&amp;rkey=CAQSOAB6JWENi5LM9be562vZi4t3vFCsQlV0Wg812unX8zu7kPuk6jU_4f3ytQ_8W3yQiUsR6nkKjM-f&amp;spec=0
    img_url = msg_seg.data['url'] if 'url' in msg_seg.data else msg_seg.data['file']
    img_url = img_url.replace('https', 'http')

    img_file = msg_seg.data['file']

    # [CQ:image,file={5E3E770A-1CC4-24DD-951C-DAFC2A44FEDE}.jpg,subType=0,url=https://gchat.qpic.cn&amp;rkey=CAQSOAB6JWENi5LM9be562vZi4t3vFCsQlV0Wg812unX8zu7kPuk6jU_4f3ytQ_8W3yQiUsR6nkKjM-f&amp;spec=0,file_size=76235]
    img_fileid = str(random.random())
    try:
        if 'multimedia.nt.qq' in img_url:
            img_fileid = re.findall(r'fileid=(.+?)[&_-]', img_url)[0]
        elif 'gchat.qpic.cn/gchatpic_new' in img_url:
            img_fileid = re.findall(r'[/-]([\w\.]+)/0\?', img_url)[0]
        elif 'gchat.qpic.cn/offpic_new' in img_url:
            img_fileid = re.findall(r'[/-]([^/]+)/0\?', img_url)[0]
    except: # 没有匹配到
        # if 'gchat.qpic.cn' in img_url:
        #     img_fileid = img_file
        if len(img_file) > 0:
            img_fileid = img_file
    print('img_fileid', img_fileid, msg_seg.data['subType'] if 'subType' in msg_seg.data else '')

    async with aiohttp.ClientSession() as session:
        async with session.get(img_url) as response:
            # 确保响应成功
            if response.status == 200:
                img_data = BytesIO(await response.read())
                img = Image.open(img_data)
                img = img.convert('RGB')

                setu_score, reply_text, debug_text, raw_result, image_features = await handle_setu(img)
                print(raw_result)
                if image_features != None:
                    image_features = image_features.detach().to('cpu')

                # 发送至群debug_group
                if 'debug_group' in setu_config and len(setu_config['debug_group']) > 0:
                    if ((len(debug_text) > 0 and setu_score > -0.5) or event.group_id == int(setu_config['debug_group'])):
                        # 相关推荐
                        group_records = ivss_group.search_by_vector(query_vector=image_features.tolist(), n_results = 21)
                        
                        message = Message()
                        message += msg_seg
                        message += MessageSegment.text(
                            debug_text + f'色:{setu_score:.2}\n' + 
                            '\n'.join([f'{groupid} {distance:.3f}' for groupid, distance in zip(group_records['ids'][0], group_records['distances'][0])])
                        )
                        try:
                            await bot.call_api("send_group_msg", group_id=int(setu_config['debug_group']), message=message)
                            # 记录消息
                            await logger.log_message(type='send_msg', user_id=event.self_id, group_id=int(setu_config['debug_group']), content=str(message))
                        except Exception as e:
                            print(e)

                # 色图
                if setu_score > 1e-3:
                    # 使用aiofiles保存图片
                    # 根据图片格式动态设置文件扩展名
                    file_extension = img.format.lower() if img.format else 'png'
                    file_name = f'{img_fileid}.{file_extension}'
                    file_path = f"{SETU_ROOT}/data/image/{file_name}"
                    async with aiofiles.open(file_path, 'wb') as out_file:
                        await out_file.write(img_data.getvalue())

                    # 保存至vector db
                    ivss.insert_data(f'{file_name}', str(msg_seg), image_features.tolist())
                    # 更新ivss_group中的group平均特征值
                    record = ivss_group.get_data_by_id(id=str(event.group_id))
                    group_feature_avg = image_features.clone()
                    # print(record)
                    if len(record['ids']) > 0:
                        alpha = 0.9
                        old = torch.tensor(record['embeddings'][0])
                        group_feature_avg = alpha * old + (1 - alpha) * image_features
                        group_feature_avg = group_feature_avg / group_feature_avg.norm(p=2, dim=-1, keepdim=True)
                    ivss_group.collection.delete(ids=[str(event.group_id)])
                    ivss_group.insert_data(str(event.group_id), '', group_feature_avg.tolist())
                    # log
                    await logger.log_setu(type='recv', user_id=event.user_id, group_id=event.group_id, 
                                          file=file_name, message=str(msg_seg)
                                          )

                if setu_score > 0.3:
                    #相关推荐
                    await handle_recommendation(bot, event, msg_seg, image_features, file_name)
                    

                # 绘制直方图
                if (event.group_id == int(setu_config['debug_group'])):
                    results = ivss.search_by_vector(query_vector=image_features.tolist(), n_results = 2000)
                    plt.hist(results['distances'][0], bins=100, facecolor='blue', alpha=0.7)
                    plt.xlim((0, 0.5))
                    # plt.ylim((0, 2200))
                    plt.title('distribute')
                    plt.xlabel('cosine distance')
                    plt.ylabel('count')
                    file_name = f'{SETU_ROOT}/CLIP/tmp/{int(time.time())}.png'
                    plt.savefig(file_name)
                    plt.clf()
                    # 计算平均距离
                    mean_embedding = torch.tensor(results['embeddings'][0][:1000]).mean(dim=0)
                    mean_embedding = mean_embedding / np.linalg.norm(mean_embedding)
                    distanse_1000 = 1 - (mean_embedding * image_features).sum()
                    mean_embedding = torch.tensor(results['embeddings'][0][:100]).mean(dim=0)
                    mean_embedding = mean_embedding / np.linalg.norm(mean_embedding)
                    distanse_100 = 1 - (mean_embedding * image_features).sum()
                    message = Message()
                    message.append(MessageSegment.image(file=file_name))
                    message.append(f'100平均距离{distanse_100:.3f}\n1000平均距离{distanse_1000:.3f}')
                    try:
                        await bot.call_api("send_group_msg", group_id=int(setu_config['debug_group']), message=message)
                        # 记录消息
                        await logger.log_message(type='send_msg', user_id=event.self_id, group_id=int(setu_config['debug_group']), content=str(message))
                    except Exception as e:
                        print(e)
            else:
                print('获取图片失败', response.status)
    return reply_text

async def handle_forward_message(bot, event, messages):
    reply_text = ''
    # 遍历转发的消息段，寻找图片或进一步的转发消息
    for msg_seg in messages:
        if msg_seg.type == 'image':
            # 处理图片消息
            reply_text += await handle_image(bot, event, msg_seg)
        elif msg_seg.type == 'forward':
            # 如果有进一步的嵌套转发，递归处理
            print(msg_seg.data)
            try:
                forward_msg = await bot.call_api('get_forward_msg', id=msg_seg.data['id'])
                forward_msg = dict_to_message(forward_msg)
                reply_text += await handle_forward_message(bot, event, forward_msg)
            except Exception as e:
                print(e)
    return reply_text

async def handle_check(bot, event, message):
    reply_text = ''
    # 遍历消息段，寻找图片
    for msg_seg in event.message:
        if msg_seg.type == 'image':
            # 处理图片消息
            reply_text += await handle_image(bot, event, msg_seg)
        # 处理转发消息
        elif msg_seg.type == 'forward':
            print(msg_seg)
            print(msg_seg.data['id'])
            forward_msg = await bot.call_api('get_forward_msg', id=msg_seg.data['id'])
            print(forward_msg)

            forward_msg = dict_to_message(forward_msg)
            reply_text += await handle_forward_message(bot, event, forward_msg)
    # 回复至源群
    if (len(reply_text) > 0):
        message = Message()
        message += MessageSegment.text(reply_text)
        try:
            await bot.call_api("send_group_msg", group_id=event.group_id, message=message)
            # 记录消息
            await logger.log_message(type='send_msg', user_id=event.self_id, group_id=event.group_id, content=str(message))
        except Exception as e:
            print(e)
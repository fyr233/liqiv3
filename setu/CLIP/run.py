import torch
import torch.nn as nn
from PIL import Image
from typing import List, Dict, Tuple
import os
from transformers import CLIPProcessor, AutoProcessor, CLIPConfig, CLIPTextModel, PreTrainedModel, AutoTokenizer, CLIPModel, ChineseCLIPProcessor, ChineseCLIPModel

SETU_ROOT = os.path.dirname(os.path.abspath(__file__)) + '/..'
print(__file__, 'SETU_ROOT', SETU_ROOT)

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")
print(__file__, 'device', device)

cnclip_model = ChineseCLIPModel.from_pretrained(SETU_ROOT + "/CLIP/model/CN_CLIP").to(device)
cnclip_processor = ChineseCLIPProcessor.from_pretrained(SETU_ROOT + "/CLIP/model/CN_CLIP")

# 编译模型
# cnclip_model = torch.compile(cnclip_model)
# cnclip_processor = torch.compile(cnclip_processor)
# cnclip_model = torch.jit.script(cnclip_model)
# cnclip_processor = torch.jit.script(cnclip_processor)

def CheckOneImage(img: Image.Image, classes_and_prompts):
    result = {}
    with torch.no_grad():
        # 收集所有提示
        all_prompts = [prompt for group in classes_and_prompts for prompt in group.values()]

        # compute image feature
        inputs = cnclip_processor(images=img, return_tensors="pt").to(device)
        image_features = cnclip_model.get_image_features(**inputs)
        image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)  # normalize

        # compute text features for all prompts at once
        inputs = cnclip_processor(text=all_prompts, padding=True, return_tensors="pt").to(device)
        text_features = cnclip_model.get_text_features(**inputs)
        text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)  # normalize

        # 初始化类别组的起始索引
        start_idx = 0
        # 分组计算softmax
        for oneclassgroup in classes_and_prompts:
            keys = list(oneclassgroup.keys())
            group_size = len(keys)

            # 选择当前组对应的文本特征
            group_text_features = text_features[start_idx:start_idx + group_size]

            # 计算图像特征与当前组文本特征的相似度
            logits_per_image = torch.mm(image_features, group_text_features.t()) * 100
            probs = logits_per_image.softmax(dim=1)

            for j in range(len(keys)):
                result[keys[j]] = probs[:, j].item()

            # 更新起始索引以获取下一组的文本特征
            start_idx += group_size

    return result, image_features[0]

def CheckImages(imgs: List[Image.Image], classes_and_prompts) -> Tuple[List[Dict], List[List]]:
    results = [{} for img in imgs]
    with torch.no_grad():
        # 收集所有提示
        all_prompts = [prompt for group in classes_and_prompts for prompt in group.values()]

        # compute image feature
        inputs = cnclip_processor(images=imgs, return_tensors="pt").to(device)
        image_features = cnclip_model.get_image_features(**inputs)
        image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)  # normalize

        # compute text features for all prompts at once
        inputs = cnclip_processor(text=all_prompts, padding=True, return_tensors="pt").to(device)
        text_features = cnclip_model.get_text_features(**inputs)
        text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)  # normalize

        # 初始化类别组的起始索引
        start_idx = 0
        # 分组计算softmax
        for oneclassgroup in classes_and_prompts:
            keys = list(oneclassgroup.keys())
            group_size = len(keys)

            # 选择当前组对应的文本特征
            group_text_features = text_features[start_idx:start_idx + group_size]

            # 计算图像特征与当前组文本特征的相似度
            logits_per_image = torch.mm(image_features, group_text_features.t()) * 100
            probs = logits_per_image.softmax(dim=1)

            for i in range(len(imgs)):
                for j in range(len(keys)):
                    results[i][keys[j]] = probs[i, j].item()

            # 更新起始索引以获取下一组的文本特征
            start_idx += group_size

    return results, image_features.tolist()

def GetTextFeature(text):
    with torch.no_grad():
        # compute text features for all prompts at once
        inputs = cnclip_processor(text=text, padding=True, return_tensors="pt").to(device)
        text_features = cnclip_model.get_text_features(**inputs)
        text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)  # normalize

    return text_features[0].tolist()


if __name__ == '__main__':
    # model.save_pretrained(SETU_ROOT + "/CLIP/model/CN_CLIP")
    # processor.save_pretrained(SETU_ROOT + "/CLIP/model/CN_CLIP")

    imgFiles = os.listdir(SETU_ROOT + '/data/test')
    print(imgFiles)
    imgs = [
        Image.open(SETU_ROOT + "/data/test/" + i) for i in imgFiles
        if '.db' not in i
    ]

    Classes_And_Prompts = [
        {
            '无暴力': '不含暴力的画面',
            '轻度暴力': '含轻度暴力的画面',
            '严重暴力': '含严重暴力的画面:'
        },
        {
            '无恶心': '不含恶心的画面',
            '恶心': '恶心'
        },
        {
            '实拍': '一张实拍照片',
            '插画': '一张插画',
            '截图': '一张屏幕截图',
            '表情': '一张聊天表情'
        },
        # {'无血腥': '没有血腥、肢解等画面', '血腥': '含有血腥、肢解等画面'},
        # {'高质量': '高质量', '低质量': '低质量'},
        # {'高画质': '高画质', '低画质': '低画质'},
        # {'高分辨率': '高分辨率', '低分辨率': '低分辨率'},
        # {'水印': '有水印', '无水印': '无水印'},
        # {'无裸露': '无裸露内容', '半裸': '含有半裸内容', '全裸': '含有全裸内容'},
        # {'男': '男人', '女': '女人'},
        # {'无性暗示': '不含挑逗或性暗示', '性暗示': '含有挑逗或性暗示'},
        # {'二次元': '二次元', '三次元': '三次元'},
        # {'美丽': '美丽', '丑陋': '丑陋'},
        # {'不含文字': '不含文字或有少量文字', '文字': '含有大量文字'},
        # # {'贫乳': 'small breasts', '中乳': 'medium breasts', '巨乳': ' big breasts'},
        # {'无乳': '没有胸部画面', '贫乳': '包含贫乳画面', '巨乳': '包含巨乳画面'},
        # {'成年': '成年', '青少年': '青少年', '幼年': '幼年'},
        # {'单人': '图中只有一个人', '多人': '图中有多个人'},
        # {'无性爱': '无性爱画面', '少量性爱': '少量性爱画面', '性爱': '露骨的性爱画面',}
    ]
    results, image_features = CheckImages(imgs, Classes_And_Prompts)
    print(results)
    results, image_features = CheckOneImage(imgs[-1], Classes_And_Prompts)
    print(results)

    import requests
    url = "https://clip-cn-beijing.oss-cn-beijing.aliyuncs.com/pokemon.jpeg"
    image = Image.open(requests.get(url, stream=True).raw)
    texts = [{"杰尼龟": "杰尼龟", "妙蛙种子": "妙蛙种子", "小火龙": "小火龙", "皮卡丘": "皮卡丘"}]
    results, image_features = CheckImages([image], texts)
    print(results)

    # for img in imgs:
    #     with torch.no_grad():
    #         # compute image feature
    #         inputs = cnclip_processor(images=img, return_tensors="pt")
    #         image_features = cnclip_model.get_image_features(**inputs)
    #         image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)  # normalize

    #         for oneclass in classes:
    #             # compute text features
    #             inputs = cnclip_processor(text=oneclass, padding=True, return_tensors="pt")
    #             text_features = cnclip_model.get_text_features(**inputs)
    #             text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)  # normalize

    #             # scores
    #             logits_per_image = torch.mm(image_features, text_features.t()) * 100
    #             probs = logits_per_image.softmax(dim=1)

    #             for i in range(len(oneclass)):
    #                 print(f'{oneclass[i]}: {logits_per_image[:, i].item()}, {probs[:, i].item()}', end='  ')
    #             print('')

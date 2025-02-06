

# liqiv3


## 目录

- [简介](#简介)
- [项目结构](#项目结构)
- [环境搭建](#环境搭建)
- [运行项目](#运行项目)
- [配置文件](#配置文件)

---

## 简介

本项目是一个基于nonebot框架的qq机器人，目前有功能：

- 收色图：识别图片，保存色图。
- 发色图：从本地图库中发图。支持文图查询，但效果很烂。
- 相关推荐：基于CN_CLIP的图片特征向量，推送相似图片。
- 统计：统计发图排行榜和热门色图等等。

在此开源色图特征向量数据库，但不会开源图库本身。**注意**，因为不开源图库，如果直接按下文搭建环境并运行本项目，发图功能是无法使用的，请自行修改。

---

## 项目结构

（比较乱，忍一忍）

```
├── config/                  # 配置文件目录
│   ├── config.py            # 管理config
│   └── setu/                # setu配置
│       └── config.json      # 插件配置文件
│
├── liqiv3/                  # NoneBot 项目核心目录
│   ├── bot.py               # NoneBot 主程序入口
│   ├── pyproject.toml       # 项目元数据和依赖声明
│   ├── requirements.txt     # 依赖列表
│   └── src/                 # 插件源代码
│       └── plugins/
│           └── setu/        # 插件代码目录
│               ├── check_setu.py      # 检测模块
│               ├── __init__.py        # 插件入口
│               ├── plugin_config.py   # 插件配置
│               ├── recommendation.py  # 推荐功能
│               ├── select_setu.py     # 发图模块
│               ├── stat_setu.py       # 统计模块
│               └── util.py            # 工具模块
│
├── log/                     # 日志相关目录
│   ├── log.py               # 日志模块
│   ├── message/             # 消息日志数据库
│   │   └── db.sqlite        # SQLite 数据库文件
│   └── setu/                # 色图日志数据库
│       └── db.sqlite        # SQLite 数据库文件
│
├── setu/                    # 色图目录
│   ├── CLIP/                # CLIP 模型和数据
│   │   ├── data/            # 数据集
│   │   │   ├── setudb_group_240708/  # 群向量数据库
│   │   │   └── setudb_purify_240606/ # 色图向量数据库
│   │   ├── model/           # 模型文件
│   │   │   ├── CN_CLIP/     # 中文 CLIP 模型
│   │   ├── run.py           # CLIP 执行模块
│   │   └── tmp/             # 临时文件目录
│   ├── data/                # 色图数据
│   │   └── image/           # 色图
│   └── vector_db.py         # 向量数据库模块
│
├── stat/                    # 统计和可视化目录
│   ├── image/               # 输出的图片
│   ├── visualizer.py        # 数据可视化模块
│   └── webpage/             # 网页可视化
│       ├── index.html       # 主页
│       ├── index_group.html # 带群聊统计的主页
│       └── static/          # 静态资源
│           ├── css/         # CSS 文件
│           ├── img/         # 图片资源
│           └── js/          # JavaScript 文件
│
├── LICENSE                  # 项目许可证
└── README.md                # 项目说明文档
```

---

## 环境搭建

### 1. 安装 NoneBot 环境

本项目基于 [NoneBot](https://nonebot.dev/) 框架开发。在运行本项目之前，请先搭建基础环境（以 NoneBot 官方文档为准）。

#### 1.1 安装 `pipx` 和 `nb-cli`
NoneBot 推荐使用 `pipx` 安装脚手架工具 `nb-cli`：

```bash
# 安装 pipx
python -m pip install --user pipx
python -m pipx ensurepath

# 安装 nb-cli
pipx install nb-cli
```

---

### 2. 克隆本项目

```bash
git clone https://github.com/fyr233/liqiv3.git
cd liqiv3
```

---

### 3. 下载大文件

由于CN_CLIP模型和向量数据库较大，已通过网盘分享。请按照以下步骤下载并解压：

#### 3.1 下载文件

夸克网盘链接：https://pan.quark.cn/s/e91f0548b581
提取码：czz4
- **CN_CLIP.zip**（中文 CLIP 模型）
  该模型也可从huggingface下载，但文件结构似乎略有不同
  https://huggingface.co/OFA-Sys/chinese-clip-vit-base-patch16
- **setudb.zip**（色图向量数据库）用于增强色图识别的准确度。非必须，可自行修改代码跳过


#### 3.2 解压文件
将下载的文件解压到指定目录：

- **CN_CLIP.zip**：
  - 解压到 `setu/CLIP/model/CN_CLIP/`。
  - 解压后目录结构：
    ```
    setu/CLIP/model/CN_CLIP/
    ├── config.json
    ├── model.safetensors
    ├── preprocessor_config.json
    ├── special_tokens_map.json
    ├── tokenizer_config.json
    ├── tokenizer.json
    └── vocab.txt
    ```

- **setudb.zip**：
  - 解压到 `setu/CLIP/data/`。
  - 解压后目录结构：
    ```
    setu/CLIP/data/
    └── setudb_purify_240606/
    ```

---

### 4. 创建虚拟环境

使用 Python 内置的 `venv` 模块创建虚拟环境：

```bash
cd liqiv3 #在NoneBot 项目目录中
python -m venv .venv
```

---

### 5. 激活虚拟环境

- **Linux/macOS**：
  ```bash
  source .venv/bin/activate
  ```
- **Windows**：
  ```bash
  .\.venv\Scripts\activate
  ```

---

### 6. 安装依赖

安装项目所需的依赖：

```bash
pip install -r requirements.txt
```

---

## 运行项目

1. 确保虚拟环境已激活。
2. 运行 NoneBot 项目：
   ```bash
   cd liqiv3
   nb run
   ```

---

## 配置文件

以下是 `config/setu/config.json` 的示例文件，用于配置插件的推荐开关、白名单、debug群：

```json
{
    "recommendations": {
        "123456789": true
    },
    "white_list": [
        "123456789",
        "1234567890"
    ],
    "debug_group": "123456789"
}
```

---

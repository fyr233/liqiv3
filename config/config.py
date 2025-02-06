import json
import os


CONFIG_ROOT = os.path.dirname(os.path.abspath(__file__))
print(__file__, 'CONFIG_ROOT', CONFIG_ROOT)


# 读取配置文件
def load_config(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# 保存配置到文件
def save_config(file_path, config):
    with open(file_path, 'w') as f:
        json.dump(config, f, indent=4)

setu_config = load_config(f'{CONFIG_ROOT}/setu/config.json')
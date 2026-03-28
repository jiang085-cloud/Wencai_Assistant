import logging
import json
from pathlib import Path
from config import LOG_DIR

def setup_logger(name: str, log_file: str, level=logging.INFO):
    """配置日志"""
    log_file_path = Path(log_file)
    # 日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # 文件处理器
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    # 日志器
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

def read_json(file_path: Path) -> dict:
    """读取JSON文件"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(data: dict, file_path: Path):
    """写入JSON文件"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
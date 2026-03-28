import os
from pathlib import Path

# 项目根路径
PROJECT_ROOT = Path(__file__).parent.parent
# 数据路径
RAW_PDF_DIR = PROJECT_ROOT / "data" / "raw_pdf"
PROCESSED_JSON_DIR = PROJECT_ROOT / "data" / "processed_json"
LOG_DIR = Path(__file__).parent / "logs"
OUTPUT_DIR = Path(__file__).parent / "output"

# 创建目录
for dir_path in [RAW_PDF_DIR, PROCESSED_JSON_DIR, LOG_DIR, OUTPUT_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# 数据库配置
DB_TYPE = "sqlite"
SQLITE_DB_PATH = PROJECT_ROOT / "sql" / "finance.db"

# PDF解析配置
TARGET_PAGE = 0  
TABLE_SETTINGS = {  # PDF表格提取参数
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines",
    "explicit_vertical_lines": [],
    "explicit_horizontal_lines": []
}

# 字段映射（后续替换为赛题要求的字段）
# 格式：{PDF表格列名: 数据库表字段名}
FIELD_MAPPING = {
    "营业收入": "operating_revenue",
    "净利润": "net_profit",
    "总资产": "total_assets",
    # 补充其他字段...
}
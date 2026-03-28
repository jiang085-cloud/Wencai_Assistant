from config import FIELD_MAPPING
from utils import setup_logger

logger = setup_logger("data_validator", "logs/data_validator.log")

class FinanceDataValidator:
    def __init__(self, table_data: list):
        self.table_data = table_data  # 解析后的表格数据
        self.validated_data = {}
        self.error_list = []

    def check_data_completeness(self):
        """检查核心字段是否存在"""
        # 提取表格中所有列名
        if not self.table_data:
            self.error_list.append("表格数据为空")
            return False
        header_row = [cell.lower() for cell in self.table_data[0]]
        required_fields = [k.lower() for k in FIELD_MAPPING.keys()]
        missing_fields = [f for f in required_fields if f not in header_row]
        if missing_fields:
            self.error_list.append(f"缺失核心字段: {missing_fields}")
            logger.warning(f"数据校验失败：缺失字段 {missing_fields}")
            return False
        return True

    def check_numeric_consistency(self):
        """检查数值型字段的格式（非空/数字格式）"""
        # 示例：遍历表格，校验数值字段是否为数字
        header_row = [cell.lower() for cell in self.table_data[0]]
        numeric_fields = ["营业收入", "净利润", "总资产"]  # 替换为赛题数值字段
        for row in self.table_data[1:]:  # 跳过表头
            for idx, header in enumerate(header_row):
                if header in [f.lower() for f in numeric_fields]:
                    cell_value = row[idx].strip()
                    if not cell_value:
                        self.error_list.append(f"数值字段为空: {header}")
                    else:
                        # 去除千分位逗号，尝试转换为浮点数
                        try:
                            float(cell_value.replace(",", ""))
                        except ValueError:
                            self.error_list.append(f"数值格式错误: {header} = {cell_value}")
        if self.error_list:
            logger.warning(f"数值校验失败：{self.error_list}")
            return False
        return True

    def map_to_db_fields(self):
        """将PDF表格字段映射为数据库字段"""
        if not self.check_data_completeness() or not self.check_numeric_consistency():
            return None
        header_row = [cell.lower() for cell in self.table_data[0]]
        # 遍历表格行，映射字段
        for row in self.table_data[1:]:
            row_dict = {}
            for idx, header in enumerate(header_row):
                # 匹配字段映射
                original_field = [k for k in FIELD_MAPPING if k.lower() == header][0]
                db_field = FIELD_MAPPING[original_field]
                # 清洗数值
                cell_value = row[idx].strip().replace(",", "").replace("万元", "")
                # 转换为数值类型
                try:
                    row_dict[db_field] = float(cell_value) if cell_value else None
                except:
                    row_dict[db_field] = cell_value
            self.validated_data = row_dict
        logger.info("数据校验通过，完成字段映射")
        return self.validated_data

    def run_full_validation(self):
        """执行全量校验"""
        self.check_data_completeness()
        self.check_numeric_consistency()
        if not self.error_list:
            return self.map_to_db_fields()
        return None

if __name__ == "__main__":
    # 测试校验逻辑
    test_table = [
        ["营业收入", "净利润", "总资产"],
        ["100,000万元", "5,000万元", "200,000万元"]
    ]
    validator = FinanceDataValidator(test_table)
    validated_data = validator.run_full_validation()
    print("校验后数据:", validated_data)
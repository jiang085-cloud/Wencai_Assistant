from pdf_parser import PDFFinanceParser
from data_validator import FinanceDataValidator
from db_operations import FinanceDB
from utils import setup_logger

logger = setup_logger("main", "logs/main.log")

def main():
    # 1. 批量解析PDF
    parsed_results = PDFFinanceParser.batch_parse_pdfs()
    if not parsed_results:
        logger.warning("无PDF解析结果，退出流程")
        return

    # 2. 初始化数据库
    db = FinanceDB()
    db.create_tables()

    # 3. 遍历解析结果，校验+入库
    for result in parsed_results:
        if result["parsed_status"] != "success":
            logger.warning(f"跳过失败的PDF: {result['file_name']}")
            continue
        # 提取表格数据
        table_data = result["page_1_tables"]
        # 数据校验+字段映射
        validator = FinanceDataValidator(table_data)
        validated_data = validator.run_full_validation()
        if not validated_data:
            logger.warning(f"数据校验失败，跳过入库: {result['file_name']}")
            continue
        # 补充文件名（便于溯源）
        validated_data["file_name"] = result["file_name"]
        # 插入核心业绩表（其他表同理）
        db.insert_data("core_performance", validated_data)

    # 4. 关闭数据库连接
    db.close()
    logger.info("全量PDF解析→校验→入库流程完成")

if __name__ == "__main__":
    main()
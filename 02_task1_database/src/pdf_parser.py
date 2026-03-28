import pdfplumber
import json
from pathlib import Path
from config import RAW_PDF_DIR, PROCESSED_JSON_DIR, TARGET_PAGE, TABLE_SETTINGS
from utils import setup_logger

logger = setup_logger("pdf_parser", "logs/pdf_parser.log")

class PDFFinanceParser:
    def __init__(self, pdf_path: Path):
        self.pdf_path = pdf_path
        self.file_name = pdf_path.name
        self.parsed_data = {
            "file_name": self.file_name,
            "page_1_text": "",
            "page_1_tables": [],
            "parsed_status": "success"
        }

    def extract_page_content(self):
        """提取PDF第一页的文本和表格"""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                # 仅处理第一页
                page = pdf.pages[TARGET_PAGE]
                
                # 提取文本
                self.parsed_data["page_1_text"] = page.extract_text() or ""
                
                # 提取表格
                tables = page.extract_tables(TABLE_SETTINGS)
                # 过滤空表格，转换为结构化列表
                self.parsed_data["page_1_tables"] = [
                    [cell.strip() if cell else "" for cell in row] 
                    for table in tables 
                    for row in table 
                    if any(cell.strip() for cell in row)
                ]
            logger.info(f"成功解析PDF: {self.file_name}")
        except Exception as e:
            self.parsed_data["parsed_status"] = "failed"
            self.parsed_data["error_msg"] = str(e)
            logger.error(f"解析PDF失败 {self.file_name}: {e}")
        return self.parsed_data

    def save_to_json(self):
        """将解析结果保存为JSON（中间产物）"""
        json_path = PROCESSED_JSON_DIR / f"{self.file_name.replace('.pdf', '.json')}"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.parsed_data, f, ensure_ascii=False, indent=4)
        logger.info(f"JSON文件已保存: {json_path}")
        return json_path

    @classmethod
    def batch_parse_pdfs(cls):
        """批量解析raw_pdf目录下的所有PDF"""
        pdf_files = list(RAW_PDF_DIR.glob("*.pdf"))
        if not pdf_files:
            logger.warning("raw_pdf目录下无PDF文件")
            return []
        parsed_results = []
        for pdf_file in pdf_files:
            parser = cls(pdf_file)
            result = parser.extract_page_content()
            parser.save_to_json()
            parsed_results.append(result)
        return parsed_results

if __name__ == "__main__":
    # 测试单文件解析
    test_pdf = RAW_PDF_DIR / "测试财报.pdf"  
    if test_pdf.exists():
        parser = PDFFinanceParser(test_pdf)
        parser.extract_page_content()
        parser.save_to_json()
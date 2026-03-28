import sqlite3
from config import DB_TYPE, SQLITE_DB_PATH, MYSQL_CONFIG
from utils import setup_logger

logger = setup_logger("db_operations", "logs/db_operations.log")

class FinanceDB:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self._connect_db()

    def _connect_db(self):
        """连接数据库"""
        try:
            if DB_TYPE == "sqlite":
                self.conn = sqlite3.connect(SQLITE_DB_PATH)
                self.cursor = self.conn.cursor()
            logger.info(f"成功连接{DB_TYPE}数据库")
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            raise e

    def create_tables(self):
        """创建核心表"""
        # 核心业绩表（示例，后续替换为赛题要求的字段）
        core_performance_sql = """
        CREATE TABLE IF NOT EXISTS core_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name VARCHAR(255) NOT NULL,
            operating_revenue FLOAT,
            net_profit FLOAT,
            total_assets FLOAT,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        # 资产负债表/现金流量表/利润表 同理，补充对应的CREATE语句
        try:
            self.cursor.execute(core_performance_sql)
            self.conn.commit()
            logger.info("数据库表创建成功")
        except Exception as e:
            logger.error(f"建表失败: {e}")
            self.conn.rollback()

    def insert_data(self, table_name: str, data: dict):
        """插入数据到指定表"""
        if not data:
            logger.warning("无有效数据，跳过插入")
            return
        try:
            # 构造插入SQL
            fields = ", ".join(data.keys())
            placeholders = ", ".join(["%s"] * len(data)) if DB_TYPE == "mysql" else ", ".join(["?"] * len(data))
            sql = f"INSERT INTO {table_name} ({fields}) VALUES ({placeholders})"
            values = list(data.values())
            self.cursor.execute(sql, values)
            self.conn.commit()
            logger.info(f"成功插入{table_name}表 {len(data)} 条数据")
        except Exception as e:
            logger.error(f"插入数据失败: {e}")
            self.conn.rollback()

    def close(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    # 测试建表+插入
    db = FinanceDB()
    db.create_tables()
    test_data = {"file_name": "测试财报.pdf", "operating_revenue": 100000.0, "net_profit": 5000.0, "total_assets": 200000.0}
    db.insert_data("core_performance", test_data)
    db.close()
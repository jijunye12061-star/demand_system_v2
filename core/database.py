# core/database.py - 数据库连接管理

import sqlite3
import hashlib
from datetime import datetime
from contextlib import contextmanager

DB_PATH = "data.db"


@contextmanager
def get_connection():
    """获取数据库连接的上下文管理器"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def hash_password(password: str) -> str:
    """密码哈希"""
    return hashlib.sha256(password.encode()).hexdigest()


def init_db():
    """初始化数据库表"""
    with get_connection() as conn:
        cursor = conn.cursor()

        # 用户表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                display_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 需求表
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS requests (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT,
                        request_type TEXT,
                        research_scope TEXT,
                        org_name TEXT,
                        org_type TEXT,
                        sales_id INTEGER NOT NULL,
                        researcher_id INTEGER NOT NULL,
                        is_confidential INTEGER DEFAULT 0,
                        status TEXT DEFAULT 'pending',
                        result_note TEXT,
                        attachment_path TEXT,
                        work_hours REAL DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        completed_at TIMESTAMP,
                        FOREIGN KEY (sales_id) REFERENCES users(id),
                        FOREIGN KEY (researcher_id) REFERENCES users(id)
                    )
                ''')

        conn.commit()

        # 检查是否需要插入测试数据
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            _insert_test_data(conn)


def _insert_test_data(conn):
    """插入真实用户数据"""
    cursor = conn.cursor()
    # 格式: (username, password, role, display_name)
    # 密码统一默认为 123456
    default_pwd = hash_password("123456")

    users = [
        # 管理员
        ("admin", hash_password("admin123"), "admin", "管理员"),

        # --- 研究员 ---
        ("chenxiyu", default_pwd, "researcher", "陈熙雨"),
        ("liuyang", default_pwd, "researcher", "刘洋"),
        ("zhuhaotian", default_pwd, "researcher", "朱浩天"),

        # --- 销售 ---
        ("liyingsheng", default_pwd, "sales", "李迎圣"),
        ("sunyumeng", default_pwd, "sales", "孙宇萌"),
        ("liuqianyi", default_pwd, "sales", "刘仟一"),
        ("yaofang", default_pwd, "sales", "姚芳"),
        ("wuzehang", default_pwd, "sales", "吴泽航"),
        ("duanying", default_pwd, "sales", "段颖"),
        ("lidianzhe", default_pwd, "sales", "李典哲"),
        ("qiandingkun", default_pwd, "sales", "钱定坤"),
        ("guolijia", default_pwd, "sales", "郭力嘉"),
        ("niehuimin", default_pwd, "sales", "聂慧敏"),
        ("huqiyang", default_pwd, "sales", "胡奇洋"),
        ("jinchengjun", default_pwd, "sales", "金成俊"),
        ("huhuihui", default_pwd, "sales", "胡慧慧"),
        ("qianyibing", default_pwd, "sales", "钱一冰"),
    ]

    cursor.executemany(
        "INSERT INTO users (username, password, role, display_name) VALUES (?, ?, ?, ?)",
        users
    )
    conn.commit()
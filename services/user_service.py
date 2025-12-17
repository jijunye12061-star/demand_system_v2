# services/user_service.py - 用户相关业务逻辑

from core.database import get_connection, hash_password


def get_users_by_role(role: str) -> list:
    """获取指定角色的用户列表"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE role = ?", (role,))
        return [dict(row) for row in cursor.fetchall()]


def get_user_by_id(user_id: int) -> dict | None:
    """根据ID获取用户"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_all_users() -> list:
    """获取所有用户"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role, display_name FROM users ORDER BY role, id")
        return [dict(row) for row in cursor.fetchall()]


def create_user(username: str, password: str, role: str, display_name: str) -> tuple[bool, str]:
    """创建新用户"""
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password, role, display_name) VALUES (?, ?, ?, ?)",
                (username, hash_password(password), role, display_name)
            )
            conn.commit()
            return True, "创建成功"
        except Exception as e:
            return False, f"用户名已存在或创建失败: {e}"


def delete_user(user_id: int):
    """删除用户"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()


def update_user_password(user_id: int, new_password: str):
    """修改用户密码"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET password = ? WHERE id = ?",
            (hash_password(new_password), user_id)
        )
        conn.commit()

# services/request_service.py - 需求相关业务逻辑

from datetime import datetime
from core.database import get_connection


def create_request(
        title: str,
        description: str,
        request_type: str,
        research_scope: str,
        org_name: str,
        org_type: str,
        sales_id: int,
        researcher_id: int,
        is_confidential: bool = False
) -> int:
    """创建新需求"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO requests 
            (title, description, request_type, research_scope, org_name, org_type,
             sales_id, researcher_id, is_confidential)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, request_type, research_scope, org_name, org_type,
              sales_id, researcher_id, 1 if is_confidential else 0))
        conn.commit()
        return cursor.lastrowid


def _build_request_query(where_clause: str = "") -> str:
    """构建带用户名的需求查询SQL"""
    base = '''
        SELECT r.*, 
               s.display_name as sales_name,
               s.username as sales_username,
               res.display_name as researcher_name
        FROM requests r
        JOIN users s ON r.sales_id = s.id
        JOIN users res ON r.researcher_id = res.id
    '''
    if where_clause:
        base += f" WHERE {where_clause}"
    base += " ORDER BY r.created_at DESC"
    return base


def get_requests_by_sales(sales_id: int) -> list:
    """获取销售人员创建的需求"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(_build_request_query("r.sales_id = ?"), (sales_id,))
        return [dict(row) for row in cursor.fetchall()]


def get_requests_by_researcher(researcher_id: int) -> list:
    """获取分配给研究人员的需求"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(_build_request_query("r.researcher_id = ?"), (researcher_id,))
        return [dict(row) for row in cursor.fetchall()]


def get_visible_requests_for_user(user: dict) -> list:
    """
    获取用户可见的需求列表
    规则：
    - 公开需求(is_confidential=0)：所有销售和研究员可见
    - 保密需求(is_confidential=1)：仅创建者和被指派的研究员可见
    - 管理员：可见全部
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        if user['role'] == 'admin':
            cursor.execute(_build_request_query())
        else:
            query = _build_request_query('''
                (r.is_confidential = 0 
                 OR r.sales_id = ? 
                 OR r.researcher_id = ?)
            ''')
            cursor.execute(query, (user['id'], user['id']))

        return [dict(row) for row in cursor.fetchall()]


def get_public_requests() -> list:
    """获取所有公开需求"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(_build_request_query("r.is_confidential = 0"))
        return [dict(row) for row in cursor.fetchall()]


def get_all_requests() -> list:
    """获取所有需求（管理员用）"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(_build_request_query())
        return [dict(row) for row in cursor.fetchall()]


def get_request_by_id(request_id: int) -> dict | None:
    """根据ID获取需求详情"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(_build_request_query("r.id = ?"), (request_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def update_request_status(
        request_id: int,
        status: str,
        result_note: str = None,
        attachment_path: str = None,
        work_hours: float = None
):
    """更新需求状态"""
    with get_connection() as conn:
        cursor = conn.cursor()

        now = datetime.now()
        completed_at = now if status == 'completed' else None

        cursor.execute('''
            UPDATE requests 
            SET status = ?, result_note = ?, attachment_path = ?, 
                work_hours = ?, updated_at = ?, completed_at = ?
            WHERE id = ?
        ''', (status, result_note, attachment_path, work_hours or 0, now, completed_at, request_id))
        conn.commit()


def reassign_researcher(request_id: int, new_researcher_id: int):
    """重新分配研究员（管理员用）"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE requests 
            SET researcher_id = ?, updated_at = ?
            WHERE id = ?
        ''', (new_researcher_id, datetime.now(), request_id))
        conn.commit()


def toggle_confidential(request_id: int, is_confidential: bool):
    """切换需求的保密状态（管理员用）"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE requests 
            SET is_confidential = ?, updated_at = ?
            WHERE id = ?
        ''', (1 if is_confidential else 0, datetime.now(), request_id))
        conn.commit()


def get_researcher_today_pending_count(researcher_id: int) -> int:
    """获取研究员今日待完成数量（待处理+处理中）"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM requests 
            WHERE researcher_id = ? 
            AND status IN ('pending', 'in_progress')
            AND DATE(created_at) = DATE('now')
        ''', (researcher_id,))
        return cursor.fetchone()[0]


def can_user_view_request(user: dict, request: dict) -> bool:
    """检查用户是否有权限查看某个需求"""
    if user['role'] == 'admin':
        return True
    if not request['is_confidential']:
        return True
    return user['id'] in (request['sales_id'], request['researcher_id'])


def check_researcher_workload(researcher_id: int) -> tuple[bool, int]:
    """
    检查研究员当日工作量
    返回: (是否超载, 待完成数量)
    超载定义：当日待完成工作 >= 5项
    """
    count = get_researcher_today_pending_count(researcher_id)
    is_overloaded = count >= 5
    return is_overloaded, count
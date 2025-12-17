# services/stats_service.py - 统计相关业务逻辑

from datetime import datetime, timedelta
from core.database import get_connection


def get_date_range(period: str, custom_start=None, custom_end=None) -> tuple:
    """
    获取时间范围
    period: 'week' | 'month' | 'quarter' | 'year' | 'custom'
    """
    now = datetime.now()
    today = now.replace(hour=23, minute=59, second=59, microsecond=0)

    if period == 'week':
        start = today - timedelta(days=7)
    elif period == 'month':
        start = today - timedelta(days=30)
    elif period == 'quarter':
        start = today - timedelta(days=90)
    elif period == 'year':
        start = today.replace(month=1, day=1, hour=0, minute=0, second=0)
    elif period == 'custom' and custom_start and custom_end:
        start = datetime.combine(custom_start, datetime.min.time())
        today = datetime.combine(custom_end, datetime.max.time())
    else:
        start = today.replace(month=1, day=1, hour=0, minute=0, second=0)

    return start, today


def get_overview_stats(start_date=None, end_date=None) -> dict:
    """获取整体统计数据"""
    with get_connection() as conn:
        cursor = conn.cursor()

        if start_date and end_date:
            cursor.execute('''
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                    SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress,
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                    COALESCE(SUM(work_hours), 0) as total_hours
                FROM requests
                WHERE created_at >= ? AND created_at <= ?
            ''', (start_date, end_date))
        else:
            cursor.execute('''
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                    SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress,
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                    COALESCE(SUM(work_hours), 0) as total_hours
                FROM requests
            ''')

        row = cursor.fetchone()
        return dict(row) if row else {}


def get_stats_by_researcher(start_date=None, end_date=None) -> list:
    """按研究员统计"""
    with get_connection() as conn:
        cursor = conn.cursor()

        date_filter = ""
        params = []
        if start_date and end_date:
            date_filter = "WHERE r.completed_at >= ? AND r.completed_at <= ?"
            params = [start_date, end_date]

        cursor.execute(f'''
            SELECT 
                u.id,
                u.display_name as researcher_name,
                COUNT(*) as total,
                SUM(CASE WHEN r.status = 'completed' THEN 1 ELSE 0 END) as completed,
                COALESCE(SUM(r.work_hours), 0) as total_hours
            FROM requests r
            JOIN users u ON r.researcher_id = u.id
            {date_filter}
            GROUP BY r.researcher_id
            ORDER BY total_hours DESC
        ''', params)

        return [dict(row) for row in cursor.fetchall()]


def get_stats_by_request_type(start_date=None, end_date=None) -> list:
    """按需求类型统计"""
    with get_connection() as conn:
        cursor = conn.cursor()

        date_filter = ""
        params = []
        if start_date and end_date:
            date_filter = "WHERE completed_at >= ? AND completed_at <= ?"
            params = [start_date, end_date]

        cursor.execute(f'''
            SELECT 
                request_type,
                COUNT(*) as total,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                COALESCE(SUM(work_hours), 0) as total_hours
            FROM requests
            {date_filter}
            GROUP BY request_type
            ORDER BY total DESC
        ''', params)

        return [dict(row) for row in cursor.fetchall()]


def get_stats_by_org(start_date=None, end_date=None) -> list:
    """按客户/机构统计"""
    with get_connection() as conn:
        cursor = conn.cursor()

        date_filter = ""
        params = []
        if start_date and end_date:
            date_filter = "WHERE completed_at >= ? AND completed_at <= ?"
            params = [start_date, end_date]

        cursor.execute(f'''
            SELECT 
                org_name,
                org_type,
                COUNT(*) as total,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                COALESCE(SUM(work_hours), 0) as total_hours
            FROM requests
            {date_filter}
            GROUP BY org_name
            ORDER BY total DESC
        ''', params)

        return [dict(row) for row in cursor.fetchall()]


def get_researcher_detail_stats(researcher_id: int, start_date=None, end_date=None) -> dict:
    """获取单个研究员的详细统计"""
    with get_connection() as conn:
        cursor = conn.cursor()

        date_filter = "WHERE r.researcher_id = ?"
        params = [researcher_id]
        if start_date and end_date:
            date_filter += " AND r.completed_at >= ? AND r.completed_at <= ?"
            params.extend([start_date, end_date])

        # 总体统计
        cursor.execute(f'''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN r.status = 'completed' THEN 1 ELSE 0 END) as completed,
                COALESCE(SUM(r.work_hours), 0) as total_hours
            FROM requests r
            {date_filter}
        ''', params)
        overview = dict(cursor.fetchone())

        # 按需求类型
        cursor.execute(f'''
            SELECT 
                request_type,
                COUNT(*) as total,
                COALESCE(SUM(work_hours), 0) as hours
            FROM requests r
            {date_filter}
            GROUP BY request_type
        ''', params)
        by_type = [dict(row) for row in cursor.fetchall()]

        # 按客户
        cursor.execute(f'''
            SELECT 
                org_name,
                org_type,
                COUNT(*) as total,
                COALESCE(SUM(work_hours), 0) as hours
            FROM requests r
            {date_filter}
            GROUP BY org_name
        ''', params)
        by_org = [dict(row) for row in cursor.fetchall()]

        return {
            'overview': overview,
            'by_type': by_type,
            'by_org': by_org
        }


def get_org_detail_stats(org_name: str, start_date=None, end_date=None) -> dict:
    """获取单个客户的详细统计"""
    with get_connection() as conn:
        cursor = conn.cursor()

        date_filter = "WHERE r.org_name = ?"
        params = [org_name]
        if start_date and end_date:
            date_filter += " AND r.completed_at >= ? AND r.completed_at <= ?"
            params.extend([start_date, end_date])

        # 总体统计
        cursor.execute(f'''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN r.status = 'completed' THEN 1 ELSE 0 END) as completed,
                COALESCE(SUM(r.work_hours), 0) as total_hours
            FROM requests r
            {date_filter}
        ''', params)
        overview = dict(cursor.fetchone())

        # 按需求类型
        cursor.execute(f'''
            SELECT 
                request_type,
                COUNT(*) as total,
                COALESCE(SUM(work_hours), 0) as hours
            FROM requests r
            {date_filter}
            GROUP BY request_type
        ''', params)
        by_type = [dict(row) for row in cursor.fetchall()]

        # 按研究员
        cursor.execute(f'''
            SELECT 
                u.display_name as researcher_name,
                COUNT(*) as total,
                COALESCE(SUM(r.work_hours), 0) as hours
            FROM requests r
            JOIN users u ON r.researcher_id = u.id
            {date_filter}
            GROUP BY r.researcher_id
        ''', params)
        by_researcher = [dict(row) for row in cursor.fetchall()]

        # 需求列表
        cursor.execute(f'''
            SELECT r.*, 
                   s.display_name as sales_name,
                   res.display_name as researcher_name
            FROM requests r
            JOIN users s ON r.sales_id = s.id
            JOIN users res ON r.researcher_id = res.id
            {date_filter}
            ORDER BY r.created_at DESC
        ''', params)
        requests = [dict(row) for row in cursor.fetchall()]

        return {
            'overview': overview,
            'by_type': by_type,
            'by_researcher': by_researcher,
            'requests': requests
        }


def get_request_type_detail_stats(request_type: str, start_date=None, end_date=None) -> dict:
    """获取单个需求类型的详细统计"""
    with get_connection() as conn:
        cursor = conn.cursor()

        date_filter = "WHERE r.request_type = ?"
        params = [request_type]
        if start_date and end_date:
            date_filter += " AND r.completed_at >= ? AND r.completed_at <= ?"
            params.extend([start_date, end_date])

        # 总体统计
        cursor.execute(f'''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN r.status = 'completed' THEN 1 ELSE 0 END) as completed,
                COALESCE(SUM(r.work_hours), 0) as total_hours
            FROM requests r
            {date_filter}
        ''', params)
        overview = dict(cursor.fetchone())

        # 按研究员
        cursor.execute(f'''
            SELECT 
                u.display_name as researcher_name,
                COUNT(*) as total,
                COALESCE(SUM(r.work_hours), 0) as hours
            FROM requests r
            JOIN users u ON r.researcher_id = u.id
            {date_filter}
            GROUP BY r.researcher_id
        ''', params)
        by_researcher = [dict(row) for row in cursor.fetchall()]

        # 按客户
        cursor.execute(f'''
            SELECT 
                org_name,
                org_type,
                COUNT(*) as total,
                COALESCE(SUM(work_hours), 0) as hours
            FROM requests r
            {date_filter}
            GROUP BY org_name
        ''', params)
        by_org = [dict(row) for row in cursor.fetchall()]

        return {
            'overview': overview,
            'by_researcher': by_researcher,
            'by_org': by_org
        }


def get_user_stats(user_id: int, role: str) -> dict:
    """获取单个用户的统计数据（兼容旧代码）"""
    with get_connection() as conn:
        cursor = conn.cursor()

        field = 'sales_id' if role == 'sales' else 'researcher_id'

        cursor.execute(f'''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed
            FROM requests
            WHERE {field} = ?
        ''', (user_id,))

        row = cursor.fetchone()
        return dict(row) if row else {'total': 0, 'pending': 0, 'in_progress': 0, 'completed': 0}
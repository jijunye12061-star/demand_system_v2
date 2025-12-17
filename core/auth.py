# core/auth.py - 认证逻辑

import streamlit as st
from core.database import get_connection, hash_password


def check_login() -> bool:
    """检查用户是否已登录"""
    return st.session_state.get('user') is not None


def get_current_user() -> dict | None:
    """获取当前登录用户"""
    return st.session_state.get('user')


def require_login():
    """要求登录，未登录则显示提示并停止"""
    if not check_login():
        st.warning("请先登录")
        st.stop()
    return get_current_user()


def require_role(allowed_roles: list):
    """要求特定角色"""
    user = require_login()
    if user['role'] not in allowed_roles:
        st.error("您没有权限访问此页面")
        st.stop()
    return user


def login(username: str, password: str) -> bool:
    """登录验证"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, hash_password(password))
        )
        row = cursor.fetchone()
        if row:
            st.session_state['user'] = dict(row)
            return True
    return False


def logout():
    """登出"""
    if 'user' in st.session_state:
        del st.session_state['user']

# components/filters.py - 筛选器组件

import streamlit as st
from config import REQUEST_STATUS, REQUEST_TYPES, RESEARCH_SCOPES


def render_status_filter(key: str = "status_filter") -> str | None:
    """渲染状态筛选器，返回选中的状态值或None（全部）"""
    options = ["全部"] + [v['label'] for v in REQUEST_STATUS.values()]
    selected = st.selectbox("状态筛选", options, key=key)
    
    if selected == "全部":
        return None
    
    # 反向查找status key
    for k, v in REQUEST_STATUS.items():
        if v['label'] == selected:
            return k
    return None


def render_request_type_filter(key: str = "type_filter") -> str | None:
    """渲染需求类型筛选器"""
    options = ["全部"] + REQUEST_TYPES
    selected = st.selectbox("需求类型", options, key=key)
    return None if selected == "全部" else selected


def render_research_scope_filter(key: str = "scope_filter") -> str | None:
    """渲染研究范畴筛选器"""
    options = ["全部"] + RESEARCH_SCOPES
    selected = st.selectbox("研究范畴", options, key=key)
    return None if selected == "全部" else selected


def render_keyword_filter(key: str = "keyword_filter") -> str:
    """渲染关键词搜索框"""
    return st.text_input("搜索（事项名称/机构）", key=key)


def apply_filters(requests: list, filters: dict) -> list:
    """
    应用筛选条件
    filters: {
        'status': str | None,
        'request_type': str | None,
        'research_scope': str | None,
        'keyword': str,
    }
    """
    result = requests
    
    if filters.get('status'):
        result = [r for r in result if r['status'] == filters['status']]
    
    if filters.get('request_type'):
        result = [r for r in result if r.get('request_type') == filters['request_type']]
    
    if filters.get('research_scope'):
        result = [r for r in result if r.get('research_scope') == filters['research_scope']]
    
    if filters.get('keyword'):
        kw = filters['keyword'].lower()
        result = [r for r in result 
                  if kw in (r.get('title') or '').lower() 
                  or kw in (r.get('org_name') or '').lower()]
    
    return result

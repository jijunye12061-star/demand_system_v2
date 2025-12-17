# components/cards.py - 统计卡片组件

import streamlit as st


def render_stats_cards(stats: dict):
    """渲染统计卡片（总数、待处理、处理中、已完成）"""
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 总需求", stats.get('total', 0))
    col2.metric("🟡 待处理", stats.get('pending', 0))
    col3.metric("🔵 处理中", stats.get('in_progress', 0))
    col4.metric("🟢 已完成", stats.get('completed', 0))


def render_mini_stats(stats: dict):
    """渲染迷你统计（3列）"""
    col1, col2, col3 = st.columns(3)
    col1.metric("待处理", stats.get('pending', 0))
    col2.metric("处理中", stats.get('in_progress', 0))
    col3.metric("已完成", stats.get('completed', 0))


def render_dimension_stats(title: str, data: dict, show_completion_rate: bool = False):
    """
    渲染维度统计
    data: {name: {'total': x, 'completed': y, ...}, ...}
    """
    st.subheader(title)
    if not data:
        st.info("暂无数据")
        return
    
    for name, info in data.items():
        if show_completion_rate and info.get('total', 0) > 0:
            rate = info.get('completed', 0) / info['total'] * 100
            st.write(f"- **{name}**: {info['total']} 条 (完成率 {rate:.0f}%)")
        else:
            st.write(f"- **{name}**: {info.get('total', 0)} 条")

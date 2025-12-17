# components/admin_views.py - 管理端视图组件

import streamlit as st
import pandas as pd
from io import BytesIO


def render_time_selector(key_prefix: str = "") -> tuple:
    """
    渲染时间选择器
    返回: (start_date, end_date)
    """
    from services.stats_service import get_date_range

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        period = st.selectbox(
            "时间范围",
            ["week", "month", "quarter", "year", "custom"],
            format_func=lambda x: {
                "week": "近一周",
                "month": "近一月",
                "quarter": "近一季",
                "year": "今年以来",
                "custom": "自定义"
            }[x],
            key=f"{key_prefix}period"
        )

    custom_start, custom_end = None, None
    if period == "custom":
        with col2:
            custom_start = st.date_input("开始日期", key=f"{key_prefix}start")
        with col3:
            custom_end = st.date_input("结束日期", key=f"{key_prefix}end")

    start_date, end_date = get_date_range(period, custom_start, custom_end)
    return start_date, end_date


def render_overview_cards(stats: dict):
    """渲染总览卡片"""
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("📊 总需求", stats.get('total', 0))
    col2.metric("🟡 待处理", stats.get('pending', 0))
    col3.metric("🔵 处理中", stats.get('in_progress', 0))
    col4.metric("🟢 已完成", stats.get('completed', 0))
    col5.metric("⏱️ 总工时", f"{stats.get('total_hours', 0):.1f}H")


def render_researcher_table(data: list):
    """渲染研究员统计表格"""
    if not data:
        st.info("暂无数据")
        return

    df = pd.DataFrame(data)
    df = df.rename(columns={
        'researcher_name': '研究员',
        'total': '需求数',
        'completed': '已完成',
        'total_hours': '工时(H)'
    })
    df['工时(H)'] = df['工时(H)'].round(1)
    st.dataframe(df[['研究员', '需求数', '已完成', '工时(H)']], use_container_width=True, hide_index=True)


def render_request_type_table(data: list):
    """渲染需求类型统计表格"""
    if not data:
        st.info("暂无数据")
        return

    df = pd.DataFrame(data)
    df = df.rename(columns={
        'request_type': '需求类型',
        'total': '需求数',
        'completed': '已完成',
        'total_hours': '工时(H)'
    })
    df['工时(H)'] = df['工时(H)'].round(1)
    st.dataframe(df[['需求类型', '需求数', '已完成', '工时(H)']], use_container_width=True, hide_index=True)


def render_org_table(data: list):
    """渲染客户统计表格"""
    if not data:
        st.info("暂无数据")
        return

    df = pd.DataFrame(data)
    df = df.rename(columns={
        'org_name': '客户名称',
        'org_type': '客户类型',
        'total': '需求数',
        'completed': '已完成',
        'total_hours': '工时(H)'
    })
    df['工时(H)'] = df['工时(H)'].round(1)
    st.dataframe(df[['客户名称', '客户类型', '需求数', '已完成', '工时(H)']], use_container_width=True, hide_index=True)


def render_pie_chart(data: list, name_field: str, value_field: str, title: str, key: str = None):
    """渲染饼图"""
    if not data:
        return

    import plotly.express as px

    df = pd.DataFrame(data)
    if df.empty or df[value_field].sum() == 0:
        st.info("暂无数据")
        return

    fig = px.pie(df, names=name_field, values=value_field, title=title)
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True, key=key or f"pie_{title}")


def render_bar_chart(data: list, x_field: str, y_field: str, title: str, key: str = None):
    """渲染柱状图"""
    if not data:
        return

    import plotly.express as px

    df = pd.DataFrame(data)
    if df.empty:
        st.info("暂无数据")
        return

    fig = px.bar(df, x=x_field, y=y_field, title=title)
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True, key=key or f"bar_{title}")


def render_detail_table(data: list, title: str):
    """渲染详情小表格"""
    if not data:
        st.info("暂无数据")
        return

    st.write(f"**{title}**")
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_request_list_simple(requests: list):
    """渲染简化的需求列表"""
    from config import get_status_display

    if not requests:
        st.info("暂无需求")
        return

    for req in requests:
        status_display = get_status_display(req['status'])
        with st.expander(f"**{req['title']}** - {status_display}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**需求类型:** {req.get('request_type') or '-'}")
                st.write(f"**研究范畴:** {req.get('research_scope') or '-'}")
                st.write(f"**工时:** {req.get('work_hours', 0)}H")
            with col2:
                st.write(f"**销售:** {req.get('sales_name', '-')}")
                st.write(f"**研究员:** {req.get('researcher_name', '-')}")
                st.write(f"**创建时间:** {req.get('created_at', '-')}")

            if req.get('description'):
                st.write(f"**描述:** {req['description']}")
            if req.get('result_note'):
                st.write(f"**处理结果:** {req['result_note']}")


def export_to_excel(data: list, filename: str = "导出数据.xlsx") -> bytes:
    """导出数据到Excel"""
    from config import get_org_type

    export_data = []
    for r in data:
        export_data.append({
            '事项': r.get('title', ''),
            '研究范畴': r.get('research_scope', ''),
            '需求类型': r.get('request_type', ''),
            '承接研究员': r.get('researcher_name', ''),
            '客户名': r.get('org_name', ''),
            '客户类型': r.get('org_type') or get_org_type(r.get('org_name', '')),
            '对应销售': r.get('sales_name', ''),
            '工时消耗（H）': r.get('work_hours', 0),
        })

    df = pd.DataFrame(export_data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='需求明细')
    return output.getvalue()
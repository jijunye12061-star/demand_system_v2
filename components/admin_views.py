# components/admin_views.py - 管理端视图组件（优化版）

import streamlit as st
import pandas as pd
from io import BytesIO


def render_time_selector(key_prefix: str = "") -> tuple:
    """渲染时间选择器，返回: (start_date, end_date)"""
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
        confidential_badge = "🔒 " if req.get('is_confidential') else ""

        with st.expander(f"{confidential_badge}**{req['title']}** - {status_display}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**需求类型:** {req.get('request_type') or '-'}")
                st.write(f"**研究范畴:** {req.get('research_scope') or '-'}")
                st.write(f"**工时:** {req.get('work_hours', 0):.1f}H")
            with col2:
                st.write(f"**销售:** {req.get('sales_name', '-')}")
                st.write(f"**研究员:** {req.get('researcher_name', '-')}")
                st.write(f"**创建时间:** {req.get('created_at', '-')}")

            if req.get('description'):
                st.write(f"**描述:** {req['description']}")
            if req.get('result_note'):
                st.write(f"**处理结果:** {req['result_note']}")


# ============================================================
# 优化后的多时间维度表格
# ============================================================

def render_multi_period_researcher_table(data: list):
    """
    渲染研究员多时间维度统计表格（优化版）
    - 过滤空数据行
    - 总计行固定在底部，不参与排序
    - 数值格式统一为一位小数
    """
    if not data:
        st.info("暂无数据")
        return

    df = pd.DataFrame(data)

    # 过滤掉所有列都为0的行（空白研究员）
    numeric_cols = ['today_count', 'today_hours', 'week_count', 'week_hours',
                    'month_count', 'month_hours', 'quarter_hours', 'year_hours']
    df = df[df[numeric_cols].sum(axis=1) > 0]

    if df.empty:
        st.info("暂无数据")
        return

    # 重命名列
    df = df.rename(columns={
        'researcher_name': '研究员',
        'today_count': '今日需求',
        'today_hours': '今日工时',
        'week_count': '本周需求',
        'week_hours': '本周工时',
        'month_count': '当月需求',
        'month_hours': '当月工时',
        'quarter_hours': '当季工时',
        'year_hours': '今年工时'
    })

    # 格式化为一位小数
    for col in ['今日工时', '本周工时', '当月工时', '当季工时', '今年工时']:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f"{x:.1f}")

    display_cols = ['研究员', '今日需求', '今日工时', '本周需求', '本周工时',
                    '当月需求', '当月工时', '当季工时', '今年工时']

    # 计算总计（数值类型用于计算）
    numeric_df = pd.DataFrame(data)
    numeric_df = numeric_df[numeric_df[numeric_cols].sum(axis=1) > 0]

    totals = {
        '研究员': '📊 总计',
        '今日需求': int(numeric_df['today_count'].sum()),
        '今日工时': f"{numeric_df['today_hours'].sum():.1f}",
        '本周需求': int(numeric_df['week_count'].sum()),
        '本周工时': f"{numeric_df['week_hours'].sum():.1f}",
        '当月需求': int(numeric_df['month_count'].sum()),
        '当月工时': f"{numeric_df['month_hours'].sum():.1f}",
        '当季工时': f"{numeric_df['quarter_hours'].sum():.1f}",
        '今年工时': f"{numeric_df['year_hours'].sum():.1f}"
    }

    # 数据行
    df_data = df[display_cols].copy()

    # 总计行
    df_total = pd.DataFrame([totals])

    # 分别显示数据和总计
    st.dataframe(
        df_data,
        use_container_width=True,
        hide_index=True,
        height=min(400, len(df_data) * 35 + 38)
    )

    # 总计行用不同样式
    st.markdown("""
        <style>
        .total-row {
            background-color: #f0f2f6;
            font-weight: bold;
            padding: 8px;
            border-radius: 4px;
            margin-top: -10px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.dataframe(
        df_total,
        use_container_width=True,
        hide_index=True,
        column_config={col: st.column_config.Column(width="medium") for col in display_cols}
    )


def render_multi_period_request_type_table(data: list):
    """
    渲染需求类型多时间维度统计表格（优化版）
    - 过滤空数据行
    - 总计行固定在底部，不参与排序
    - 数值格式统一为一位小数
    """
    if not data:
        st.info("暂无数据")
        return

    df = pd.DataFrame(data)

    # 过滤掉所有列都为0的行
    numeric_cols = ['today_count', 'today_hours', 'week_count', 'week_hours',
                    'month_count', 'month_hours', 'quarter_hours', 'year_hours']
    df = df[df[numeric_cols].sum(axis=1) > 0]

    if df.empty:
        st.info("暂无数据")
        return

    # 重命名列
    df = df.rename(columns={
        'request_type': '需求类型',
        'today_count': '今日需求',
        'today_hours': '今日工时',
        'week_count': '本周需求',
        'week_hours': '本周工时',
        'month_count': '当月需求',
        'month_hours': '当月工时',
        'quarter_hours': '当季工时',
        'year_hours': '今年工时'
    })

    # 格式化为一位小数
    for col in ['今日工时', '本周工时', '当月工时', '当季工时', '今年工时']:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f"{x:.1f}")

    display_cols = ['需求类型', '今日需求', '今日工时', '本周需求', '本周工时',
                    '当月需求', '当月工时', '当季工时', '今年工时']

    # 计算总计
    numeric_df = pd.DataFrame(data)
    numeric_df = numeric_df[numeric_df[numeric_cols].sum(axis=1) > 0]

    totals = {
        '需求类型': '📊 总计',
        '今日需求': int(numeric_df['today_count'].sum()),
        '今日工时': f"{numeric_df['today_hours'].sum():.1f}",
        '本周需求': int(numeric_df['week_count'].sum()),
        '本周工时': f"{numeric_df['week_hours'].sum():.1f}",
        '当月需求': int(numeric_df['month_count'].sum()),
        '当月工时': f"{numeric_df['month_hours'].sum():.1f}",
        '当季工时': f"{numeric_df['quarter_hours'].sum():.1f}",
        '今年工时': f"{numeric_df['year_hours'].sum():.1f}"
    }

    df_data = df[display_cols].copy()
    df_total = pd.DataFrame([totals])

    st.dataframe(
        df_data,
        use_container_width=True,
        hide_index=True,
        height=min(400, len(df_data) * 35 + 38)
    )

    st.dataframe(
        df_total,
        use_container_width=True,
        hide_index=True,
        column_config={col: st.column_config.Column(width="medium") for col in display_cols}
    )


def export_to_excel(data: list, filename: str = "导出数据.xlsx") -> bytes:
    """导出数据到Excel"""
    from config import get_org_type, get_status_display

    export_data = []
    for r in data:
        status_text = get_status_display(r.get('status', '')).replace('🟡 ', '').replace('🔵 ', '').replace('🟢 ', '')

        export_data.append({
            '事项': r.get('title', ''),
            '内容概要': r.get('description', ''),
            '研究范畴': r.get('research_scope', ''),
            '需求类型': r.get('request_type', ''),
            '客户名': r.get('org_name', ''),
            '客户类型': r.get('org_type') or get_org_type(r.get('org_name', '')),
            '对应销售': r.get('sales_name', ''),
            '承接研究员': r.get('researcher_name', ''),
            '工时消耗（H）': r.get('work_hours', 0),
            '状态': status_text,
            '是否保密': '是' if r.get('is_confidential') else '否',
            '创建时间': r.get('created_at', ''),
            '完成时间': r.get('completed_at', ''),
            '处理结果': r.get('result_note', ''),
        })

    df = pd.DataFrame(export_data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='需求明细')
    return output.getvalue()
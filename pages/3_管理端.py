# pages/3_管理端.py

import streamlit as st
import pandas as pd
from core.auth import require_role
from components.admin_views import (
    render_time_selector,
    render_overview_cards,
    render_researcher_table,
    render_request_type_table,
    render_org_table,
    render_pie_chart,
    render_bar_chart,
    render_detail_table,
    render_request_list_simple,
    export_to_excel
)
from components.filters import (
    render_status_filter,
    render_request_type_filter,
    render_research_scope_filter,
    render_keyword_filter,
    apply_filters
)
from components.forms import render_user_form
from services.request_service import get_all_requests, reassign_researcher
from services.user_service import get_all_users, get_users_by_role, create_user, delete_user
from services.stats_service import (
    get_overview_stats,
    get_stats_by_researcher,
    get_stats_by_request_type,
    get_stats_by_org,
    get_researcher_detail_stats,
    get_org_detail_stats,
    get_request_type_detail_stats
)
from config import get_role_display, get_org_type, REQUEST_TYPES

st.set_page_config(page_title="管理端", page_icon="📊", layout="wide")

# 检查权限
user = require_role(['admin'])

st.title("📊 管理端")
st.caption(f"当前用户: {user['display_name']}")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 总览", "👤 研究员视角", "📁 需求类型视角", "🏢 客户视角", "🔄 重派管理", "👥 用户管理"
])

# ============================================================
# Tab 1: 总览看板
# ============================================================
with tab1:
    st.subheader("数据总览")

    # 时间选择
    start_date, end_date = render_time_selector("overview_")

    st.divider()

    # 整体统计
    stats = get_overview_stats(start_date, end_date)
    render_overview_cards(stats)

    st.divider()

    # 三列布局：研究员、需求类型、客户
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("按研究员")
        researcher_stats = get_stats_by_researcher(start_date, end_date)
        render_researcher_table(researcher_stats)

        if researcher_stats:
            render_pie_chart(researcher_stats, 'researcher_name', 'total_hours', '工时分布')

    with col2:
        st.subheader("按需求类型")
        type_stats = get_stats_by_request_type(start_date, end_date)
        render_request_type_table(type_stats)

        if type_stats:
            render_pie_chart(type_stats, 'request_type', 'total', '需求类型分布')

    st.divider()

    st.subheader("按客户")
    org_stats = get_stats_by_org(start_date, end_date)
    render_org_table(org_stats)

# ============================================================
# Tab 2: 研究员视角
# ============================================================
with tab2:
    st.subheader("研究员详情")

    # 选择研究员
    researchers = get_users_by_role('researcher')
    researcher_options = {r['display_name']: r['id'] for r in researchers}

    col1, col2 = st.columns([1, 2])
    with col1:
        selected_researcher = st.selectbox(
            "选择研究员",
            list(researcher_options.keys()),
            key="researcher_select"
        )

    # 时间选择
    start_date, end_date = render_time_selector("researcher_")

    if selected_researcher:
        researcher_id = researcher_options[selected_researcher]
        detail = get_researcher_detail_stats(researcher_id, start_date, end_date)

        st.divider()

        # 总览
        overview = detail['overview']
        col1, col2, col3 = st.columns(3)
        col1.metric("需求总数", overview.get('total', 0))
        col2.metric("已完成", overview.get('completed', 0))
        col3.metric("总工时", f"{overview.get('total_hours', 0):.1f}H")

        st.divider()

        # 按需求类型和客户
        col1, col2 = st.columns(2)

        with col1:
            st.write("**按需求类型**")
            by_type = detail['by_type']
            if by_type:
                df = pd.DataFrame(by_type)
                df = df.rename(columns={'request_type': '需求类型', 'total': '数量', 'hours': '工时(H)'})
                df['工时(H)'] = df['工时(H)'].round(1)
                st.dataframe(df, use_container_width=True, hide_index=True)
                render_bar_chart(by_type, 'request_type', 'hours', '各类型工时')
            else:
                st.info("暂无数据")

        with col2:
            st.write("**按客户**")
            by_org = detail['by_org']
            if by_org:
                df = pd.DataFrame(by_org)
                df = df.rename(columns={'org_name': '客户', 'org_type': '类型', 'total': '数量', 'hours': '工时(H)'})
                df['工时(H)'] = df['工时(H)'].round(1)
                st.dataframe(df, use_container_width=True, hide_index=True)
                render_pie_chart(by_org, 'org_name', 'total', '客户需求分布')
            else:
                st.info("暂无数据")

# ============================================================
# Tab 3: 需求类型视角
# ============================================================
with tab3:
    st.subheader("需求类型详情")

    col1, col2 = st.columns([1, 2])
    with col1:
        selected_type = st.selectbox(
            "选择需求类型",
            REQUEST_TYPES,
            key="type_select"
        )

    # 时间选择
    start_date, end_date = render_time_selector("type_")

    if selected_type:
        detail = get_request_type_detail_stats(selected_type, start_date, end_date)

        st.divider()

        # 总览
        overview = detail['overview']
        col1, col2, col3 = st.columns(3)
        col1.metric("需求总数", overview.get('total', 0))
        col2.metric("已完成", overview.get('completed', 0))
        col3.metric("总工时", f"{overview.get('total_hours', 0):.1f}H")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.write("**按研究员**")
            by_researcher = detail['by_researcher']
            if by_researcher:
                df = pd.DataFrame(by_researcher)
                df = df.rename(columns={'researcher_name': '研究员', 'total': '数量', 'hours': '工时(H)'})
                df['工时(H)'] = df['工时(H)'].round(1)
                st.dataframe(df, use_container_width=True, hide_index=True)
                render_bar_chart(by_researcher, 'researcher_name', 'hours', '研究员工时')
            else:
                st.info("暂无数据")

        with col2:
            st.write("**按客户**")
            by_org = detail['by_org']
            if by_org:
                df = pd.DataFrame(by_org)
                df = df.rename(columns={'org_name': '客户', 'org_type': '类型', 'total': '数量', 'hours': '工时(H)'})
                df['工时(H)'] = df['工时(H)'].round(1)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("暂无数据")

# ============================================================
# Tab 4: 客户视角
# ============================================================
with tab4:
    st.subheader("客户详情")

    # 获取所有客户
    all_requests = get_all_requests()
    org_names = list(set(r['org_name'] for r in all_requests if r.get('org_name')))
    org_names.sort()

    col1, col2 = st.columns([1, 2])
    with col1:
        selected_org = st.selectbox(
            "选择客户",
            org_names if org_names else ["暂无客户"],
            key="org_select"
        )

    # 时间选择
    start_date, end_date = render_time_selector("org_")

    if selected_org and selected_org != "暂无客户":
        detail = get_org_detail_stats(selected_org, start_date, end_date)

        st.divider()

        # 总览
        overview = detail['overview']
        col1, col2, col3 = st.columns(3)
        col1.metric("需求总数", overview.get('total', 0))
        col2.metric("已完成", overview.get('completed', 0))
        col3.metric("总工时", f"{overview.get('total_hours', 0):.1f}H")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.write("**按需求类型**")
            by_type = detail['by_type']
            if by_type:
                df = pd.DataFrame(by_type)
                df = df.rename(columns={'request_type': '需求类型', 'total': '数量', 'hours': '工时(H)'})
                df['工时(H)'] = df['工时(H)'].round(1)
                st.dataframe(df, use_container_width=True, hide_index=True)
                # 修改后 (添加 key="org_view_pie")
                render_pie_chart(by_type, 'request_type', 'total', '需求类型分布', key="org_view_pie")
            else:
                st.info("暂无数据")

        with col2:
            st.write("**按研究员**")
            by_researcher = detail['by_researcher']
            if by_researcher:
                df = pd.DataFrame(by_researcher)
                df = df.rename(columns={'researcher_name': '研究员', 'total': '数量', 'hours': '工时(H)'})
                df['工时(H)'] = df['工时(H)'].round(1)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("暂无数据")

        st.divider()

        # 需求列表
        st.write("**需求明细**")
        requests = detail['requests']

        # 导出按钮
        if requests:
            excel_data = export_to_excel(requests)
            st.download_button(
                label="📥 导出Excel",
                data=excel_data,
                file_name=f"{selected_org}_需求明细.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.spreadsheetml"
            )

        render_request_list_simple(requests)

# ============================================================
# Tab 5: 重派管理
# ============================================================
with tab5:
    st.subheader("需求重派")
    st.caption("管理员可以重新分配需求的承接研究员")

    # 只显示未完成的需求
    all_requests = get_all_requests()
    pending_requests = [r for r in all_requests if r['status'] != 'completed']

    researchers = get_users_by_role('researcher')
    researcher_options = {r['display_name']: r['id'] for r in researchers}

    if not pending_requests:
        st.info("没有待处理的需求")
    else:
        for req in pending_requests:
            with st.expander(f"**{req['title']}** (当前: {req['researcher_name']})"):
                st.write(f"**销售:** {req['sales_name']}")
                st.write(f"**需求类型:** {req.get('request_type', '-')}")
                st.write(f"**机构:** {req.get('org_name', '-')}")

                col1, col2 = st.columns([2, 1])
                with col1:
                    current_index = 0
                    if req['researcher_name'] in researcher_options:
                        current_index = list(researcher_options.keys()).index(req['researcher_name'])

                    new_researcher = st.selectbox(
                        "重派给",
                        list(researcher_options.keys()),
                        index=current_index,
                        key=f"reassign_{req['id']}"
                    )
                with col2:
                    if st.button("确认重派", key=f"confirm_{req['id']}", type="primary"):
                        new_id = researcher_options[new_researcher]
                        if new_id != req['researcher_id']:
                            reassign_researcher(req['id'], new_id)
                            st.success(f"已重派给 {new_researcher}")
                            st.rerun()
                        else:
                            st.warning("研究员未变更")

# ============================================================
# Tab 6: 用户管理
# ============================================================
with tab6:
    st.subheader("添加用户")

    form_data = render_user_form()
    if form_data:
        success, msg = create_user(
            form_data['username'],
            form_data['password'],
            form_data['role'],
            form_data['display_name']
        )
        if success:
            st.success(msg)
            st.rerun()
        else:
            st.error(msg)

    st.divider()
    st.subheader("现有用户")

    users = get_all_users()

    for u in users:
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(f"**{u['display_name']}** ({u['username']})")
        with col2:
            st.write(get_role_display(u['role']))
        with col3:
            if u['id'] != user['id']:
                if st.button("删除", key=f"del_{u['id']}"):
                    delete_user(u['id'])
                    st.rerun()

# pages/3_管理端.py - 优化版（二级标签）

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="管理端", page_icon="📊", layout="wide")

from core.auth import require_role
from components.admin_views import (
    render_multi_period_researcher_table,
    render_multi_period_request_type_table,
    render_time_selector,
    render_overview_cards,
    render_researcher_table,
    render_request_type_table,
    render_org_table,
    render_bar_chart,
    export_to_excel
)
from components.filters import render_keyword_filter
from components.forms import render_user_form
from services.request_service import get_all_requests, reassign_researcher, toggle_confidential
from services.user_service import get_all_users, get_users_by_role, create_user, delete_user
from services.stats_service import (
    get_overview_stats,
    get_stats_by_researcher,
    get_stats_by_request_type,
    get_stats_by_org,
    get_multi_period_stats_by_researcher,
    get_multi_period_stats_by_request_type,
    get_researcher_detail_stats,
    get_request_type_detail_stats,
    get_org_detail_stats
)
from config import get_role_display, REQUEST_TYPES, RESEARCH_SCOPES, get_status_display

user = require_role(['admin'])

st.title("📊 管理端")
st.caption(f"当前用户: {user['display_name']}")

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 工作量看板", "📊 多维分析", "📥 数据导出", "⚙️ 系统管理"
])

# ============================================================
# Tab 1: 工作量看板
# ============================================================
with tab1:
    st.subheader("工作量统计看板")

    st.divider()

    st.write("### 📊 （全部人员）研究员")
    researcher_stats = get_multi_period_stats_by_researcher()
    render_multi_period_researcher_table(researcher_stats)

    st.divider()

    st.write("### 📁 （全部标签）需求类型")
    type_stats = get_multi_period_stats_by_request_type()
    render_multi_period_request_type_table(type_stats)

# ============================================================
# Tab 2: 多维分析（二级标签）
# ============================================================
with tab2:
    sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
        "📊 统计看板", "👤 研究员视角", "📁 需求类型视角", "🏢 客户视角"
    ])

    # 统计看板
    with sub_tab1:
        st.subheader("数据总览")

        start_date, end_date = render_time_selector("overview_")

        st.divider()

        stats = get_overview_stats(start_date, end_date)
        render_overview_cards(stats)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("按研究员")
            researcher_stats = get_stats_by_researcher(start_date, end_date)
            render_researcher_table(researcher_stats)

        with col2:
            st.subheader("按需求类型")
            type_stats = get_stats_by_request_type(start_date, end_date)
            render_request_type_table(type_stats)

        st.divider()

        st.subheader("按客户")
        org_stats = get_stats_by_org(start_date, end_date)
        render_org_table(org_stats)

    # 研究员视角
    with sub_tab2:
        st.subheader("👤 研究员详情")

        researchers = get_users_by_role('researcher')
        researcher_options = {r['display_name']: r['id'] for r in researchers}

        col1, col2 = st.columns([1, 2])
        with col1:
            selected_researcher = st.selectbox(
                "选择研究员",
                list(researcher_options.keys()),
                key="researcher_select"
            )

        start_date, end_date = render_time_selector("researcher_")

        if selected_researcher:
            researcher_id = researcher_options[selected_researcher]
            detail = get_researcher_detail_stats(researcher_id, start_date, end_date)

            st.divider()

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
                    render_bar_chart(by_type, 'request_type', 'hours', '各类型工时', key="researcher_type_bar")
                else:
                    st.info("暂无数据")

            with col2:
                st.write("**按客户**")
                by_org = detail['by_org']
                if by_org:
                    df = pd.DataFrame(by_org)
                    df = df.rename(
                        columns={'org_name': '客户', 'org_type': '类型', 'total': '数量', 'hours': '工时(H)'})
                    df['工时(H)'] = df['工时(H)'].round(1)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("暂无数据")

    # 需求类型视角
    with sub_tab3:
        st.subheader("📁 需求类型详情")

        col1, col2 = st.columns([1, 2])
        with col1:
            selected_type = st.selectbox(
                "选择需求类型",
                REQUEST_TYPES,
                key="type_select"
            )

        start_date, end_date = render_time_selector("type_")

        if selected_type:
            detail = get_request_type_detail_stats(selected_type, start_date, end_date)

            st.divider()

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
                    render_bar_chart(by_researcher, 'researcher_name', 'hours', '研究员工时', key="type_researcher_bar")
                else:
                    st.info("暂无数据")

            with col2:
                st.write("**按客户**")
                by_org = detail['by_org']
                if by_org:
                    df = pd.DataFrame(by_org)
                    df = df.rename(
                        columns={'org_name': '客户', 'org_type': '类型', 'total': '数量', 'hours': '工时(H)'})
                    df['工时(H)'] = df['工时(H)'].round(1)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("暂无数据")

    # 客户视角
    with sub_tab4:
        st.subheader("🏢 客户详情")

        all_requests = get_all_requests()
        org_names = sorted(list(set(r['org_name'] for r in all_requests if r.get('org_name'))))

        col1, col2 = st.columns([1, 2])
        with col1:
            selected_org = st.selectbox(
                "选择客户",
                org_names if org_names else ["暂无客户"],
                key="org_select"
            )

        start_date, end_date = render_time_selector("org_")

        if selected_org and selected_org != "暂无客户":
            detail = get_org_detail_stats(selected_org, start_date, end_date)

            st.divider()

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

            st.write("**需求明细**")
            requests = detail['requests']
            if requests:
                excel_data = export_to_excel(requests)
                st.download_button(
                    label="📥 导出Excel",
                    data=excel_data,
                    file_name=f"{selected_org}_需求明细.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

                for req in requests[:10]:
                    confidential_badge = "🔒 " if req.get('is_confidential') else ""
                    status_display = get_status_display(req['status'])
                    with st.expander(f"{confidential_badge}{req['title']} - {status_display}"):
                        st.write(f"**需求类型:** {req.get('request_type')}")
                        st.write(f"**研究员:** {req.get('researcher_name')}")
                        st.write(f"**工时:** {req.get('work_hours', 0):.1f}H")

# ============================================================
# Tab 3: 数据导出
# ============================================================
with tab3:
    st.subheader("📥 数据导出")
    st.caption("支持多条件筛选后导出Excel")

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        start_date_export = st.date_input("开始日期", key="export_start")
        type_options_export = REQUEST_TYPES
        selected_types_export = st.multiselect("需求类型（可多选）", type_options_export, key="export_types")

    with col2:
        end_date_export = st.date_input("结束日期", key="export_end")
        researchers = get_users_by_role('researcher')
        researcher_names = [r['display_name'] for r in researchers]
        selected_researchers_export = st.multiselect("研究员（可多选）", researcher_names, key="export_researchers")

    with col3:
        all_requests = get_all_requests()
        org_list = sorted(list(set(r['org_name'] for r in all_requests if r.get('org_name'))))
        selected_orgs_export = st.multiselect("机构（可多选）", org_list, key="export_orgs")
        status_options_export = ["待处理", "处理中", "已完成"]
        selected_statuses_export = st.multiselect("状态（可多选）", status_options_export, key="export_statuses")

    st.divider()

    if st.button("🔍 预览筛选结果", type="secondary", use_container_width=True):
        filter_start = datetime.combine(start_date_export, datetime.min.time()) if start_date_export else None
        filter_end = datetime.combine(end_date_export, datetime.max.time()) if end_date_export else None

        all_data = get_all_requests()
        filtered_data = all_data

        if filter_start and filter_end:
            filtered_data = [r for r in filtered_data
                             if filter_start <= datetime.fromisoformat(r['created_at']) <= filter_end]

        if selected_types_export:
            filtered_data = [r for r in filtered_data if r.get('request_type') in selected_types_export]

        if selected_researchers_export:
            filtered_data = [r for r in filtered_data if r.get('researcher_name') in selected_researchers_export]

        if selected_orgs_export:
            filtered_data = [r for r in filtered_data if r.get('org_name') in selected_orgs_export]

        if selected_statuses_export:
            status_map = {"待处理": "pending", "处理中": "in_progress", "已完成": "completed"}
            selected_status_values = [status_map[s] for s in selected_statuses_export]
            filtered_data = [r for r in filtered_data if r.get('status') in selected_status_values]

        st.success(f"筛选结果：共 {len(filtered_data)} 条记录")

        if filtered_data:
            preview_data = []
            for r in filtered_data[:20]:
                preview_data.append({
                    '事项': r.get('title', ''),
                    '需求类型': r.get('request_type', ''),
                    '研究员': r.get('researcher_name', ''),
                    '机构': r.get('org_name', ''),
                    '工时': f"{r.get('work_hours', 0):.1f}",
                    '保密': '是' if r.get('is_confidential') else '否',
                })

            df_preview = pd.DataFrame(preview_data)
            st.dataframe(df_preview, use_container_width=True, hide_index=True)

            if len(filtered_data) > 20:
                st.caption("（仅显示前20条，完整数据请下载Excel）")

    st.divider()

    if st.button("📥 导出Excel", type="primary", use_container_width=True):
        filter_start = datetime.combine(start_date_export, datetime.min.time()) if start_date_export else None
        filter_end = datetime.combine(end_date_export, datetime.max.time()) if end_date_export else None

        all_data = get_all_requests()
        export_data = all_data

        if filter_start and filter_end:
            export_data = [r for r in export_data
                           if filter_start <= datetime.fromisoformat(r['created_at']) <= filter_end]

        if selected_types_export:
            export_data = [r for r in export_data if r.get('request_type') in selected_types_export]

        if selected_researchers_export:
            export_data = [r for r in export_data if r.get('researcher_name') in selected_researchers_export]

        if selected_orgs_export:
            export_data = [r for r in export_data if r.get('org_name') in selected_orgs_export]

        if selected_statuses_export:
            status_map = {"待处理": "pending", "处理中": "in_progress", "已完成": "completed"}
            selected_status_values = [status_map[s] for s in selected_statuses_export]
            export_data = [r for r in export_data if r.get('status') in selected_status_values]

        if export_data:
            excel_bytes = export_to_excel(export_data)
            st.download_button(
                label="💾 下载Excel文件",
                data=excel_bytes,
                file_name=f"需求明细_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        else:
            st.warning("没有符合条件的数据")

# ============================================================
# Tab 4: 系统管理
# ============================================================
with tab4:
    sub_tab1, sub_tab2, sub_tab3 = st.tabs(["🔄 重派管理", "🌐 公开需求", "👥 用户管理"])

    with sub_tab1:
        st.subheader("需求管理")

        all_requests = get_all_requests()

        col1, col2 = st.columns([1, 3])
        with col1:
            status_options = ["全部", "待处理", "处理中", "已完成"]
            selected_status = st.selectbox("状态筛选", status_options, key="reassign_status")
        with col2:
            keyword = render_keyword_filter(key="reassign_keyword")

        filtered_requests = all_requests
        if selected_status != "全部":
            status_map = {"待处理": "pending", "处理中": "in_progress", "已完成": "completed"}
            filtered_requests = [r for r in filtered_requests if r['status'] == status_map.get(selected_status)]

        if keyword:
            kw = keyword.lower()
            filtered_requests = [r for r in filtered_requests
                                 if kw in (r.get('title') or '').lower()
                                 or kw in (r.get('org_name') or '').lower()]

        researchers = get_users_by_role('researcher')
        researcher_options = {r['display_name']: r['id'] for r in researchers}

        if not filtered_requests:
            st.info("没有符合条件的需求")
        else:
            st.write(f"共 {len(filtered_requests)} 条需求")

            for req in filtered_requests:
                confidential_badge = "🔒 " if req.get('is_confidential') else "🔓 "
                status_display = get_status_display(req['status'])

                with st.expander(f"{confidential_badge}**{req['title']}** - {status_display}"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(f"**销售:** {req['sales_name']}")
                        st.write(f"**需求类型:** {req.get('request_type', '-')}")

                    with col2:
                        st.write(f"**研究员:** {req['researcher_name']}")
                        st.write(f"**机构:** {req.get('org_name', '-')}")

                    st.divider()

                    col_a, col_b, col_c, col_d = st.columns([2, 1, 2, 1])

                    with col_a:
                        current_index = 0
                        if req['researcher_name'] in researcher_options:
                            current_index = list(researcher_options.keys()).index(req['researcher_name'])

                        new_researcher = st.selectbox(
                            "重派给",
                            list(researcher_options.keys()),
                            index=current_index,
                            key=f"reassign_{req['id']}"
                        )

                    with col_b:
                        if st.button("确认重派", key=f"confirm_reassign_{req['id']}"):
                            new_id = researcher_options[new_researcher]
                            if new_id != req['researcher_id']:
                                reassign_researcher(req['id'], new_id)
                                st.success(f"已重派给 {new_researcher}")
                                st.rerun()

                    with col_c:
                        current_conf = req.get('is_confidential', 0)
                        new_conf_status = st.radio(
                            "保密状态",
                            ["公开", "保密"],
                            index=1 if current_conf else 0,
                            key=f"conf_{req['id']}",
                            horizontal=True
                        )

                    with col_d:
                        if st.button("确认修改", key=f"confirm_conf_{req['id']}"):
                            new_is_conf = (new_conf_status == "保密")
                            if new_is_conf != bool(current_conf):
                                toggle_confidential(req['id'], new_is_conf)
                                st.success(f"已修改为{new_conf_status}")
                                st.rerun()

    with sub_tab2:
        st.subheader("公开需求")

        col1, col2, col3 = st.columns(3)
        with col1:
            status_options_pub = ["全部", "待处理", "处理中", "已完成"]
            selected_status_pub = st.selectbox("状态", status_options_pub, key="public_status")
        with col2:
            type_options_pub = ["全部"] + REQUEST_TYPES
            selected_type_pub = st.selectbox("需求类型", type_options_pub, key="public_type")
        with col3:
            scope_options_pub = ["全部"] + RESEARCH_SCOPES
            selected_scope_pub = st.selectbox("研究范畴", scope_options_pub, key="public_scope")

        all_requests = get_all_requests()
        public_requests = [r for r in all_requests if not r.get('is_confidential')]

        filtered_public = public_requests
        if selected_status_pub != "全部":
            status_map = {"待处理": "pending", "处理中": "in_progress", "已完成": "completed"}
            filtered_public = [r for r in filtered_public if r['status'] == status_map.get(selected_status_pub)]
        if selected_type_pub != "全部":
            filtered_public = [r for r in filtered_public if r.get('request_type') == selected_type_pub]
        if selected_scope_pub != "全部":
            filtered_public = [r for r in filtered_public if r.get('research_scope') == selected_scope_pub]

        st.write(f"共 {len(filtered_public)} 条记录")

        if not filtered_public:
            st.info("暂无公开需求")
        else:
            for req in filtered_public[:20]:
                status_display = get_status_display(req['status'])

                with st.expander(f"**{req['title']}** - {status_display}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**需求类型:** {req.get('request_type') or '-'}")
                        st.write(f"**研究员:** {req.get('researcher_name', '-')}")
                    with col2:
                        st.write(f"**销售:** {req.get('sales_name', '-')}")
                        st.write(f"**创建时间:** {req.get('created_at', '-')}")

                    if req.get('description'):
                        st.write(f"**内容概要:** {req['description']}")

                    if req['status'] == 'completed' and req.get('result_note'):
                        st.divider()
                        st.write(f"**处理结果:** {req.get('result_note')}")

    with sub_tab3:
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
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : 2_研究端.py
@Time    : 2025/12/9 11:09
@Author  : jijunye
@Desc    : 
"""
# pages/2_研究端.py

import os
import streamlit as st
from core.auth import require_role
from components.cards import render_mini_stats
from components.filters import (
    render_status_filter,
    render_request_type_filter,
    render_research_scope_filter,
    apply_filters
)
from services.request_service import (
    get_requests_by_researcher,
    get_visible_requests_for_user,
    update_request_status
)
from services.stats_service import get_user_stats
from config import get_status_display

st.set_page_config(page_title="研究端", page_icon="🔬", layout="wide")

# 检查权限
user = require_role(['researcher'])

st.title("🔬 研究端")
st.caption(f"当前用户: {user['display_name']}")


def handle_status_update(request_id: int, status: str, result_note: str, uploaded_file, work_hours: float):
    """处理状态更新"""
    attachment_path = None
    if uploaded_file:
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, f"{request_id}_{uploaded_file.name}")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        attachment_path = file_path

    update_request_status(request_id, status, result_note, attachment_path, work_hours)
    st.success("保存成功！")
    st.rerun()


tab1, tab2 = st.tabs(["📋 我的任务", "🌐 公开需求"])

# Tab 1: 我的任务
with tab1:
    st.subheader("分配给我的需求")

    # 统计卡片
    my_stats = get_user_stats(user['id'], 'researcher')
    render_mini_stats(my_stats)

    st.divider()

    # 筛选
    status_filter = render_status_filter(key="my_task_filter")

    # 获取数据
    my_requests = get_requests_by_researcher(user['id'])
    filtered = apply_filters(my_requests, {'status': status_filter})

    st.write(f"共 {len(filtered)} 条记录")

    if not filtered:
        st.info("暂无需求记录")
    else:
        for req in filtered:
            status_display = get_status_display(req['status'])

            # 标题
            title_prefix = "🔒 " if req.get('is_confidential') else ""
            expander_title = f"{title_prefix}**{req['title']}** - {status_display} (来自: {req['sales_name']})"

            with st.expander(expander_title):
                # 基本信息
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**需求类型:** {req.get('request_type') or '-'}")
                    st.write(f"**研究范畴:** {req.get('research_scope') or '-'}")
                    st.write(f"**机构:** {req.get('org_name') or '-'}")
                with col2:
                    st.write(f"**销售:** {req.get('sales_name', '-')}")
                    st.write(f"**创建时间:** {req.get('created_at', '-')}")
                    st.write(f"**更新时间:** {req.get('updated_at', '-')}")

                if req.get('description'):
                    st.write(f"**描述:** {req['description']}")

                st.divider()

                # 已完成：显示结果
                if req['status'] == 'completed':
                    st.write("**📌 处理结果:**")
                    st.write(req.get('result_note') or '-')

                    # 附件下载
                    if req.get('attachment_path') and os.path.exists(req['attachment_path']):
                        file_name = os.path.basename(req['attachment_path'])
                        with open(req['attachment_path'], "rb") as f:
                            st.download_button(
                                label=f"📎 下载: {file_name}",
                                data=f.read(),
                                file_name=file_name,
                                key=f"dl_{req['id']}"
                            )
                        # 图片预览
                        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                            st.image(req['attachment_path'], caption=file_name, width=400)

                # 未完成：可编辑状态
                else:
                    st.write("**更新状态:**")

                    new_status = st.selectbox(
                        "状态",
                        ["pending", "in_progress", "completed"],
                        index=["pending", "in_progress", "completed"].index(req['status']),
                        format_func=lambda x:
                        {"pending": "待处理", "in_progress": "处理中", "completed": "已完成"}[x],
                        key=f"status_{req['id']}"
                    )

                    result_note = st.text_area(
                        "完成说明",
                        key=f"note_{req['id']}",
                        placeholder="填写处理过程或结果说明..."
                    )

                    uploaded_file = st.file_uploader(
                        "上传附件",
                        key=f"file_{req['id']}",
                        help="支持任意文件格式"
                    )

                    work_hours = st.number_input(
                        "工时消耗（小时）",
                        min_value=0.0,
                        max_value=24.0,
                        step=0.5,
                        key=f"hours_{req['id']}",
                        help="完成此任务花费的工时"
                    )

                    if st.button("💾 保存", key=f"save_{req['id']}", type="primary"):
                        handle_status_update(req['id'], new_status, result_note, uploaded_file, work_hours)

# Tab 2: 公开需求
with tab2:
    st.subheader("公开需求")
    st.caption("所有已完成的公开需求")

    # 筛选
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = render_status_filter(key="public_task_filter")
    with col2:
        type_filter = render_request_type_filter(key="public_type_filter")
    with col3:
        scope_filter = render_research_scope_filter(key="public_scope_filter")

    # 获取所有非保密需求
    visible_requests = get_visible_requests_for_user(user)
    public_requests = [r for r in visible_requests
                       if not r.get('is_confidential') and r['status'] == 'completed']

    filtered = apply_filters(public_requests, {
        'status': status_filter,
        'request_type': type_filter,
        'research_scope': scope_filter
    })

    st.write(f"共 {len(filtered)} 条记录")

    if not filtered:
        st.info("暂无公开需求")
    else:
        for req in filtered:
            status_display = get_status_display(req['status'])
            is_mine = req['researcher_id'] == user['id']
            badge = "📌 " if is_mine else ""
            expander_title = f"{badge}**{req['title']}** - {status_display}"

            with st.expander(expander_title):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**需求类型:** {req.get('request_type') or '-'}")
                    st.write(f"**研究范畴:** {req.get('research_scope') or '-'}")
                    st.write(f"**机构:** {req.get('org_name') or '-'}")
                with col2:
                    st.write(f"**销售:** {req.get('sales_name', '-')}")
                    st.write(f"**研究员:** {req.get('researcher_name', '-')}")
                    st.write(f"**创建时间:** {req.get('created_at', '-')}")

                if req.get('description'):
                    st.write(f"**描述:** {req['description']}")

                # 已完成的显示结果和附件
                if req['status'] == 'completed':
                    st.divider()
                    st.write("**📌 处理结果:**")
                    st.write(req.get('result_note') or '-')

                    # 附件下载
                    if req.get('attachment_path') and os.path.exists(req['attachment_path']):
                        file_name = os.path.basename(req['attachment_path'])
                        with open(req['attachment_path'], "rb") as f:
                            st.download_button(
                                label=f"📎 下载: {file_name}",
                                data=f.read(),
                                file_name=file_name,
                                key=f"pub_dl_{req['id']}"
                            )
                        # 图片预览
                        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                            st.image(req['attachment_path'], caption=file_name, width=400)
# components/tables.py - 列表/表格组件

import os
import streamlit as st
from config import get_status_display


def render_request_list(
    requests: list,
    show_sales: bool = False,
    show_researcher: bool = True,
    show_confidential_badge: bool = False,
    current_user: dict = None,
    on_status_update: callable = None
):
    """
    渲染需求列表
    
    参数:
        requests: 需求列表
        show_sales: 是否显示销售人员
        show_researcher: 是否显示研究员
        show_confidential_badge: 是否显示保密标记
        current_user: 当前用户（用于判断是否可编辑）
        on_status_update: 状态更新回调（研究员端用）
    """
    if not requests:
        st.info("暂无需求记录")
        return
    
    for req in requests:
        status_display = get_status_display(req['status'])
        
        # 构建标题
        title_parts = [f"**{req['title']}**", f"- {status_display}"]
        if show_confidential_badge and req.get('is_confidential'):
            title_parts.insert(0, "🔒")
        
        expander_title = " ".join(title_parts)
        
        with st.expander(expander_title):
            _render_request_detail(
                req,
                show_sales=show_sales,
                show_researcher=show_researcher,
                current_user=current_user,
                on_status_update=on_status_update
            )


def _render_request_detail(
    req: dict,
    show_sales: bool,
    show_researcher: bool,
    current_user: dict,
    on_status_update: callable
):
    """渲染单个需求的详情"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**需求类型:** {req.get('request_type') or '-'}")
        st.write(f"**研究范畴:** {req.get('research_scope') or '-'}")
        st.write(f"**机构:** {req.get('org_name') or '-'}")
    
    with col2:
        if show_sales:
            st.write(f"**销售:** {req.get('sales_name', '-')}")
        if show_researcher:
            st.write(f"**研究员:** {req.get('researcher_name', '-')}")
        st.write(f"**创建时间:** {req.get('created_at', '-')}")
    
    if req.get('description'):
        st.write(f"**描述:** {req['description']}")
    
    # 已完成的显示结果
    if req['status'] == 'completed':
        st.divider()
        st.write("**📌 处理结果:**")
        st.write(req.get('result_note') or '-')
        _render_attachment(req)
    
    # 研究员可更新状态
    elif on_status_update and current_user:
        is_assigned_researcher = current_user['id'] == req.get('researcher_id')
        if is_assigned_researcher:
            st.divider()
            _render_status_update_section(req, on_status_update)


def _render_attachment(req: dict):
    """渲染附件下载和预览"""
    file_path = req.get('attachment_path')
    if not file_path or not os.path.exists(file_path):
        return
    
    file_name = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    st.download_button(
        label=f"📎 下载: {file_name}",
        data=file_data,
        file_name=file_name,
        key=f"download_{req['id']}"
    )
    
    # 图片预览
    if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        st.image(file_path, caption=file_name, width=400)


def _render_status_update_section(req: dict, on_status_update: callable):
    """渲染状态更新区域"""
    st.write("**更新状态:**")
    
    new_status = st.selectbox(
        "状态",
        ["pending", "in_progress", "completed"],
        index=["pending", "in_progress", "completed"].index(req['status']),
        format_func=lambda x: {"pending": "待处理", "in_progress": "处理中", "completed": "已完成"}[x],
        key=f"status_{req['id']}"
    )
    
    result_note = st.text_area("完成说明", key=f"note_{req['id']}")
    uploaded_file = st.file_uploader("上传附件", key=f"file_{req['id']}")
    
    if st.button("保存", key=f"save_{req['id']}"):
        on_status_update(req['id'], new_status, result_note, uploaded_file)

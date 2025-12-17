# pages/1_销售端.py

import streamlit as st
from core.auth import require_role
from components.forms import render_request_form
from components.tables import render_request_list
from components.cards import render_mini_stats
from components.filters import (
    render_status_filter,
    render_request_type_filter,
    render_research_scope_filter,
    apply_filters
)
from services.request_service import (
    create_request,
    get_requests_by_sales,
    get_visible_requests_for_user
)
from services.stats_service import get_user_stats
from config import get_status_display

st.set_page_config(page_title="销售端", page_icon="💼", layout="wide")

# 检查权限
user = require_role(['sales'])

st.title("💼 销售端")
st.caption(f"当前用户: {user['display_name']}")

tab1, tab2, tab3 = st.tabs(["📝 提交需求", "📋 我的需求", "🌐 公开需求"])

# Tab 1: 提交需求
with tab1:
    st.subheader("提交新需求")
    
    form_data = render_request_form(user)

    if form_data:
        create_request(
            title=form_data['title'],
            description=form_data['description'],
            request_type=form_data['request_type'],
            research_scope=form_data['research_scope'],
            org_name=form_data['org_name'],
            org_type=form_data['org_type'],
            sales_id=user['id'],
            researcher_id=form_data['researcher_id'],
            is_confidential=form_data['is_confidential']
        )
        st.success("需求提交成功！")
        st.rerun()

# Tab 2: 我的需求
with tab2:
    st.subheader("我提交的需求")
    
    # 统计卡片
    my_stats = get_user_stats(user['id'], 'sales')
    render_mini_stats(my_stats)
    
    st.divider()
    
    # 筛选
    status_filter = render_status_filter(key="my_status_filter")
    
    # 获取并筛选数据
    my_requests = get_requests_by_sales(user['id'])
    filtered = apply_filters(my_requests, {'status': status_filter})
    
    st.write(f"共 {len(filtered)} 条记录")
    
    render_request_list(
        filtered,
        show_researcher=True,
        show_confidential_badge=True
    )

# Tab 3: 公开需求
with tab3:
    st.subheader("公开需求")
    st.caption("所有已完成的公开需求")

    # 筛选
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = render_status_filter(key="public_status_filter")
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
            is_mine = req['sales_id'] == user['id']
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
                    if req.get('attachment_path'):
                        import os

                        if os.path.exists(req['attachment_path']):
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

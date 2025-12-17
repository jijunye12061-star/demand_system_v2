# components/forms.py - 表单组件

import streamlit as st
from config import REQUEST_TYPES, RESEARCH_SCOPES, get_orgs_for_sales
from services.user_service import get_users_by_role


def render_request_form(current_user: dict) -> dict | None:
    """
    渲染需求提交表单
    返回表单数据字典，如果未提交或验证失败返回None
    """
    from config import get_org_type, ORG_TYPES, needs_remark

    # 获取研究员列表
    researchers = get_users_by_role('researcher')
    researcher_options = {r['display_name']: r['id'] for r in researchers}

    # 获取当前销售可选的机构
    orgs = get_orgs_for_sales(current_user['username'])

    with st.form("request_form", clear_on_submit=True):
        title = st.text_input("事项名称 *")
        description = st.text_area("事项描述")

        col1, col2 = st.columns(2)
        with col1:
            request_type = st.selectbox("需求类型 *", REQUEST_TYPES)
            org_name = st.selectbox("机构名称 *", orgs)
        with col2:
            research_scope = st.selectbox("研究范畴 *", RESEARCH_SCOPES)
            assigned_to = st.selectbox("承接研究员 *", list(researcher_options.keys()))

        # 需求类型为"其他"时，显示备注输入框
        request_type_remark = ""
        if needs_remark(request_type):
            request_type_remark = st.text_input("需求类型备注 *", placeholder="请说明具体需求类型")

        # 研究范畴为"其他"时，显示备注输入框
        research_scope_remark = ""
        if needs_remark(research_scope):
            research_scope_remark = st.text_input("研究范畴备注 *", placeholder="请说明具体研究范畴")

        # 客户类型：已配置的机构自动带出，"其他机构"需手动选
        auto_org_type = get_org_type(org_name)
        if org_name != "其他机构" and auto_org_type != "其他":
            st.info(f"📌 客户类型: **{auto_org_type}**（自动识别）")
            org_type = auto_org_type
            other_org_name = ""
        else:
            org_type = st.selectbox("客户类型 *", ORG_TYPES)
            other_org_name = st.text_input("机构名称（手填） *", placeholder="请输入具体机构名称")

        is_confidential = st.checkbox("🔒 保密需求（仅您和承接研究员可见）")

        submitted = st.form_submit_button("提交需求", use_container_width=True)

        if submitted:
            # 校验
            if not title.strip():
                st.error("请填写事项名称")
                return None
            if not assigned_to:
                st.error("请选择承接研究员")
                return None
            if needs_remark(request_type) and not request_type_remark.strip():
                st.error("请填写需求类型备注")
                return None
            if needs_remark(research_scope) and not research_scope_remark.strip():
                st.error("请填写研究范畴备注")
                return None
            if org_name == "其他机构" and not other_org_name.strip():
                st.error("请填写具体机构名称")
                return None

            # 处理最终值
            final_request_type = f"{request_type}({request_type_remark})" if request_type_remark else request_type
            final_research_scope = f"{research_scope}({research_scope_remark})" if research_scope_remark else research_scope
            final_org_name = other_org_name.strip() if org_name == "其他机构" else org_name

            return {
                'title': title.strip(),
                'description': description.strip(),
                'request_type': final_request_type,
                'research_scope': final_research_scope,
                'org_name': final_org_name,
                'org_type': org_type,
                'researcher_id': researcher_options[assigned_to],
                'is_confidential': is_confidential,
            }

    return None


def render_user_form() -> dict | None:
    """渲染用户创建表单"""
    with st.form("add_user_form"):
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("用户名 *")
            password = st.text_input("密码 *", type="password")
        with col2:
            role = st.selectbox(
                "角色 *",
                ["sales", "researcher", "admin"],
                format_func=lambda x: {"sales": "销售", "researcher": "研究员", "admin": "管理员"}[x]
            )
            display_name = st.text_input("显示名称 *")
        
        submitted = st.form_submit_button("添加用户")
        
        if submitted:
            if not all([username, password, display_name]):
                st.error("请填写完整信息")
                return None
            return {
                'username': username,
                'password': password,
                'role': role,
                'display_name': display_name,
            }
    
    return None


def render_status_update_form(request: dict) -> dict | None:
    """渲染状态更新表单（研究员用）"""
    current_status = request['status']
    
    new_status = st.selectbox(
        "状态",
        ["pending", "in_progress", "completed"],
        index=["pending", "in_progress", "completed"].index(current_status),
        format_func=lambda x: {"pending": "待处理", "in_progress": "处理中", "completed": "已完成"}[x],
        key=f"status_{request['id']}"
    )
    
    result_note = st.text_area("完成说明", key=f"note_{request['id']}")
    uploaded_file = st.file_uploader("上传附件", key=f"file_{request['id']}")
    
    if st.button("保存", key=f"save_{request['id']}"):
        return {
            'status': new_status,
            'result_note': result_note,
            'uploaded_file': uploaded_file,
        }
    
    return None

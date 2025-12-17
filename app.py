# app.py - 系统入口

import streamlit as st
from core.database import init_db
from core.auth import check_login, get_current_user, login, logout
from config import get_role_display

# 初始化数据库
init_db()

st.set_page_config(
    page_title="需求管理系统",
    page_icon="📋",
    layout="wide"
)

st.title("📋 需求管理系统")

# 侧边栏用户信息
with st.sidebar:
    if check_login():
        user = get_current_user()
        st.success(f"👤 {user['display_name']}")
        st.caption(f"角色: {get_role_display(user['role'])}")
        if st.button("退出登录"):
            logout()
            st.rerun()
    else:
        st.info("请登录后使用系统")

# 主页面
if check_login():
    user = get_current_user()
    st.write(f"欢迎回来，{user['display_name']}！")
    st.divider()
    
    role = user['role']
    if role == 'sales':
        st.info("👉 请点击左侧菜单的「销售端」提交或查看需求")
    elif role == 'researcher':
        st.info("👉 请点击左侧菜单的「研究端」处理分配给您的需求")
    elif role == 'admin':
        st.info("👉 请点击左侧菜单的「管理端」查看统计和管理用户")

else:
    # 登录表单
    st.subheader("用户登录")
    
    with st.form("login_form"):
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        submitted = st.form_submit_button("登录", use_container_width=True)
        
        if submitted:
            if login(username, password):
                st.success("登录成功！")
                st.rerun()
            else:
                st.error("用户名或密码错误")
    
    st.divider()
    st.caption("测试账号：")
    st.code("""
管理员: admin / admin123
销售: sales1 / 123456, sales2 / 123456
研究员: researcher1 / 123456, researcher2 / 123456
    """)

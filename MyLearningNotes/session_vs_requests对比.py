"""
session.post vs requests.post 对比示例
演示两者的区别
"""

import requests

# ============================================
# 方式1：使用 requests.post（不保持 Cookie）
# ============================================

def test_with_requests():
    """使用 requests.post，需要手动管理 Cookie"""
    print("=== 方式1：使用 requests.post ===")
    
    # 步骤1：登录
    login_url = 'http://127.0.0.1:8000/api/login'
    login_data = {"username": "admin", "password": "123456"}
    response1 = requests.post(login_url, json=login_data)
    
    print("登录响应:", response1.json())
    print("Cookie:", response1.cookies)  # 有 Cookie，但没有保存
    
    # 步骤2：访问用户信息（需要手动传递 Cookie）
    profile_url = 'http://127.0.0.1:8000/api/user/profile'
    response2 = requests.get(
        profile_url,
        cookies=response1.cookies  # ⚠️ 必须手动传递 Cookie
    )
    
    print("用户信息:", response2.json())
    print("问题：每次请求都要手动传递 Cookie\n")


# ============================================
# 方式2：使用 session.post（自动保持 Cookie）
# ============================================

def test_with_session():
    """使用 session.post，自动管理 Cookie"""
    print("=== 方式2：使用 session.post ===")
    
    # 创建会话（自动管理 Cookie）
    session = requests.Session()
    
    # 步骤1：登录
    login_url = 'http://127.0.0.1:8000/api/login'
    login_data = {"username": "admin", "password": "123456"}
    response1 = session.post(login_url, json=login_data)
    
    print("登录响应:", response1.json())
    print("Session Cookie:", session.cookies)  # ✅ Cookie 自动保存到 session
    
    # 步骤2：访问用户信息（自动使用 Cookie）
    profile_url = 'http://127.0.0.1:8000/api/user/profile'
    response2 = session.get(profile_url)  # ✅ 自动使用 session 中的 Cookie
    
    print("用户信息:", response2.json())
    print("优势：Cookie 自动管理，无需手动传递\n")


# ============================================
# Response.set_cookie 说明
# ============================================

"""
Response.set_cookie 是 FastAPI/Starlette 的 Response 对象的方法

from fastapi import Response

@app.post("/api/login")
async def login(response: Response):
    # set_cookie 是 Response 对象的方法
    response.set_cookie(
        key="session-id",      # Cookie 名称
        value="abc123",        # Cookie 值
        max_age=3600,          # 过期时间（秒）
        httponly=True,         # 防止 JavaScript 访问
        samesite="lax"         # 防止 CSRF 攻击
    )
    return {"message": "登录成功"}

# Response 对象来自 Starlette（FastAPI 基于 Starlette）
# 常用方法：
# - response.set_cookie()    # 设置 Cookie
# - response.delete_cookie()  # 删除 Cookie
# - response.headers          # 设置响应头
# - response.status_code      # 设置状态码
"""

# ============================================
# 完整对比表
# ============================================

"""
| 特性 | requests.post() | session.post() |
|------|----------------|---------------|
| Cookie 管理 | ❌ 不自动保存 | ✅ 自动保存 |
| 后续请求 | 需手动传递 Cookie | 自动使用 Cookie |
| 代码复杂度 | ⚠️ 需要手动管理 | ✅ 自动管理 |
| 使用场景 | 单次请求 | 需要保持会话的多次请求 |
| 性能 | 每次创建新连接 | 复用连接（更快） |
"""

# ============================================
# 实际使用建议
# ============================================

"""
1. 单次请求 → 使用 requests.post()
   - 不需要保持会话
   - 简单直接

2. 多次请求（需要 Cookie） → 使用 session.post()
   - 需要登录后访问多个接口
   - 自动管理 Cookie，代码更简洁

3. 浏览器 → 自动管理 Cookie
   - 浏览器会自动保存和发送 Cookie
   - 无需 JavaScript 代码
"""

if __name__ == "__main__":
    # 注意：需要先启动 FastAPI 服务器
    # test_with_requests()
    # test_with_session()
    pass


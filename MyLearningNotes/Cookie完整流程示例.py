"""
Cookie 完整流程示例
演示：设置 Cookie → 浏览器存储 → 自动发送 → FastAPI 读取
"""

import uvicorn
from fastapi import FastAPI, Cookie, Response
from typing import Annotated

# 1. 创建 FastAPI 应用
app = FastAPI(title="Cookie 完整流程示例")

# 2. 设置 Cookie 的端点（模拟登录）
@app.post("/api/login")
async def login(username: str, password: str, response: Response):
    """
    登录接口 - 设置 Cookie
    
    当浏览器收到这个响应时，会自动存储 Cookie
    """
    # 模拟登录验证
    if username == "admin" and password == "123456":
        # 设置 Cookie（浏览器会自动存储）
        response.set_cookie(
            key="session-id",      # Cookie 名称
            value="abc123xyz",      # Cookie 值
            max_age=3600,          # 过期时间（1小时）
            httponly=True,         # 防止 JavaScript 访问（安全）
            samesite="lax"         # 防止 CSRF 攻击
        )
        response.set_cookie(
            key="user-token",
            value="token_xyz789",
            max_age=3600
        )
        
        return {
            "message": "登录成功",
            "提示": "Cookie 已设置，浏览器会自动存储"
        }
    return {"error": "用户名或密码错误"}

# 3. 读取 Cookie 的端点
@app.get("/api/user/profile")
async def get_user_profile(
    session_id: Annotated[str | None, Cookie()] = None,
    user_token: Annotated[str | None, Cookie()] = None
):
    """
    获取用户信息 - 读取 Cookie
    
    FastAPI 从 HTTP 请求头的 Cookie 中自动读取
    """
    if not session_id:
        return {"error": "未登录，请先访问 /api/login"}
    
    return {
        "message": "获取用户信息成功",
        "session_id": session_id,
        "user_token": user_token,
        "说明": "这些值是从 HTTP 请求头的 Cookie 中读取的"
    }

# 4. 清除 Cookie 的端点（登出）
@app.post("/api/logout")
async def logout(response: Response):
    """
    登出接口 - 清除 Cookie
    """
    response.delete_cookie(key="session-id")
    response.delete_cookie(key="user-token")
    return {"message": "已登出，Cookie 已清除"}

# 5. 启动服务器
if __name__ == '__main__':
    config = uvicorn.Config(app, host='0.0.0.0', port=8000)
    server = uvicorn.Server(config)
    await server.serve()

# ============================================
# 完整流程说明
# ============================================

"""
1. 设置 Cookie（登录）
   POST /api/login
   响应头：Set-Cookie: session-id=abc123xyz
   → 浏览器自动存储 Cookie

2. 浏览器自动发送 Cookie（访问其他页面）
   GET /api/user/profile
   请求头：Cookie: session-id=abc123xyz
   → 浏览器自动添加存储的 Cookie

3. FastAPI 读取 Cookie
   session_id: Annotated[str | None, Cookie()]
   → FastAPI 从请求头的 Cookie 中提取 session-id

4. 清除 Cookie（登出）
   POST /api/logout
   响应头：Set-Cookie: session-id=; Max-Age=0
   → 浏览器删除 Cookie
"""

# ============================================
# 测试代码
# ============================================

"""
import requests

# 创建会话（保持 Cookie）
session = requests.Session()

# 步骤1：登录（设置 Cookie）
login_url = 'http://127.0.0.1:8000/api/login'
login_data = {"username": "admin", "password": "123456"}
response1 = session.post(login_url, json=login_data)
print("登录响应:", response1.json())
print("Cookie:", session.cookies)  # 查看存储的 Cookie

# 步骤2：访问用户信息（自动发送 Cookie）
profile_url = 'http://127.0.0.1:8000/api/user/profile'
response2 = session.get(profile_url)
print("用户信息:", response2.json())
# 注意：session 会自动管理 Cookie，无需手动设置

# 步骤3：登出（清除 Cookie）
logout_url = 'http://127.0.0.1:8000/api/logout'
response3 = session.post(logout_url)
print("登出响应:", response3.json())
"""

# ============================================
# 关键理解
# ============================================

"""
1. Cookie 存储位置：
   ✅ 浏览器（客户端）
   ❌ 不是服务器

2. Cookie 传递方式：
   - 服务器设置：响应头 Set-Cookie
   - 浏览器存储：自动保存到浏览器
   - 浏览器发送：每个请求自动添加 Cookie 头
   - 服务器读取：从请求头 Cookie 中提取

3. FastAPI 读取 Cookie：
   - 从 HTTP 请求头的 Cookie 字段中读取
   - 自动解析 Cookie 字符串
   - 匹配 Cookie 名称（session-id → session_id）

4. 为什么浏览器会自动发送？
   - 这是浏览器的标准行为
   - 每个 HTTP 请求都会自动包含该域名的 Cookie
   - 无需 JavaScript 代码手动添加
"""


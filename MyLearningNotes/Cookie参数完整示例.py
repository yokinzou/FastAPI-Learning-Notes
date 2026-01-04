"""
完整的 Cookie 参数示例
演示如何使用 Cookie 参数
"""

import uvicorn
from fastapi import FastAPI, Cookie
from typing import Annotated
from pydantic import BaseModel

# 1. 创建 FastAPI 应用
app = FastAPI(title="Cookie 参数示例", description="演示如何读取 Cookie 参数")

# 2. 定义模型（可选）
class UserInfo(BaseModel):
    """用户信息模型"""
    name: str
    email: str

# 3. 定义使用 Cookie 参数的端点
@app.get("/api/user/profile")
async def get_user_profile(
    session_id: Annotated[str | None, Cookie()] = None,  # Cookie 参数（可选）
    user_token: Annotated[str | None, Cookie()] = None   # Cookie 参数（可选）
):
    """
    获取用户信息（从 Cookie 中读取会话信息）
    
    参数:
        session_id: 会话ID（从 Cookie 中读取）
        user_token: 用户令牌（从 Cookie 中读取）
    
    返回:
        用户信息
    """
    # 检查 Cookie 是否存在
    if not session_id:
        return {"error": "缺少 session_id Cookie"}
    
    if not user_token:
        return {"error": "缺少 user_token Cookie"}
    
    # 模拟根据 session_id 和 user_token 查询用户信息
    return {
        "message": "获取用户信息成功",
        "session_id": session_id,
        "user_token": user_token,
        "user_info": {
            "name": "张三",
            "email": "zhangsan@example.com"
        }
    }

# 4. 设置 Cookie 的端点（用于测试）
@app.post("/api/login")
async def login(username: str, password: str):
    """
    登录接口（设置 Cookie）
    
    注意：实际应用中，应该在响应中设置 Cookie
    这里只是演示如何读取 Cookie
    """
    # 模拟登录验证
    if username == "admin" and password == "123456":
        return {
            "message": "登录成功",
            "session_id": "abc123xyz",
            "user_token": "token_xyz789",
            "提示": "请使用这些值设置 Cookie 来测试 /api/user/profile 接口"
        }
    return {"error": "用户名或密码错误"}

# 5. 必需 Cookie 参数的示例
@app.get("/api/user/settings")
async def get_user_settings(
    session_id: Annotated[str, Cookie()]  # 必需 Cookie 参数（没有默认值）
):
    """
    获取用户设置（需要 Cookie）
    
    参数:
        session_id: 会话ID（必需，从 Cookie 中读取）
    
    返回:
        用户设置
    """
    return {
        "session_id": session_id,
        "settings": {
            "theme": "dark",
            "language": "zh-CN"
        }
    }

# 6. 启动服务器
if __name__ == '__main__':
    config = uvicorn.Config(app, host='0.0.0.0', port=8000)
    server = uvicorn.Server(config)
    await server.serve()

# ============================================
# 测试代码（在另一个文件中运行，或使用 /docs 界面）
# ============================================

# 方式1：使用 requests 库测试
"""
import requests

# 测试1：读取 Cookie 参数
url = 'http://127.0.0.1:8000/api/user/profile'

# 设置 Cookie（注意：Cookie 名称会自动转换：session_id → session-id）
cookies = {
    "session-id": "abc123xyz",      # Python: session_id → HTTP: session-id
    "user-token": "token_xyz789"    # Python: user_token → HTTP: user-token
}

response = requests.get(url, cookies=cookies)
print("测试1（读取 Cookie）:", response.json())

# 输出示例：
# {
#     "message": "获取用户信息成功",
#     "session_id": "abc123xyz",
#     "user_token": "token_xyz789",
#     "user_info": {
#         "name": "张三",
#         "email": "zhangsan@example.com"
#     }
# }

# 测试2：必需 Cookie 参数
url2 = 'http://127.0.0.1:8000/api/user/settings'
cookies2 = {
    "session-id": "abc123xyz"
}

response2 = requests.get(url2, cookies=cookies2)
print("测试2（必需 Cookie）:", response2.json())

# 测试3：缺少 Cookie（会返回错误）
response3 = requests.get(url, cookies={})  # 不传 Cookie
print("测试3（缺少 Cookie）:", response3.json())
# 输出：{"error": "缺少 session_id Cookie"}
"""

# 方式2：使用 FastAPI 的 /docs 界面
"""
1. 启动服务器后，访问 http://127.0.0.1:8000/docs
2. 找到 GET /api/user/profile 接口
3. 点击 "Try it out"
4. 在 Cookies 部分，添加：
   - session-id: abc123xyz
   - user-token: token_xyz789
5. 点击 "Execute"
"""

# ============================================
# 重要说明
# ============================================

"""
1. Cookie 参数命名规则（和 Header 一样）：
   - Python 变量名：session_id（下划线）
   - HTTP Cookie 名：session-id（横线）
   - FastAPI 自动转换：session_id → session-id
   - 不区分大小写：session-id、Session-Id、SESSION-ID 都可以

2. Cookie 参数类型：
   - 可选：session_id: Annotated[str | None, Cookie()] = None
   - 必需：session_id: Annotated[str, Cookie()]  # 没有默认值

3. Cookie vs Header：
   - Cookie：浏览器自动管理，常用于会话管理
   - Header：需要手动设置，常用于认证令牌

4. 实际应用场景：
   - 会话管理（session_id）
   - 用户认证（user_token）
   - 购物车信息（cart_id）
   - 用户偏好设置（preferences）
"""

# ============================================
# 实际应用示例：购物车
# ============================================

"""
# 购物车示例
@app.get("/api/cart")
async def get_cart(
    cart_id: Annotated[str | None, Cookie()] = None
):
    if not cart_id:
        # 创建新购物车
        new_cart_id = "cart_12345"
        return {
            "cart_id": new_cart_id,
            "items": [],
            "提示": f"请设置 Cookie: cart-id={new_cart_id}"
        }
    
    # 根据 cart_id 查询购物车
    return {
        "cart_id": cart_id,
        "items": [
            {"product": "商品1", "quantity": 2},
            {"product": "商品2", "quantity": 1}
        ]
    }
"""


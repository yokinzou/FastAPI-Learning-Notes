"""
完整的创建用户 API 示例
演示如何使用请求体参数（Request Body Parameters）
"""

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# 1. 定义 Pydantic 模型（请求体结构）
class User(BaseModel):
    name: str                    # 必需字段：用户名
    email: str                   # 必需字段：邮箱
    age: Optional[int] = None   # 可选字段：年龄（默认为 None）
    phone: Optional[str] = None # 可选字段：电话（默认为 None）

# 2. 创建 FastAPI 应用
app = FastAPI()

# 3. 定义创建用户的端点
@app.post("/api/users/")
async def create_user(user: User):
    """
    创建新用户
    
    参数:
        user: 用户信息（请求体参数）
    
    返回:
        创建的用户信息
    """
    # 这里可以添加业务逻辑，比如保存到数据库
    # 现在只是返回接收到的数据
    
    return {
        "message": "用户创建成功",
        "user": {
            "name": user.name,
            "email": user.email,
            "age": user.age,
            "phone": user.phone
        }
    }

# 4. 启动服务器
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

url = 'http://127.0.0.1:8000/api/users/'

# 测试数据1：完整信息
data1 = {
    "name": "张三",
    "email": "zhangsan@example.com",
    "age": 25,
    "phone": "13800138000"
}

# 测试数据2：只传必需字段
data2 = {
    "name": "李四",
    "email": "lisi@example.com"
}

# 发送 POST 请求
response = requests.post(url, json=data1)
print(response.json())
"""

# 方式2：使用 FastAPI 的 /docs 界面
# 1. 启动服务器后，访问 http://127.0.0.1:8000/docs
# 2. 找到 POST /api/users/ 接口
# 3. 点击 "Try it out"
# 4. 在 Request body 中输入：
#    {
#      "name": "张三",
#      "email": "zhangsan@example.com",
#      "age": 25,
#      "phone": "13800138000"
#    }
# 5. 点击 "Execute"


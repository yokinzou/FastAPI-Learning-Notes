"""
完整的创建订单 API 示例
演示：嵌套模型（Nested Models）+ Header 参数
"""

import uvicorn
from fastapi import FastAPI, Header
from typing import Annotated
from pydantic import BaseModel

# 1. 创建 FastAPI 应用
app = FastAPI(title="订单管理系统", description="演示嵌套模型和 Header 参数")

# 2. 定义嵌套模型
class Address(BaseModel):
    """地址模型"""
    city: str
    street: str

class Order(BaseModel):
    """订单模型（包含嵌套的地址模型）"""
    product: str
    quantity: int
    address: Address  # 嵌套模型

# 3. 定义创建订单的端点
@app.post("/api/orders/")
async def create_order(
    order: Order,  # 请求体参数（嵌套模型）
    user_id: Annotated[str, Header()]  # Header 参数（从 HTTP Header 中读取）
):
    """
    创建新订单
    
    参数:
        order: 订单信息（请求体，包含嵌套的地址信息）
        user_id: 用户ID（从 HTTP Header 中读取，Header 名称为 user-id）
    
    返回:
        创建成功的订单信息
    """
    return {
        "message": "订单创建成功",
        "user_id": user_id,
        "order": {
            "product": order.product,
            "quantity": order.quantity,
            "address": {
                "city": order.address.city,
                "street": order.address.street
            }
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

url = 'http://127.0.0.1:8000/api/orders/'

# 请求体（嵌套模型）
data = {
    "product": "笔记本电脑",
    "quantity": 1,
    "address": {
        "city": "北京",
        "street": "中关村大街1号"
    }
}

# Header 参数测试
# FastAPI 自动转换规则：
# Python 变量名：user_id（下划线）
# HTTP Header 名：user-id（横线）
# 不区分大小写：user-id、User-Id、USER-ID 都可以

# 测试1：标准格式（推荐）
headers1 = {"user-id": "12345"}
response1 = requests.post(url, json=data, headers=headers1)
print("测试1（user-id）:", response1.json())

# 测试2：大写格式（也可以）
headers2 = {"User-Id": "12345"}
response2 = requests.post(url, json=data, headers=headers2)
print("测试2（User-Id）:", response2.json())

# 测试3：全大写格式（也可以）
headers3 = {"USER-ID": "12345"}
response3 = requests.post(url, json=data, headers=headers3)
print("测试3（USER-ID）:", response3.json())

# 所有测试都应该成功，因为 FastAPI 会自动匹配
"""

# 输出示例：
# {
#     "message": "订单创建成功",
#     "user_id": "12345",
#     "order": {
#         "product": "笔记本电脑",
#         "quantity": 1,
#         "address": {
#             "city": "北京",
#             "street": "中关村大街1号"
#         }
#     }
# }
"""

# 方式2：使用 FastAPI 的 /docs 界面
"""
1. 启动服务器后，访问 http://127.0.0.1:8000/docs
2. 找到 POST /api/orders/ 接口
3. 点击 "Try it out"
4. 在 Parameters 部分，找到 user-id（Header 参数）
   - 输入值：12345
5. 在 Request body 中输入：
   {
     "product": "笔记本电脑",
     "quantity": 1,
     "address": {
       "city": "北京",
       "street": "中关村大街1号"
     }
   }
6. 点击 "Execute"
"""

# ============================================
# 重要说明
# ============================================

"""
1. Header 参数命名规则（重要！）：
   - Python 变量名：user_id（下划线）
   - HTTP Header 名：user-id（横线）
   - FastAPI 自动转换：user_id → user-id
   - 不区分大小写：user-id、User-Id、USER-ID 都可以匹配
   
   示例：
   Python: user_id: Annotated[str, Header()]
   HTTP:   {"user-id": "12345"}  ✅ 匹配
           {"User-Id": "12345"}  ✅ 匹配
           {"USER-ID": "12345"}  ✅ 匹配

2. 嵌套模型：
   - Address 是独立的 BaseModel
   - Order 中包含 Address 类型的字段
   - 请求体是嵌套的 JSON 结构

3. 请求体结构：
   {
     "product": "商品名",
     "quantity": 数量,
     "address": {          ← 嵌套对象
       "city": "城市",
       "street": "街道"
     }
   }
"""


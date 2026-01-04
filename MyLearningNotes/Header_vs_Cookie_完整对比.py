"""
Header 参数 vs Cookie 参数完整对比
解释为什么需要 Header 参数，以及各种参数的对比
"""

# ============================================
# 为什么需要 Header 参数？
# ============================================

"""
Header 参数的必要性和优势：

1. 更灵活的控制
   - 可以手动设置和清除
   - 不受浏览器 Cookie 策略限制

2. 安全性更高
   - 不会被 JavaScript 自动访问（某些 Header）
   - 可以设置更严格的验证

3. 适合 API 认证
   - API Token、JWT Token 等
   - 适合服务间通信

4. 不受 Cookie 限制
   - Cookie 有大小限制（4KB）
   - Cookie 有域名限制
   - Cookie 有数量限制

5. 更明确的语义
   - Header 名称更清晰（如 Authorization、X-API-Key）
   - 符合 RESTful API 规范
"""

# ============================================
# Header vs Cookie 详细对比
# ============================================

"""
| 特性 | Header 参数 | Cookie 参数 |
|------|-----------|------------|
| 存储位置 | 不存储（每次请求手动设置） | 浏览器自动存储 |
| 自动发送 | ❌ 需要手动设置 | ✅ 浏览器自动发送 |
| 大小限制 | 无限制（理论上） | 4KB 限制 |
| 数量限制 | 无限制 | 每个域名约 50 个 |
| 安全性 | ✅ 更高（可设置 HttpOnly 等） | ⚠️ 可能被 XSS 攻击 |
| 适用场景 | API 认证、服务间通信 | 会话管理、用户偏好 |
| 跨域 | ✅ 可以（CORS 配置） | ⚠️ 受域名限制 |
| 手动控制 | ✅ 完全控制 | ❌ 浏览器控制 |
| 语义清晰 | ✅ 更清晰（Authorization） | ⚠️ 不够明确 |
"""

# ============================================
# 实际使用场景对比
# ============================================

"""
场景1：API 认证（使用 Header）
- 原因：需要手动控制，安全性高
- 示例：Authorization: Bearer token123

场景2：会话管理（使用 Cookie）
- 原因：浏览器自动管理，用户体验好
- 示例：session-id=abc123

场景3：服务间通信（使用 Header）
- 原因：不受浏览器限制，更灵活
- 示例：X-API-Key: key123

场景4：用户偏好（使用 Cookie）
- 原因：浏览器自动保存，持久化
- 示例：theme=dark, language=zh
"""

# ============================================
# 完整参数类型对比表
# ============================================

"""
| 参数类型 | 声明方式 | 数据来源 | 存储 | 自动发送 | 适用场景 |
|---------|---------|---------|------|---------|---------|
| 路径参数 | Path() | URL 路径 | ❌ | ✅ | 资源标识 |
| 查询参数 | Query() | URL 查询字符串 | ❌ | ✅ | 过滤、分页 |
| 请求体参数 | BaseModel | HTTP 请求体（JSON） | ❌ | ✅ | 创建/更新数据 |
| Cookie 参数 | Cookie() | HTTP Cookie 头 | ✅ 浏览器 | ✅ 自动 | 会话、偏好 |
| Header 参数 | Header() | HTTP Header 头 | ❌ | ❌ 手动 | 认证、元数据 |
| 表单参数 | Form() | HTTP 请求体（表单） | ❌ | ✅ | HTML 表单 |
| 文件参数 | File() | HTTP 请求体（文件） | ❌ | ✅ | 文件上传 |
"""

# ============================================
# Header 参数的实际应用场景
# ============================================

"""
1. API 认证（最常见）
   - Authorization: Bearer token
   - X-API-Key: key123
   - 原因：需要手动控制，安全性高

2. 请求元数据
   - X-Request-ID: 请求追踪
   - X-Client-Version: 客户端版本
   - 原因：传递请求相关信息

3. 服务间通信
   - X-Service-Name: 服务名称
   - X-Request-Source: 请求来源
   - 原因：不受浏览器限制

4. 内容协商
   - Accept: application/json
   - Content-Type: application/json
   - 原因：控制响应格式
"""

# ============================================
# Cookie 参数的实际应用场景
# ============================================

"""
1. 会话管理（最常见）
   - session-id: 会话标识
   - 原因：浏览器自动管理，用户体验好

2. 用户偏好
   - theme: 主题设置
   - language: 语言设置
   - 原因：持久化存储

3. 购物车
   - cart-id: 购物车标识
   - 原因：跨页面保持状态

4. 追踪信息
   - tracking-id: 追踪标识
   - 原因：用户行为分析
"""

# ============================================
# 完整代码示例对比
# ============================================

from fastapi import FastAPI, Header, Cookie
from typing import Annotated

app = FastAPI()

# ===== 场景1：API 认证（使用 Header） =====
@app.get("/api/protected")
async def protected_resource(
    authorization: Annotated[str, Header()]  # API Token
):
    """
    使用 Header 的原因：
    1. 需要手动控制（客户端代码设置）
    2. 安全性高（不会被 JavaScript 自动访问）
    3. 适合服务间通信
    """
    return {"message": "访问受保护资源", "token": authorization}


# ===== 场景2：会话管理（使用 Cookie） =====
@app.get("/api/user/profile")
async def user_profile(
    session_id: Annotated[str | None, Cookie()] = None  # 会话 ID
):
    """
    使用 Cookie 的原因：
    1. 浏览器自动管理（无需手动设置）
    2. 用户体验好（自动保存和发送）
    3. 适合 Web 应用
    """
    return {"session_id": session_id}


# ===== 场景3：混合使用 =====
@app.get("/api/data")
async def get_data(
    # Header：API 认证（手动控制）
    api_key: Annotated[str, Header()],
    # Cookie：用户偏好（浏览器管理）
    theme: Annotated[str | None, Cookie()] = None,
    # 查询参数：过滤条件
    limit: int = 10
):
    """
    混合使用不同参数类型：
    - Header：认证信息（手动控制）
    - Cookie：用户偏好（浏览器管理）
    - Query：过滤条件（URL 参数）
    """
    return {
        "api_key": api_key,
        "theme": theme,
        "limit": limit
    }


# ============================================
# 为什么 Header 和 Cookie 都需要？
# ============================================

"""
1. 不同的使用场景
   - Header：API 认证、服务间通信
   - Cookie：会话管理、用户偏好

2. 不同的控制方式
   - Header：手动控制，更灵活
   - Cookie：浏览器自动管理，更便捷

3. 不同的安全策略
   - Header：可以设置更严格的验证
   - Cookie：有 HttpOnly、SameSite 等安全选项

4. 不同的限制
   - Header：无大小和数量限制
   - Cookie：有大小（4KB）和数量限制

5. 符合标准规范
   - Header：符合 RESTful API 规范
   - Cookie：符合 HTTP Cookie 标准
"""

# ============================================
# 实际项目中的选择建议
# ============================================

"""
选择 Header 的情况：
✅ API 认证（Token、API Key）
✅ 服务间通信
✅ 请求元数据（Request ID、版本号）
✅ 需要手动控制的情况

选择 Cookie 的情况：
✅ 会话管理（Session ID）
✅ 用户偏好（主题、语言）
✅ 购物车信息
✅ 需要浏览器自动管理的情况

选择查询参数的情况：
✅ 过滤条件（status=active）
✅ 分页参数（limit=10, offset=0）
✅ 排序参数（sort_by=name）

选择路径参数的情况：
✅ 资源标识（/users/{user_id}）
✅ RESTful 资源路径
"""

# ============================================
# 完整对比总结
# ============================================

"""
参数类型选择指南：

1. 资源标识 → 路径参数（Path）
   /users/{user_id}

2. 过滤/分页 → 查询参数（Query）
   /users?status=active&limit=10

3. 创建/更新数据 → 请求体参数（BaseModel）
   POST /users/ {"name": "张三"}

4. API 认证 → Header 参数（Header）
   Authorization: Bearer token

5. 会话管理 → Cookie 参数（Cookie）
   session-id: abc123

6. HTML 表单 → 表单参数（Form）
   username=admin&password=123

7. 文件上传 → 文件参数（File）
   二进制文件数据
"""

if __name__ == "__main__":
    print("Header vs Cookie 完整对比说明")


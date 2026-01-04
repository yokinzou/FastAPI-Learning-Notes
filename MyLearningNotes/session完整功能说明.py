"""
session 完整功能说明
演示 session 不只是管理 Cookie，还有其他功能
"""

import requests

# ============================================
# session 的完整功能
# ============================================

"""
session 不只是管理 Cookie，还包括：

1. Cookie 管理（自动保存和发送）
2. 连接池（连接复用，提高性能）
3. 默认 Headers（可以设置默认请求头）
4. 认证信息（可以设置默认认证）
5. 超时设置（可以设置默认超时）
6. 其他会话级别的配置
"""

# ============================================
# 功能1：Cookie 管理（最常用）
# ============================================

def cookie_management():
    """Cookie 自动管理"""
    session = requests.Session()
    
    # 第一次请求：服务器设置 Cookie
    response1 = session.post('http://example.com/login', json={"user": "admin"})
    # Cookie 自动保存到 session.cookies
    
    # 后续请求：自动使用 Cookie
    response2 = session.get('http://example.com/profile')
    # 自动在请求头中添加 Cookie，无需手动传递


# ============================================
# 功能2：连接池（性能优化）
# ============================================

def connection_pooling():
    """连接复用，提高性能"""
    session = requests.Session()
    
    # 第一次请求：建立连接
    response1 = session.get('http://example.com/api/data1')
    
    # 第二次请求：复用之前的连接（更快！）
    response2 = session.get('http://example.com/api/data2')
    # 不需要重新建立 TCP 连接，直接复用
    
    # 而 requests.get() 每次都要建立新连接


# ============================================
# 功能3：默认 Headers
# ============================================

def default_headers():
    """设置默认请求头"""
    session = requests.Session()
    
    # 设置默认请求头（所有请求都会包含）
    session.headers.update({
        'User-Agent': 'MyApp/1.0',
        'Authorization': 'Bearer token123',
        'X-Custom-Header': 'value'
    })
    
    # 所有请求自动包含这些 Headers
    response1 = session.get('http://example.com/api/data1')
    response2 = session.get('http://example.com/api/data2')
    # 无需每次都设置 Headers


# ============================================
# 功能4：即使没有 Cookie，session 仍然有用
# ============================================

def session_without_cookie():
    """
    即使 API 没有设置 Cookie，session 仍然有用
    """
    session = requests.Session()
    
    # 设置默认 Headers（所有请求都会包含）
    session.headers.update({
        'Authorization': 'Bearer my_token',
        'Content-Type': 'application/json'
    })
    
    # 调用别人的 API（没有 Cookie）
    # 场景1：调用外部 API
    response1 = session.post(
        'https://api.example.com/users',
        json={"name": "张三"}
    )
    # ✅ 仍然有用：自动包含默认 Headers，连接复用
    
    # 场景2：继续调用同一个 API
    response2 = session.get('https://api.example.com/users/123')
    # ✅ 仍然有用：复用连接（更快），自动包含 Headers
    
    # 即使没有 Cookie，session 仍然有优势：
    # 1. 连接复用（性能更好）
    # 2. 默认 Headers（代码更简洁）
    # 3. 统一配置（便于管理）


# ============================================
# 实际对比：有 Cookie vs 没有 Cookie
# ============================================

def comparison_example():
    """对比示例"""
    
    # ===== 场景1：API 有 Cookie =====
    session1 = requests.Session()
    session1.post('http://api1.com/login', json={"user": "admin"})
    # Cookie 自动保存
    session1.get('http://api1.com/profile')
    # 自动使用 Cookie ✅
    
    # ===== 场景2：API 没有 Cookie =====
    session2 = requests.Session()
    session2.headers.update({'Authorization': 'Bearer token'})
    
    # 调用外部 API（没有 Cookie）
    session2.post('https://api2.com/users', json={"name": "张三"})
    # ✅ 仍然有用：
    # - 自动包含 Authorization Header
    # - 连接复用（如果多次调用）
    
    session2.get('https://api2.com/users/123')
    # ✅ 仍然有用：
    # - 自动包含 Authorization Header
    # - 复用连接（更快）


# ============================================
# 完整示例：调用外部 API（没有 Cookie）
# ============================================

def call_external_api():
    """调用外部 API 的完整示例"""
    
    session = requests.Session()
    
    # 1. 设置默认配置（所有请求都会使用）
    session.headers.update({
        'Authorization': 'Bearer your_api_token',
        'Content-Type': 'application/json',
        'User-Agent': 'MyApp/1.0'
    })
    
    # 2. 设置超时（可选）
    session.timeout = 10
    
    # 3. 调用外部 API（没有 Cookie）
    # 即使没有 Cookie，session 仍然有优势：
    
    # 请求1
    response1 = session.post(
        'https://api.github.com/user/repos',
        json={"name": "my-repo"}
    )
    # ✅ 自动包含 Authorization Header
    # ✅ 建立连接
    
    # 请求2（复用连接，更快）
    response2 = session.get('https://api.github.com/user')
    # ✅ 自动包含 Authorization Header
    # ✅ 复用之前的连接（性能更好）
    
    # 请求3（继续复用连接）
    response3 = session.get('https://api.github.com/user/repos')
    # ✅ 自动包含 Authorization Header
    # ✅ 复用连接（性能更好）


# ============================================
# session vs requests 完整对比
# ============================================

"""
| 特性 | requests.post() | session.post() |
|------|----------------|---------------|
| Cookie 管理 | ❌ 不自动保存 | ✅ 自动保存（如果有） |
| 连接复用 | ❌ 每次新连接 | ✅ 复用连接（更快） |
| 默认 Headers | ❌ 每次都要设置 | ✅ 设置一次，所有请求使用 |
| 没有 Cookie 时 | ⚠️ 功能相同 | ✅ 仍然有优势（连接复用、默认 Headers） |
| 有 Cookie 时 | ⚠️ 需要手动管理 | ✅ 自动管理 |
"""

# ============================================
# 使用建议
# ============================================

"""
1. 有 Cookie 的 API → 使用 session
   - 自动管理 Cookie
   - 连接复用
   - 默认 Headers

2. 没有 Cookie 的 API → 仍然可以使用 session
   - 连接复用（性能更好）
   - 默认 Headers（代码更简洁）
   - 统一配置（便于管理）

3. 单次请求 → 使用 requests.post()
   - 简单直接
   - 不需要会话管理

4. 多次请求 → 使用 session.post()
   - 无论有没有 Cookie
   - 都有性能和维护优势
"""

# ============================================
# 实际例子：调用 GitHub API（没有 Cookie）
# ============================================

def github_api_example():
    """调用 GitHub API 示例（没有 Cookie，但 session 仍然有用）"""
    
    session = requests.Session()
    
    # 设置认证 Header（所有请求都会包含）
    session.headers.update({
        'Authorization': 'token YOUR_GITHUB_TOKEN',
        'Accept': 'application/vnd.github.v3+json'
    })
    
    # 多次调用 GitHub API
    # 即使没有 Cookie，session 仍然有优势：
    
    # 1. 连接复用（更快）
    repos = session.get('https://api.github.com/user/repos')
    
    # 2. 自动包含认证 Header（无需每次设置）
    user = session.get('https://api.github.com/user')
    
    # 3. 继续复用连接
    orgs = session.get('https://api.github.com/user/orgs')
    
    # 所有请求都自动包含 Authorization Header
    # 所有请求都复用连接（性能更好）


if __name__ == "__main__":
    print("session 的完整功能说明")
    print("即使 API 没有 Cookie，session 仍然有用！")


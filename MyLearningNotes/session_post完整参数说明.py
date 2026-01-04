"""
session.post() 完整参数说明
演示 session 如何记住表头信息，以及 post() 的所有参数
"""

import requests

# ============================================
# 1. session 会记住表头信息吗？
# ============================================

"""
是的！session 会记住表头信息（Headers）

session 会记住：
1. Cookie（自动保存和发送）
2. Headers（默认 Headers）
3. 认证信息（auth）
4. 超时设置（timeout）
5. 其他会话级别的配置
"""

# ============================================
# session 记住 Headers 的示例
# ============================================

def session_remembers_headers():
    """session 会记住 Headers"""
    
    session = requests.Session()
    
    # 设置默认 Headers（所有请求都会包含）
    session.headers.update({
        'Authorization': 'Bearer token123',
        'Content-Type': 'application/json',
        'User-Agent': 'MyApp/1.0',
        'X-Custom-Header': 'value123'
    })
    
    # 第一次请求：自动包含所有 Headers
    response1 = session.post(
        'http://api.example.com/users',
        json={"name": "张三"}
    )
    # ✅ 自动包含：Authorization, Content-Type, User-Agent, X-Custom-Header
    
    # 第二次请求：继续自动包含所有 Headers
    response2 = session.get('http://api.example.com/users/123')
    # ✅ 自动包含：Authorization, User-Agent, X-Custom-Header
    # （GET 请求通常不需要 Content-Type）
    
    # 第三次请求：仍然自动包含
    response3 = session.post(
        'http://api.example.com/orders',
        json={"product": "商品"}
    )
    # ✅ 自动包含：Authorization, Content-Type, User-Agent, X-Custom-Header


# ============================================
# session.post() 完整参数列表
# ============================================

"""
session.post(url, **kwargs)

主要参数：

1. url (必需)
   - 请求的 URL
   - 示例：'http://api.example.com/users'

2. params (可选)
   - URL 查询参数（字典）
   - 示例：params={'limit': 10, 'offset': 0}
   - 结果：/users?limit=10&offset=0

3. data (可选)
   - 请求体数据（字典、字符串、文件）
   - 用于表单数据
   - 示例：data={'username': 'admin', 'password': '123'}

4. json (可选)
   - JSON 数据（字典）
   - 自动设置 Content-Type: application/json
   - 示例：json={"name": "张三", "age": 25}

5. headers (可选)
   - 请求头（字典）
   - 会与 session 的默认 Headers 合并
   - 示例：headers={'X-Request-ID': '123'}

6. cookies (可选)
   - Cookie（字典）
   - 会与 session 的 Cookie 合并
   - 示例：cookies={'session-id': 'abc123'}

7. files (可选)
   - 文件上传（字典）
   - 示例：files={'file': open('image.jpg', 'rb')}

8. auth (可选)
   - 认证信息（元组或认证对象）
   - 示例：auth=('username', 'password')
   - 或：auth=requests.auth.HTTPBasicAuth('user', 'pass')

9. timeout (可选)
   - 超时时间（秒）
   - 示例：timeout=10

10. allow_redirects (可选)
    - 是否允许重定向（默认 True）
    - 示例：allow_redirects=False

11. proxies (可选)
    - 代理设置（字典）
    - 示例：proxies={'http': 'http://proxy.example.com:8080'}

12. verify (可选)
    - 是否验证 SSL 证书（默认 True）
    - 示例：verify=False（不推荐，仅用于测试）

13. stream (可选)
    - 是否流式传输（默认 False）
    - 示例：stream=True（用于大文件下载）

14. cert (可选)
    - 客户端证书
    - 示例：cert=('/path/to/cert.pem', '/path/to/key.pem')
"""

# ============================================
# 完整示例：所有参数的使用
# ============================================

def complete_example():
    """完整的参数使用示例"""
    
    session = requests.Session()
    
    # 设置默认配置（所有请求都会使用）
    session.headers.update({
        'Authorization': 'Bearer default_token',
        'User-Agent': 'MyApp/1.0'
    })
    
    # 完整的 post() 调用
    response = session.post(
        # 1. url (必需)
        url='http://api.example.com/users',
        
        # 2. params - URL 查询参数
        params={
            'limit': 10,
            'offset': 0
        },
        # 结果：/users?limit=10&offset=0
        
        # 3. json - JSON 请求体
        json={
            'name': '张三',
            'age': 25
        },
        # 自动设置 Content-Type: application/json
        
        # 4. headers - 额外的请求头（会与默认 Headers 合并）
        headers={
            'X-Request-ID': 'req_123',
            'X-Custom-Header': 'custom_value'
        },
        # 最终 Headers：
        # - Authorization: Bearer default_token (来自 session)
        # - User-Agent: MyApp/1.0 (来自 session)
        # - X-Request-ID: req_123 (本次请求)
        # - X-Custom-Header: custom_value (本次请求)
        # - Content-Type: application/json (自动设置)
        
        # 5. cookies - 额外的 Cookie（会与 session Cookie 合并）
        cookies={
            'temp-token': 'temp_123'
        },
        
        # 6. timeout - 超时时间（秒）
        timeout=10,
        
        # 7. allow_redirects - 是否允许重定向
        allow_redirects=True,
        
        # 8. verify - 是否验证 SSL 证书
        verify=True,
        
        # 9. stream - 是否流式传输
        stream=False
    )
    
    return response


# ============================================
# session 记住的配置 vs 单次请求的参数
# ============================================

def session_vs_request_params():
    """session 配置 vs 单次请求参数"""
    
    session = requests.Session()
    
    # ===== session 级别的配置（所有请求都会使用）=====
    session.headers.update({
        'Authorization': 'Bearer token123',  # 所有请求都包含
        'User-Agent': 'MyApp/1.0'            # 所有请求都包含
    })
    session.timeout = 10  # 所有请求都使用
    session.cookies.set('session-id', 'abc123')  # 所有请求都包含
    
    # ===== 单次请求的参数（只影响本次请求）=====
    response = session.post(
        'http://api.example.com/users',
        
        # 本次请求的 Headers（会与 session Headers 合并）
        headers={
            'X-Request-ID': 'req_123'  # 只本次请求包含
        },
        
        # 本次请求的 JSON 数据
        json={'name': '张三'},
        
        # 本次请求的超时（会覆盖 session 的 timeout）
        timeout=5  # 只本次请求使用
    )
    
    # 最终请求包含：
    # Headers:
    #   - Authorization: Bearer token123 (来自 session)
    #   - User-Agent: MyApp/1.0 (来自 session)
    #   - X-Request-ID: req_123 (本次请求)
    #   - Content-Type: application/json (自动设置)
    # Cookies:
    #   - session-id: abc123 (来自 session)
    # Timeout: 5 (本次请求覆盖了 session 的 10)


# ============================================
# Headers 合并规则
# ============================================

def headers_merge_rules():
    """Headers 合并规则"""
    
    session = requests.Session()
    
    # session 的默认 Headers
    session.headers.update({
        'Authorization': 'Bearer default_token',
        'User-Agent': 'MyApp/1.0',
        'X-Common-Header': 'common_value'
    })
    
    # 单次请求的 Headers
    response = session.post(
        'http://api.example.com/users',
        headers={
            'Authorization': 'Bearer override_token',  # 会覆盖 session 的
            'X-Request-ID': 'req_123'                  # 新增的
        }
    )
    
    # 最终 Headers：
    # - Authorization: Bearer override_token (本次请求覆盖)
    # - User-Agent: MyApp/1.0 (来自 session)
    # - X-Common-Header: common_value (来自 session)
    # - X-Request-ID: req_123 (本次请求新增)
    # - Content-Type: application/json (自动设置)


# ============================================
# 常用参数组合示例
# ============================================

def common_combinations():
    """常用参数组合"""
    
    session = requests.Session()
    
    # ===== 组合1：JSON 数据 + 自定义 Headers =====
    response1 = session.post(
        'http://api.example.com/users',
        json={'name': '张三'},
        headers={'X-Request-ID': 'req_123'}
    )
    
    # ===== 组合2：表单数据 =====
    response2 = session.post(
        'http://api.example.com/login',
        data={'username': 'admin', 'password': '123456'}
    )
    
    # ===== 组合3：文件上传 =====
    response3 = session.post(
        'http://api.example.com/upload',
        files={'file': open('image.jpg', 'rb')}
    )
    
    # ===== 组合4：查询参数 + JSON 数据 =====
    response4 = session.post(
        'http://api.example.com/users',
        params={'version': 'v1'},
        json={'name': '张三'}
    )
    # URL: /users?version=v1
    # Body: {"name": "张三"}


# ============================================
# 参数优先级总结
# ============================================

"""
参数优先级（从高到低）：

1. 单次请求的参数（最高优先级）
   - 会覆盖 session 的默认配置
   - 示例：headers={'Authorization': 'new_token'}

2. session 的默认配置
   - 所有请求都会使用
   - 示例：session.headers.update({'Authorization': 'default_token'})

3. requests 的默认行为
   - 自动设置 Content-Type（使用 json 参数时）
   - 自动处理 Cookie
"""

# ============================================
# 完整对比表
# ============================================

"""
| 配置类型 | session 级别 | 单次请求级别 | 优先级 |
|---------|------------|------------|--------|
| Headers | session.headers | headers 参数 | 单次请求 > session |
| Cookies | session.cookies | cookies 参数 | 合并 |
| Timeout | session.timeout | timeout 参数 | 单次请求 > session |
| Auth | session.auth | auth 参数 | 单次请求 > session |
| Proxies | session.proxies | proxies 参数 | 单次请求 > session |
"""

# ============================================
# 实际使用建议
# ============================================

"""
1. 使用 session 级别的配置：
   ✅ 所有请求都需要的 Headers（如 Authorization）
   ✅ 所有请求都需要的 Cookie（如 session-id）
   ✅ 统一的超时设置
   ✅ 统一的认证信息

2. 使用单次请求的参数：
   ✅ 本次请求特有的 Headers（如 X-Request-ID）
   ✅ 本次请求的请求体（json、data、files）
   ✅ 本次请求的查询参数（params）
   ✅ 需要覆盖默认配置的情况

3. 最佳实践：
   - 通用配置 → session 级别
   - 特定配置 → 单次请求级别
"""

if __name__ == "__main__":
    print("session.post() 完整参数说明")
    print("session 会记住 Headers、Cookies 等配置！")


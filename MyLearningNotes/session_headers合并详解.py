"""
session Headers 合并详解
解释为什么 session 记住了 Headers，还要在单次请求中传 headers 参数
"""

import requests

# ============================================
# 核心理解：通用 vs 特定
# ============================================

"""
session 记住的是：通用的、所有请求都需要的 Headers
单次请求传的是：本次请求特有的、需要覆盖的 Headers

类比：
- session Headers = 公司统一的工作服（所有人都有）
- 单次请求 Headers = 个人名牌（每个人不同）
"""

# ============================================
# 场景1：通用 Headers（session 记住）
# ============================================

def common_headers():
    """通用 Headers - 所有请求都需要"""
    
    session = requests.Session()
    
    # 这些 Headers 所有请求都需要，所以放在 session 中
    session.headers.update({
        'Authorization': 'Bearer token123',  # 所有请求都需要认证
        'User-Agent': 'MyApp/1.0',            # 所有请求都需要标识
        'Accept': 'application/json'          # 所有请求都接受 JSON
    })
    
    # 请求1：自动包含通用 Headers
    response1 = session.post('http://api.com/users', json={'name': '张三'})
    # ✅ 自动包含：Authorization, User-Agent, Accept
    
    # 请求2：自动包含通用 Headers
    response2 = session.get('http://api.com/users/123')
    # ✅ 自动包含：Authorization, User-Agent, Accept
    
    # 请求3：自动包含通用 Headers
    response3 = session.post('http://api.com/orders', json={'product': '商品'})
    # ✅ 自动包含：Authorization, User-Agent, Accept
    
    # 优势：不需要每次都写这些 Headers，代码更简洁！


# ============================================
# 场景2：特定 Headers（单次请求传）
# ============================================

def specific_headers():
    """特定 Headers - 每次请求都不同"""
    
    session = requests.Session()
    
    # 通用 Headers（session 记住）
    session.headers.update({
        'Authorization': 'Bearer token123',
        'User-Agent': 'MyApp/1.0'
    })
    
    # 请求1：需要请求追踪 ID（每次请求都不同）
    response1 = session.post(
        'http://api.com/users',
        json={'name': '张三'},
        headers={'X-Request-ID': 'req_001'}  # 本次请求特有的
    )
    # 最终 Headers：
    # - Authorization: Bearer token123 (来自 session)
    # - User-Agent: MyApp/1.0 (来自 session)
    # - X-Request-ID: req_001 (本次请求)
    
    # 请求2：需要不同的请求追踪 ID
    response2 = session.post(
        'http://api.com/users',
        json={'name': '李四'},
        headers={'X-Request-ID': 'req_002'}  # 每次请求都不同！
    )
    # 最终 Headers：
    # - Authorization: Bearer token123 (来自 session)
    # - User-Agent: MyApp/1.0 (来自 session)
    # - X-Request-ID: req_002 (本次请求，不同！)
    
    # 为什么不能放在 session 中？
    # ❌ 因为每次请求的 X-Request-ID 都不同！
    # ✅ 所以必须每次请求单独传


# ============================================
# 场景3：覆盖 session 的 Headers
# ============================================

def override_headers():
    """覆盖 session 的 Headers"""
    
    session = requests.Session()
    
    # session 的默认认证
    session.headers.update({
        'Authorization': 'Bearer default_token',
        'User-Agent': 'MyApp/1.0'
    })
    
    # 请求1：使用默认认证
    response1 = session.post('http://api.com/users', json={'name': '张三'})
    # ✅ 使用：Authorization: Bearer default_token
    
    # 请求2：需要不同的认证（覆盖 session 的）
    response2 = session.post(
        'http://api.com/admin/users',
        json={'name': '管理员'},
        headers={'Authorization': 'Bearer admin_token'}  # 覆盖 session 的
    )
    # ✅ 使用：Authorization: Bearer admin_token（覆盖了默认的）
    
    # 为什么需要覆盖？
    # 因为不同接口可能需要不同的认证方式！


# ============================================
# 完整示例：为什么两者都需要
# ============================================

def why_both_needed():
    """为什么 session 和单次请求都需要"""
    
    session = requests.Session()
    
    # ===== session 记住的（通用、固定的）=====
    session.headers.update({
        'Authorization': 'Bearer token123',  # 所有请求都需要
        'User-Agent': 'MyApp/1.0',          # 所有请求都需要
        'Accept': 'application/json'        # 所有请求都需要
    })
    
    # ===== 单次请求传的（特定、变化的）=====
    
    # 请求1：创建用户
    response1 = session.post(
        'http://api.com/users',
        json={'name': '张三'},
        headers={
            'X-Request-ID': 'req_001',        # 每次请求都不同
            'X-Operation': 'create_user'     # 本次操作特有
        }
    )
    
    # 请求2：更新用户
    response2 = session.put(
        'http://api.com/users/123',
        json={'name': '李四'},
        headers={
            'X-Request-ID': 'req_002',        # 每次请求都不同
            'X-Operation': 'update_user'     # 本次操作特有
        }
    )
    
    # 最终每个请求的 Headers：
    # ✅ 通用部分（来自 session）：
    #    - Authorization: Bearer token123
    #    - User-Agent: MyApp/1.0
    #    - Accept: application/json
    # ✅ 特定部分（来自单次请求）：
    #    - X-Request-ID: req_001/req_002（每次不同）
    #    - X-Operation: create_user/update_user（每次不同）


# ============================================
# 实际项目中的使用模式
# ============================================

def real_world_pattern():
    """实际项目中的使用模式"""
    
    session = requests.Session()
    
    # ===== 放在 session 中的（通用配置）=====
    session.headers.update({
        'Authorization': 'Bearer company_token',  # 公司统一的认证
        'User-Agent': 'CompanyApp/1.0',         # 应用标识
        'Accept': 'application/json',            # 统一接受 JSON
        'X-Company-ID': 'company_123'            # 公司标识
    })
    
    # ===== 每次请求单独传的（请求特定）=====
    
    import uuid
    
    # 请求1：创建订单
    request_id_1 = str(uuid.uuid4())  # 生成唯一 ID
    response1 = session.post(
        'http://api.com/orders',
        json={'product': '商品1'},
        headers={
            'X-Request-ID': request_id_1,      # 每次请求都不同
            'X-Operation': 'create_order',      # 本次操作
            'X-Client-IP': '192.168.1.1'      # 本次请求的 IP
        }
    )
    
    # 请求2：查询订单
    request_id_2 = str(uuid.uuid4())  # 生成新的唯一 ID
    response2 = session.get(
        'http://api.com/orders/123',
        headers={
            'X-Request-ID': request_id_2,      # 每次请求都不同
            'X-Operation': 'get_order'         # 本次操作
        }
    )
    
    # 为什么这样设计？
    # 1. 通用配置 → session（代码简洁，统一管理）
    # 2. 特定配置 → 单次请求（灵活，每次不同）


# ============================================
# 对比：如果不用 session 会怎样？
# ============================================

def without_session():
    """如果不用 session，每次都要写所有 Headers"""
    
    # ❌ 方式1：不用 session（代码重复）
    response1 = requests.post(
        'http://api.com/users',
        json={'name': '张三'},
        headers={
            'Authorization': 'Bearer token123',  # 每次都要写
            'User-Agent': 'MyApp/1.0',          # 每次都要写
            'Accept': 'application/json',       # 每次都要写
            'X-Request-ID': 'req_001'           # 本次请求特有的
        }
    )
    
    response2 = requests.post(
        'http://api.com/users',
        json={'name': '李四'},
        headers={
            'Authorization': 'Bearer token123',  # 重复！
            'User-Agent': 'MyApp/1.0',          # 重复！
            'Accept': 'application/json',       # 重复！
            'X-Request-ID': 'req_002'           # 本次请求特有的
        }
    )
    
    # ✅ 方式2：使用 session（代码简洁）
    session = requests.Session()
    session.headers.update({
        'Authorization': 'Bearer token123',  # 写一次
        'User-Agent': 'MyApp/1.0',            # 写一次
        'Accept': 'application/json'          # 写一次
    })
    
    response1 = session.post(
        'http://api.com/users',
        json={'name': '张三'},
        headers={'X-Request-ID': 'req_001'}  # 只写特定的
    )
    
    response2 = session.post(
        'http://api.com/users',
        json={'name': '李四'},
        headers={'X-Request-ID': 'req_002'}  # 只写特定的
    )


# ============================================
# 总结：为什么两者都需要
# ============================================

"""
session Headers（记住的）：
✅ 通用的、所有请求都需要的
✅ 固定的、不会变化的
✅ 示例：Authorization, User-Agent, Accept

单次请求 Headers（传的参数）：
✅ 特定的、每次请求都不同的
✅ 变化的、需要覆盖的
✅ 示例：X-Request-ID, X-Operation, X-Client-IP

类比：
- session Headers = 公司统一的工作服（所有人都有）
- 单次请求 Headers = 个人名牌（每个人不同）

优势：
1. 代码简洁（通用配置写一次）
2. 灵活（特定配置每次不同）
3. 易维护（统一管理通用配置）
"""

# ============================================
# 快速记忆
# ============================================

"""
session.headers = 通用的、固定的（写一次，所有请求都用）
单次请求 headers = 特定的、变化的（每次请求都不同）

就像：
- 公司统一的工作服（session）
- 个人名牌（单次请求）
"""

if __name__ == "__main__":
    print("session Headers 合并详解")
    print("session 记住通用的，单次请求传特定的！")


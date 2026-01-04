# FastAPI My Learning Notes 

## 📚 目录
- [第1章：URL参数](#第1章url参数)
- [第2章：请求体参数](#第2章请求体参数)
- [第3章：响应](#第3章响应)
- [第4章：表单和文件](#第4章表单和文件)
- [第5章：依赖注入](#第5章依赖注入)
- [第6章：FastAPI MCP](#第6章fastapi-mcp)
- [补充知识：requests 库](#补充知识requests-库)
- [项目目录结构](#项目目录结构)

---

## 第1章：URL参数

### 1.1 路径参数（Path Parameters）

**核心概念：**
- 路径参数是 URL 路径中的变量
- 例如：`/users/{user_id}` 中的 `{user_id}` 是路径参数

**基本用法：**
```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

**要点：**
- 路径参数用于标识资源
- FastAPI 自动进行类型转换和验证
- 使用 `Path()` 可以添加校验（如 `ge=5` 表示 >= 5）

**枚举类型（Enum）：**
```python
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    return {"model_name": model_name}
```

**要点：**
- `class ModelName(str, Enum)` 表示既是 Enum 也是 str
- 限制可选值，提高安全性
- 自动验证，不在枚举中的值会返回 422 错误

**❓ 问题：Enum 既是 str 也是 Enum？**

**A:** 
- `class ModelName(str, Enum)` 使用了多重继承
- 既是 Enum（具有枚举特性），也是 str（可以当作字符串使用）
- 继承 `str` 是为了可以直接当字符串用，不需要 `.value`
- 验证：`isinstance(ModelName.alexnet, Enum)` → True，`isinstance(ModelName.alexnet, str)` → True

### 1.2 查询参数（Query Parameters）

**核心概念：**
- 查询参数是 URL 中 `?` 后面的键值对
- 用于过滤、分页、排序等

**基本用法：**
```python
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

**三种类型：**
1. **默认参数**：`skip: int = 0` - 有默认值，可选
2. **必需参数**：`skip: int` - 没有默认值，必须传
3. **可选参数**：`skip: int | None = None` - 可以是 None

**要点：**
- 查询参数不是路径的固定部分，可以是可选的
- 不定义分页参数 = 不支持分页
- 如果定义了分页参数，用户不传会使用默认值

**❓ 问题：路径参数和查询参数的区别？**

**A:** 
- **路径参数**：在 URL 路径中，用于标识资源。例如：`/users/{user_id}`
- **查询参数**：在 URL 查询字符串中，用于过滤、分页。例如：`/users?limit=10&offset=0`
- **本质区别**：
  - 路径参数 = 地址（告诉服务器"哪个资源"）
  - 查询参数 = 条件（告诉服务器"如何过滤/分页"）

**❓ 问题：skip 和 limit 在 API 设计时一定要定义吗？**

**A:**
- 不是必须的，分页参数是可选的
- 如果不需要分页，就不定义分页参数
- 如果不定义，用户传了分页参数会被忽略
- 如果定义了，用户不传会使用默认值

### 1.3 路径参数校验

**使用 `Path()` 进行校验：**
```python
from typing import Annotated
from fastapi import Path

@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(ge=5)]  # 必须 >= 5
):
    return {"item_id": item_id}
```

**常用校验：**
- `gt=5`：大于 5
- `ge=5`：大于等于 5
- `lt=10`：小于 10
- `le=10`：小于等于 10

### 1.4 查询参数校验

**使用 `Query()` 进行校验：**
```python
from fastapi import Query

@app.get("/items/")
async def read_items(
    q: str | None = Query(default=None, min_length=3, max_length=5)
):
    return {"q": q}
```

**常用校验：**
- `min_length=3`：最少3个字符
- `max_length=5`：最多5个字符
- `pattern="^test.?$"`：正则表达式
- 数值校验：`limit: int = Query(ge=1, le=100)`

---

## 第2章：请求体参数

### 2.1 请求体参数（Request Body Parameters）

**核心概念：**
- FastAPI 自动识别参数类型：
  1. 路径参数：在路径中 `{item_id}`
  2. 查询参数：不在路径中的单个参数
  3. 请求体参数：Pydantic 模型（BaseModel）

**基本用法：**
```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int | None = None

@app.post("/users/")
async def create_user(user: User):
    return user
```

**要点：**
- `BaseModel` 是 Pydantic 的模型基类
- 继承 `BaseModel` 后获得数据验证、类型转换等功能
- 请求体参数在 HTTP 请求的 body 中（不是 URL）

**BaseModel 官方定义：**
- `BaseModel` 是 Pydantic 库中的基类
- 用于定义数据模型，自动进行数据验证和转换
- 可以看作类似 C 语言中的结构体

**❓ 问题：BaseModel 是什么？**

**A:**
- `BaseModel` 是 Pydantic 的模型基类
- 继承 `BaseModel` 后获得数据验证、类型转换等功能
- 用于定义请求体和响应体的数据结构
- 实际实现使用元类（Metaclass），在类定义时处理字段，自动生成验证器

**❓ 问题：请求体参数和路径参数的本质区别？**

**A:**
- **位置不同**：路径参数在 URL 路径中，请求体参数在 HTTP 请求体中
- **用途不同**：路径参数标识资源（哪个资源），请求体参数传递数据（要创建/更新的内容）
- **数据量不同**：路径参数简单（单个值），请求体参数可以很复杂（对象、数组等）
- **类比**：路径参数 = 门牌号，请求体参数 = 搬家时的物品清单

### 2.2 额外参数信息（Field）

**使用 `Field` 添加校验和元数据：**
```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str
    price: float = Field(gt=0, description="价格必须大于0")
    description: str | None = Field(default=None, max_length=300)
```

**要点：**
- `Field` 从 `pydantic` 导入（不是 `fastapi`）
- 可以添加校验（`gt`、`max_length` 等）和描述

### 2.3 嵌套模型（Nested Models）

**基本用法：**
```python
class Address(BaseModel):
    city: str
    street: str

class Order(BaseModel):
    product: str
    quantity: int
    address: Address  # 嵌套模型
```

**列表嵌套：**
```python
class Order(BaseModel):
    name: str
    images: list[Image] | None = None  # 嵌套模型列表
```

### 2.4 Cookie 参数

**基本用法：**
```python
from fastapi import Cookie
from typing import Annotated

@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}
```

**要点：**
- Cookie 存储在浏览器中（客户端）
- 浏览器自动在每个请求中发送 Cookie
- FastAPI 从请求头的 `Cookie` 字段中读取
- 命名转换：`session_id` → `session-id`（下划线变横线）

### 2.5 Header 参数

**基本用法：**
```python
from fastapi import Header
from typing import Annotated

@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}
```

**要点：**
- Header 参数从 HTTP Header 头中读取
- 命名转换：`user_id` → `user-id`（下划线变横线）
- 不区分大小写：`user-id`、`User-Id`、`USER-ID` 都可以
- 适合 API 认证、元数据传递

**Header vs Cookie 对比：**
| 特性 | Header 参数 | Cookie 参数 |
|------|-----------|------------|
| 存储位置 | 不存储（每次手动设置） | 浏览器自动存储 |
| 自动发送 | ❌ 需要手动设置 | ✅ 浏览器自动发送 |
| 适用场景 | API 认证、服务间通信 | 会话管理、用户偏好 |

**❓ 问题：Cookie 参数和 Header 参数的区别？**

**A:**
| 特性 | Header 参数 | Cookie 参数 |
|------|-----------|------------|
| 存储位置 | 不存储（每次手动设置） | 浏览器自动存储 |
| 自动发送 | ❌ 需要手动设置 | ✅ 浏览器自动发送 |
| 大小限制 | 无限制 | 4KB 限制 |
| 适用场景 | API 认证、服务间通信 | 会话管理、用户偏好 |
| 安全性 | ✅ 更高 | ⚠️ 可能被 XSS 攻击 |

**为什么两者都需要？**
- 不同场景：Header 用于 API 认证，Cookie 用于会话管理
- 不同控制：Header 手动控制，Cookie 浏览器自动管理
- 不同限制：Header 无大小限制，Cookie 有 4KB 限制

**❓ 问题：Cookie 是存在浏览器中吗？FastAPI 如何读取？**

**A:**
- 是的，Cookie 存储在浏览器中（客户端）
- 浏览器自动在每个请求中发送 Cookie
- FastAPI 从 HTTP 请求头的 `Cookie` 字段中读取
- 流程：服务器设置 Cookie → 浏览器存储 → 浏览器自动发送 → FastAPI 读取

**❓ 问题：Header 的 user-id 是带横线，函数定义的字段是下划线，能成功读取吗？**

**A:**
- 可以，FastAPI 会自动转换
- Python 变量名：`user_id`（下划线）→ HTTP Header 名：`user-id`（横线）
- 不区分大小写：`user-id`、`User-Id`、`USER-ID` 都可以匹配
- 这是 FastAPI 的自动转换机制

**❓ 问题：Annotated[str, Header()] 是什么意思？**

**A:**
- `Annotated[类型, 元数据]` 是 Python 3.9+ 的类型注解语法
- 第一个参数是类型（`str`），后面的参数是元数据（`Header()`）
- 含义：类型是 `str`，并且是 Header 参数
- 不是"或者"的关系，而是"类型 + 参数类型"的组合

---

## 第3章：响应

### 3.1 响应模型（Response Models）

**核心概念：**
- 使用 `response_model` 定义返回数据的结构
- 自动过滤未在响应模型中声明的字段

**基本用法：**
```python
class UserIn(BaseModel):
    username: str
    password: str  # 输入需要密码

class UserOut(BaseModel):
    username: str
    # 输出不包含密码！

@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user  # 自动过滤掉 password
```

**要点：**
- `response_model` 是装饰器参数（不是函数参数）
- 用于隐藏敏感信息（如密码）
- 自动生成 API 文档

### 3.2 多个模型（Multiple Models）

**使用继承减少重复：**
```python
class UserBase(BaseModel):
    username: str
    email: str

class UserIn(UserBase):
    password: str  # 输入需要密码

class UserOut(UserBase):
    pass  # 输出不包含密码

class UserInDB(UserBase):
    hashed_password: str  # 数据库存储哈希密码
```

**Union 模型（多种可能的响应）：**
```python
from typing import Union

@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]
```

**列表响应：**
```python
@app.get("/items/", response_model=list[Item])
async def read_items():
    return items
```

### 3.3 响应状态码（Status Codes）

**基本用法：**
```python
from fastapi import status

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
```

**常用状态码：**
| 状态码 | 含义 | 使用场景 |
|--------|------|---------|
| 200 | OK | 成功（默认） |
| 201 | Created | 创建成功 |
| 204 | No Content | 成功但无响应体 |
| 400 | Bad Request | 请求格式错误 |
| 404 | Not Found | 资源不存在 |
| 422 | Unprocessable Entity | 参数验证失败（FastAPI 自动返回） |
| 500 | Internal Server Error | 服务器内部错误 |

**要点：**
- 不写状态码 = 默认 `200 OK`
- 写状态码 = 明确语义（如创建用 `201`）
- 创建资源建议用 `201`，其他用默认 `200`

**❓ 问题：写状态码和不写状态码的区别？**

**A:**
- 不写状态码 = 默认 `200 OK`（通用成功）
- 写状态码 = 明确语义（如创建用 `201 Created`）
- 建议：创建资源用 `201`，其他用默认 `200`
- API 文档中会显示不同的状态码

**❓ 问题：状态码 400、404、500 的区别？**

**A:**
- **400 Bad Request**：请求格式错误（JSON 格式错误、参数类型错误）
- **404 Not Found**：URL 错误或资源不存在（数据库查询为空）
- **422 Unprocessable Entity**：参数验证失败（FastAPI 自动返回）
- **500 Internal Server Error**：服务器内部错误（代码 bug、数据库失败等）

**注意：**
- 路径参数或请求体参数不对 → 422（FastAPI 自动返回），不是 500
- 400 是客户端错误，500 是服务器错误

**❓ 问题：response.status_code 是 request 还是 response 的属性？**

**A:**
- 是 `response.status_code`，不是 request
- `response` 是 Response 对象（服务器返回的数据）
- 返回 HTTP 状态码（如 200、201、404）
- 使用：`response = requests.get(url)` → `response.status_code`

---

## 第4章：表单和文件

### 4.1 表单数据（Form Data）

**基本用法：**
```python
from fastapi import Form

@app.post("/login/")
async def login(
    username: str = Form(),
    password: str = Form()
):
    return {"username": username}
```

**要点：**
- 需要安装：`pip install python-multipart`
- 必须显式使用 `Form()`，否则会被当作查询参数
- 编码类型：`application/x-www-form-urlencoded`

### 4.2 请求文件（File Upload）

**基本用法：**
```python
from fastapi import UploadFile

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
```

**UploadFile 的属性：**
- `file.filename` - 文件名（str）
- `file.content_type` - MIME 类型（str）
- `file.file` - 文件对象（可读取内容）

**读取文件内容：**
```python
# 在 async 函数中
contents = await file.read()

# 在普通函数中
contents = file.file.read()
```

**多文件上传：**
```python
@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}
```

### 4.3 表单 + 文件

**基本用法：**
```python
from fastapi import File, Form, UploadFile

@app.post("/files/")
async def create_file(
    file: UploadFile = File(),
    token: str = Form()
):
    return {
        "token": token,
        "file_name": file.filename
    }
```

**要点：**
- 可以同时使用 `File()` 和 `Form()`
- 不能同时使用 `BaseModel`（JSON）和 `Form/File`
- 编码类型：`multipart/form-data`

---

## 第5章：依赖注入

### 5.1 依赖项（Dependencies）

**核心概念：**
- 依赖注入用于代码复用
- 将共享逻辑提取为依赖项

**基本用法：**
```python
from fastapi import Depends

async def common_parameters(
    q: str | None = None,
    skip: int = 0,
    limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons
```

**要点：**
- `Depends()` 声明依赖项
- 依赖项是普通函数
- 可以复用相同的逻辑
- `q` 是查询参数，从 URL 的 `?q=值` 中读取

**使用场景：**
- 共享业务逻辑（分页、过滤）
- 共享数据库连接
- 认证和权限验证
- 减少代码重复

### 5.2 类作为依赖项

**使用类代替函数：**
```python
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends()):
    return commons
```

**要点：**
- 类也是可调用对象
- 更好的类型提示和代码补全
- 推荐写法：`commons: CommonQueryParams = Depends()`

### 5.3 子依赖项（Sub-dependencies）

**依赖项可以依赖其他依赖项：**
```python
def query_extractor(q: str | None = None):
    return q

def query_or_cookie_extractor(
    q: str = Depends(query_extractor),  # 依赖其他依赖项
    last_query: str | None = "last query"
):
    if not q:
        return last_query
    return q

@app.get("/items/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_query": query_or_default}
```

**要点：**
- 依赖项可以嵌套
- FastAPI 自动处理依赖关系
- 同一请求中，相同依赖项只调用一次（缓存）

### 5.4 路径装饰器依赖项

**不需要返回值的依赖项：**
```python
async def verify_token(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token invalid")

@app.get("/items/", dependencies=[Depends(verify_token)])
async def read_items():
    return [{"item": "Foo"}]
```

**要点：**
- 在装饰器中声明：`dependencies=[Depends(...)]`
- 不需要在函数参数中使用
- 适合认证、验证等场景

### 5.5 全局依赖项

**应用到所有路径操作：**
```python
async def verify_token(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token invalid")

app = FastAPI(dependencies=[Depends(verify_token)])

@app.get("/items/")
async def read_items():
    return [{"item": "Foo"}]
```

**要点：**
- 在创建 FastAPI 应用时声明
- 所有路径操作都会执行
- 适合全局认证、日志等

**❓ 问题：HTTPBearer() 会自动弹出登录页面吗？如何获取 token？**

**A:**
- 不会，`HTTPBearer()` 只是定义了一种认证方式
- 需要客户端在请求头中提供 token：`Authorization: Bearer token`
- 获取 token 的方式：
  1. 登录接口（用户名密码）→ 返回 token
  2. API Key 注册 → 生成 API Key
  3. OAuth2 流程 → 第三方登录
- 流程：登录获取 token → 存到 session.headers → 后续请求自动包含

**❓ 问题：依赖项中的 `q` 是什么？**

**A:**
- `q` 是查询参数（Query Parameter）
- 从 URL 的查询字符串中读取：`/items/?q=张三`
- 依赖项函数可以接收和路径操作函数相同的参数类型（Query、Path、Header 等）
- `q` 通常表示搜索关键词（query）

---

## 第6章：FastAPI MCP

### 6.1 FastAPI MCP 基础

**什么是 MCP？**
- MCP（Model Context Protocol，模型上下文协议）
- 让 AI 助手（如 Claude）可以直接调用你的 FastAPI API

**基本用法：**
```python
from fastapi_mcp import FastApiMCP

app = FastAPI()

# 创建 MCP 服务
mcp = FastApiMCP(app)
mcp.mount()  # 挂载到应用
```

**要点：**
- 安装：`pip install fastapi-mcp`
- 自动将 API 转换为 MCP 工具
- AI 助手可以直接调用

**身份认证：**
```python
from fastapi_mcp import FastApiMCP, AuthConfig
from fastapi.security import HTTPBearer

token_auth_scheme = HTTPBearer()

mcp = FastApiMCP(
    app,
    auth_config=AuthConfig(
        dependencies=[Depends(token_auth_scheme)]
    )
)
```

### 6.2 实现天气查询 MCP

**实战项目示例：**
- 整合了前面所有知识
- 路径参数、查询参数、请求体参数
- 响应模型、依赖注入、Header 参数

---

## 补充知识：requests 库

### session.post() vs requests.post()

**❓ 问题：session.post() 和 requests.post() 的区别？**

**A:**
- `session.post()` 会记住 Cookie、Headers 等配置，自动管理
- `requests.post()` 每次都是新请求，需要手动传递 Cookie
- `session` 还会复用连接，性能更好
- 使用场景：
  - 多次请求（需要 Cookie）→ 使用 `session`
  - 单次请求 → 使用 `requests.post()`

**❓ 问题：session 会记住 Headers 吗？**

**A:**
- 是的，`session` 会记住 Headers
- `session.headers.update()` 设置的 Headers 会在所有请求中自动包含
- 单次请求的 `headers` 参数会与 session 的 Headers 合并
- 优先级：单次请求参数 > session 配置

**❓ 问题：为什么 session 记住了 Headers，还要在 post() 中传 headers 参数？**

**A:**
- session 记住的是**通用的、固定的** Headers（如 Authorization）
- 单次请求传的是**特定的、变化的** Headers（如 X-Request-ID，每次请求都不同）
- 两者合并形成最终请求的 Headers
- 类比：session Headers = 公司统一的工作服，单次请求 Headers = 个人名牌

**❓ 问题：session 只会记住 Cookie 吗？**

**A:**
- 不是，session 会记住：
  1. Cookie（自动保存和发送）
  2. Headers（默认 Headers）
  3. 连接池（连接复用，提高性能）
  4. 认证信息（auth）
  5. 超时设置（timeout）
- 即使 API 没有 Cookie，session 仍然有用（连接复用、默认 Headers）

**❓ 问题：post() 函数可以填的参数都有哪些？**

**A:**
主要参数：
- `url`（必需）- 请求 URL
- `json` - JSON 请求体
- `data` - 表单数据
- `headers` - 请求头
- `cookies` - Cookie
- `params` - URL 查询参数
- `files` - 文件上传
- `timeout` - 超时时间
- `auth` - 认证信息
- `allow_redirects` - 是否允许重定向
- `verify` - 是否验证 SSL

**❓ 问题：json=xxx 后面的就默认代表是请求体？**

**A:**
- 是的，`json=xxx` 就是请求体
- `requests` 会自动将 Python 字典转换为 JSON 字符串
- 自动设置 `Content-Type: application/json` 头
- 放在 HTTP 请求的 body 中发送

**❓ 问题：假设个人认证信息，先 post 拿到认证 token，然后存到 header 里面，再在 post() 中传入 header 参数。假设过期是 3 小时，是不是可以用 session？**

**A:**
- 是的，可以用 session
- 流程：
  1. 登录获取 token → 存到 `session.headers.update({'Authorization': f'Bearer {token}'})`
  2. 后续请求不需要传 `headers` 参数，session 会自动包含
  3. token 过期处理：设置过期时间检查，过期前自动刷新 token 并更新 `session.headers`

---

---

## 项目目录结构

### 简化版目录结构（小型项目）

```
simple_fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py                   # FastAPI 应用注册（创建 app，挂载路由）
│   ├── models.py                 # 数据库字段模型（定义数据库表结构）
│   ├── schemas.py                # Pydantic 模型（请求体校验 + 响应格式）
│   ├── database.py               # 数据库连接配置（连接数据库）
│   └── routers.py                # 所有路由（API 端点和接口函数代码）
├── .env                          # 环境变量（数据库地址、密钥等）
├── requirements.txt              # Python 依赖包列表
└── README.md                     # 项目说明文档
```

### 标准目录结构（中大型项目）

```
my_fastapi_project/
├── app/                          # 主应用目录
│   ├── __init__.py
│   ├── main.py                   # FastAPI 应用入口
│   ├── config.py                 # 配置文件
│   │
│   ├── api/                      # API 路由
│   │   ├── __init__.py
│   │   ├── deps.py               # 依赖项（认证、数据库等）
│   │   └── v1/                   # API 版本1
│   │       ├── __init__.py
│   │       ├── router.py         # 路由汇总
│   │       ├── endpoints/         # 各个端点
│   │       │   ├── __init__.py
│   │       │   ├── users.py      # 用户相关接口
│   │       │   ├── items.py      # 商品相关接口
│   │       │   └── auth.py       # 认证相关接口
│   │       └── schemas.py        # 请求/响应模型
│   │
│   ├── core/                     # 核心功能
│   │   ├── __init__.py
│   │   ├── config.py             # 配置管理
│   │   ├── security.py           # 安全相关（JWT、密码等）
│   │   └── database.py           # 数据库连接
│   │
│   ├── models/                   # 数据库模型
│   │   ├── __init__.py
│   │   ├── user.py               # 用户模型
│   │   └── item.py               # 商品模型
│   │
│   ├── schemas/                  # Pydantic 模型（请求/响应）
│   │   ├── __init__.py
│   │   ├── user.py               # 用户相关模型
│   │   └── item.py               # 商品相关模型
│   │
│   ├── services/                 # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── user_service.py       # 用户业务逻辑
│   │   └── item_service.py      # 商品业务逻辑
│   │
│   ├── crud/                     # 数据库操作（可选）
│   │   ├── __init__.py
│   │   ├── user.py               # 用户 CRUD
│   │   └── item.py               # 商品 CRUD
│   │
│   └── utils/                    # 工具函数
│       ├── __init__.py
│       └── helpers.py
│
├── tests/                        # 测试文件
│   ├── __init__.py
│   ├── conftest.py               # pytest 配置
│   ├── test_api/
│   │   ├── test_users.py
│   │   └── test_items.py
│   └── test_services/
│
├── alembic/                      # 数据库迁移（如果使用 Alembic）
│   ├── versions/
│   └── env.py
│
├── .env                          # 环境变量
├── .env.example                  # 环境变量示例
├── .gitignore
├── requirements.txt              # Python 依赖
├── README.md
└── Dockerfile                    # Docker 配置（可选）
```

### 目录结构说明（大白话版）

| 文件/目录 | 作用 | 类比 |
|----------|------|------|
| `main.py` | 应用入口，注册路由 | 总控制台 |
| `models.py` | 数据库表结构 | 数据库的"表设计图" |
| `schemas.py` | 请求/响应数据格式 | API 的"数据格式说明书" |
| `database.py` | 数据库连接 | 数据库的"连接器" |
| `routers.py` | API 接口实现 | 具体的"业务逻辑" |
| `api/deps.py` | 依赖项（认证、数据库等） | 共享的工具函数 |
| `core/config.py` | 配置管理 | 应用的"配置文件" |
| `services/` | 业务逻辑层 | 处理业务规则的地方 |
| `tests/` | 测试文件 | 测试代码的地方 |

---

## 快速参考

### 参数类型总结

| 参数类型 | 声明方式 | 数据来源 | 适用场景 |
|---------|---------|---------|---------|
| 路径参数 | `Path()` | URL 路径 | 资源标识 `/users/{id}` |
| 查询参数 | `Query()` | URL 查询字符串 | 过滤、分页 `/users?limit=10` |
| 请求体参数 | `BaseModel` | HTTP 请求体（JSON） | 创建/更新数据 |
| Cookie 参数 | `Cookie()` | HTTP Cookie 头 | 会话管理、用户偏好 |
| Header 参数 | `Header()` | HTTP Header 头 | API 认证、元数据 |
| 表单参数 | `Form()` | HTTP 请求体（表单） | HTML 表单提交 |
| 文件参数 | `File()` | HTTP 请求体（文件） | 文件上传 |

### 状态码快速参考

| 状态码 | 含义 | 使用场景 |
|--------|------|---------|
| 200 | OK | 成功（默认） |
| 201 | Created | 创建成功 |
| 400 | Bad Request | 请求格式错误 |
| 404 | Not Found | 资源不存在 |
| 422 | Unprocessable Entity | 参数验证失败 |
| 500 | Internal Server Error | 服务器内部错误 |

---

## 学习总结

### 核心知识点

1. **参数处理**：7种参数类型，每种都有其适用场景
2. **数据验证**：Pydantic 模型自动验证和转换
3. **响应设计**：响应模型、状态码、多个模型
4. **代码复用**：依赖注入减少重复代码
5. **实战应用**：MCP 集成、认证授权

### 最佳实践

1. **参数选择**：
   - 资源标识 → 路径参数
   - 过滤分页 → 查询参数
   - 创建更新 → 请求体参数
   - API 认证 → Header 参数
   - 会话管理 → Cookie 参数

2. **模型设计**：
   - 使用继承减少重复
   - 输入模型和输出模型分离
   - 隐藏敏感信息（密码等）

3. **代码组织**：
   - 小型项目用简化结构
   - 中大型项目用标准结构
   - 业务逻辑放在 services 层

---

**学习完成时间：** 2024年
**总学习时长：** 约 630 分钟（10.5 小时）


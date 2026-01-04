"""
BaseModel 简化版实现原理示例
帮助理解 BaseModel 的核心工作机制
"""

# ============================================
# 简化版 BaseModel（教学用，非实际实现）
# ============================================

class SimpleBaseModel:
    """
    简化版的 BaseModel 实现
    展示 BaseModel 的核心工作原理
    """
    
    def __init__(self, **kwargs):
        """
        初始化时自动验证和赋值
        """
        # 1. 获取类的类型注解（字段定义）
        annotations = self.__class__.__annotations__
        
        # 2. 遍历每个字段，进行验证和赋值
        for field_name, field_type in annotations.items():
            if field_name in kwargs:
                value = kwargs[field_name]
                # 3. 类型验证和转换
                validated_value = self._validate_type(value, field_type)
                setattr(self, field_name, validated_value)
            elif hasattr(self, field_name):
                # 使用默认值（如果字段有默认值）
                pass
            else:
                # 必需字段缺失
                raise ValueError(f"字段 '{field_name}' 是必需的")
    
    def _validate_type(self, value, expected_type):
        """
        简化的类型验证和转换
        """
        # 获取类型的实际类型（处理 Union、Optional 等）
        actual_type = self._get_actual_type(expected_type)
        
        # 类型转换（如果可能）
        if actual_type == int and isinstance(value, str):
            try:
                return int(value)  # "25" → 25
            except ValueError:
                raise TypeError(f"无法将 '{value}' 转换为 {actual_type.__name__}")
        
        # 类型检查
        if not isinstance(value, actual_type):
            raise TypeError(f"期望 {actual_type.__name__}，但得到 {type(value).__name__}")
        
        return value
    
    def _get_actual_type(self, type_hint):
        """
        获取类型的实际类型（简化版，处理 Union、Optional）
        """
        import typing
        origin = typing.get_origin(type_hint)
        if origin is typing.Union:
            # Union[str, None] → str
            args = typing.get_args(type_hint)
            # 返回第一个非 None 的类型
            for arg in args:
                if arg is not type(None):
                    return arg
        return type_hint
    
    def model_dump(self):
        """
        转换为字典（类似 Pydantic 的 model_dump）
        """
        result = {}
        annotations = self.__class__.__annotations__
        for field_name in annotations:
            if hasattr(self, field_name):
                result[field_name] = getattr(self, field_name)
        return result


# ============================================
# 使用示例
# ============================================

class User(SimpleBaseModel):
    name: str
    age: int
    email: str | None = None  # 可选字段

# 测试
try:
    user = User(name="张三", age="25")  # age 会自动转换
    print(user.model_dump())  # {'name': '张三', 'age': 25, 'email': None}
    print(f"姓名: {user.name}, 年龄: {user.age}")
except Exception as e:
    print(f"错误: {e}")


# ============================================
# 实际 Pydantic BaseModel 的复杂实现
# ============================================

"""
实际的 Pydantic BaseModel 实现非常复杂，包括：

1. 元类（Metaclass）
   - 使用 ModelMetaclass 在类定义时处理字段
   - 自动生成验证器、序列化器等

2. 字段验证器（Field Validators）
   - 支持多种验证规则（gt, lt, max_length 等）
   - 自定义验证函数

3. 序列化器（Serializers）
   - model_dump() - 转换为字典
   - model_dump_json() - 转换为 JSON
   - 支持多种序列化模式

4. JSON Schema 生成
   - 自动生成 OpenAPI/Swagger 文档
   - 支持复杂的类型系统

5. 性能优化
   - 使用 Rust 实现的验证器（Pydantic v2）
   - 缓存验证结果

6. 错误处理
   - 详细的错误信息
   - 错误定位和修复建议
"""

# ============================================
# 查看实际 BaseModel 源码的方法
# ============================================

"""
方法1：查看已安装的源码
import pydantic
print(pydantic.__file__)  # 显示 pydantic 安装路径
# 然后查看 pydantic/main.py 文件

方法2：GitHub 源码
https://github.com/pydantic/pydantic

方法3：Python 交互式查看
import inspect
from pydantic import BaseModel
print(inspect.getsource(BaseModel))  # 查看源代码
"""

# ============================================
# 实际 BaseModel 的核心结构（简化说明）
# ============================================

"""
class BaseModel(metaclass=ModelMetaclass):
    # 元类在类定义时执行，处理所有字段
    
    def __init__(self, **data):
        # 1. 获取模型配置
        # 2. 验证所有字段
        # 3. 赋值到实例
        
    def model_validate(cls, obj):
        # 验证并创建实例
        
    def model_dump(self):
        # 序列化为字典
        
    def model_dump_json(self):
        # 序列化为 JSON
        
    @classmethod
    def model_json_schema(cls):
        # 生成 JSON Schema
"""


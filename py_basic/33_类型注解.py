"""
【Python 高级特性：类型系统与泛型】
请在 VS Code 中观察智能提示 (Hover 到函数名上)，体会类型注解带来的“极度舒适感”！
"""
# 导入标准标签库
from typing import List, Dict, Optional, Union, Tuple, Any, TypeVar

print("="*10, "1. 基础与复合类型标签", "="*10)

# a=1: 基础类型与 List、Dict
# 我们明确规定：传入一个整数列表，返回一个“字符串->浮点数”的字典
def analyze_scores(scores: List[int]) -> Dict[str, float]:
    if not scores:
        return {"average": 0.0}
    avg = sum(scores) / len(scores)
    return {"average": round(avg, 2)}

# 智能提示魔法：当你在下面敲出 result["average"] 时，编辑器完全知道它是 float！
result = analyze_scores([90, 85, 95])
print(f"成绩分析结果: {result}")


print("\n"+"="*10, "2. Optional 与 Union (薛定谔的类型)", "="*10)

# a=2: Union 代表“多选一”。参数 age 可以是整数，也可以是字符串。
# a=3: Optional[str] 代表“要么是字符串，要么是 None”。(等价于 Union[str, None])
def get_user_info(user_id: int, age: Union[int, str] = "未知") -> Optional[str]:
    if user_id <= 0:
        return None  # 查无此人返回 None
    return f"用户 {user_id}, 年龄: {age}"

print(get_user_info(101, 25))        # 传 int 合法
print(get_user_info(102, "保密"))    # 传 str 也合法
print(get_user_info(-1))             # 返回 None 合法


print("\n"+"="*10, "3. 泛型 Generics (高级架构师的绝招)", "="*10)

# a=4: 如果我们写 def get_first(items: List[Any]) -> Any:
# 编辑器只会知道返回值是 Any (任何东西)，你丢掉了所有类型信息，后续没有代码提示了！

# a=5: 使用 TypeVar (泛型变量) 解决！
# T 是一个代号。意思是：如果 items 是 List[int]，那 T 就是 int，返回值也是 int。
# 如果 items 是 List[str]，那 T 就是 str，返回值也是 str。类型信息被完美保留！
T = TypeVar('T')

def get_first_element(items: List[T]) -> Optional[T]:
    if not items:
        return None
    return items[0]

# 测试泛型
first_num = get_first_element([10, 20, 30])  # 编辑器精准推断 first_num 是 int
first_str = get_first_element(["AI", "ML"])  # 编辑器精准推断 first_str 是 str

print(f"泛型推断 1: {first_num} (编辑器知道这是 int)")
print(f"泛型推断 2: {first_str} (编辑器知道这是 str)")

# ----------------- 现代 Python (3.9+) 语法补充 -----------------
# ⚠️ 注意：如果你用的是较新的 Python，大厂更推荐直接用内置类型，抛弃 typing 里的首字母大写！
# List[int] -> list[int]
# Dict[str, int] -> dict[str, int]
# Union[int, str] -> int | str
# Optional[str] -> str | None
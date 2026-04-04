"""
【Python 装饰器：基础、wraps、叠加、带参数】
请在 VS Code 中运行，重点观察打印语句的输出顺序，体会“包装”和“执行”的区别！
"""
import time
from functools import wraps

print("="*10, "1. 基础装饰器 & functools.wraps：智能手机壳", "="*10)

def time_it(func):
    """这是一个计算函数运行时间的装饰器（手机壳）"""
    
    # ⚠️ 核心最佳实践：永远记得加上 @wraps(func)！
    # 它的作用是把原函数的 __name__ 和 __doc__ 复制到 wrapper 上，防止伪装暴露
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 功能增强：前置操作
        start_time = time.time()
        print(f"[TimeIt] 开始执行函数: {func.__name__}")
        
        # 核心逻辑：调用原函数，并一定要接住它的返回值！
        result = func(*args, **kwargs)
        
        # 功能增强：后置操作
        end_time = time.time()
        print(f"[TimeIt] 函数 {func.__name__} 执行完毕，耗时: {end_time - start_time:.6f} 秒")
        
        # 归还结果
        return result
        
    return wrapper # 返回包装好的新函数（闭包特性）

# @time_it 是一种语法糖，底层等价于：heavy_computation = time_it(heavy_computation)
@time_it
def heavy_computation(n):
    """模拟一个耗时的算法计算"""
    total = sum([i**2 for i in range(n)])
    return total

res = heavy_computation(100000)
print(f"计算结果: {res}")
print(f"查看函数真名: {heavy_computation.__name__} (因为加了 @wraps，所以不是 wrapper)\n")


print("="*10, "2. 叠加装饰器：俄罗斯套娃", "="*10)

def auth_check(func):
    """模拟权限校验装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("[Auth] 检查权限... 权限通过！")
        return func(*args, **kwargs)
    return wrapper

# ⚠️ 坑点：执行顺序！
# 包装顺序（贴膜套壳）：从下往上 -> 先包 time_it，再在外面包 auth_check
# 执行顺序（剥洋葱）：从上往下 -> 先进 auth_check，再进 time_it，最后执行原函数
@auth_check
@time_it
def fetch_user_data(user_id):
    print(f"  --> 正在获取用户 {user_id} 的核心数据...")
    return {"id": user_id, "name": "AI_Student"}

data = fetch_user_data(9527)
print(f"获取到的数据: {data}\n")


print("="*10, "3. 带参数的装饰器：定制手机壳工厂", "="*10)

def retry(max_retries=3):
    """
    这是一个带参数的装饰器（手机壳工厂）。
    它首先接收参数 max_retries，然后返回一个真正的装饰器。
    因此需要【三层嵌套】！
    """
    def decorator(func): # 真正的装饰器
        @wraps(func)
        def wrapper(*args, **kwargs): # 包装器
            for attempt in range(1, max_retries + 1):
                try:
                    print(f"[Retry] 第 {attempt} 次尝试调用 {func.__name__}...")
                    # 假设这里调用的是不稳定的网络请求或容易报错的逻辑
                    if attempt < max_retries:
                        raise ValueError("模拟网络抖动失败！")
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[Retry] 失败原因: {e}")
                    if attempt == max_retries:
                        print("[Retry] 达到最大重试次数，彻底放弃。")
                        raise # 最后一次如果还报错，就抛出异常
        return wrapper
    return decorator

# 语法糖底层等价于：flaky_network_request = retry(max_retries=2)(flaky_network_request)
@retry(max_retries=2)
def flaky_network_request():
    print("  --> 成功连接到服务器！")
    return "Success"

try:
    flaky_network_request()
except ValueError:
    pass
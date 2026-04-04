"""
【Python 异常处理核心：try、except、else、finally、raise 与异常链】
请在 VS Code 中运行。重点观察不同输入数据下，代码流转的路径！
"""

# a=1: 自定义异常 (继承自内建的 Exception 类)
# 工程实践：为你的项目/算法包写专属的异常，方便外层调用者精准捕获
class ModelConvergeError(Exception):
    """当 AI 模型无法收敛时抛出的业务异常"""
    pass

class DataFormatError(Exception):
    """当数据格式错乱时抛出的业务异常"""
    pass

def process_training_data(data_dict):
    """模拟处理一条 AI 训练数据"""
    print(f"\n--- 开始处理记录: {data_dict} ---")
    
    try:
        # a=2: try 块 (雷区) - 尽量只把可能报错的代码放进这里
        feature_a = data_dict['a'] # 如果没有键 'a'，会引发 KeyError
        feature_b = data_dict['b']
        
        # 常见异常：TypeError (类型不对，比如字符串相除)、ValueError (值不合法)
        if not isinstance(feature_a, (int, float)):
            # a=3: 主动抛出异常 (拉手刹)
            raise TypeError(f"特征 a 必须是数字，当前是: {type(feature_a)}")
            
        if feature_a < 0:
            raise ValueError(f"特征 a 不能为负数: {feature_a}")
            
        # 假设这是一些复杂的计算
        result = feature_a / feature_b # 如果 b 是 0，引发 ZeroDivisionError
        
    except KeyError as e:
        # 拦截特定的系统异常
        print(f"[拦截 KeyError] 字典里找不到键: {e}")
        return None # 即使这里 return 了，finally 依然会执行！
        
    except TypeError as e:
        print(f"[拦截 TypeError] 数据类型错误: {e}")
        
    except ValueError as e:
        print(f"[拦截 ValueError] 业务数值不合法: {e}")
        # a=4: 异常链 (raise ... from)
        # 包装原始异常，向上层抛出更符合业务语义的异常，同时保留原始报错轨迹 (Traceback)
        raise DataFormatError("数据预处理阶段失败！") from e

    # a=5: 绝不能用裸 except: 或者 except BaseException: (会拦截 Ctrl+C！)
    except Exception as e: 
        # 兜底：拦截其他未知的常规异常
        print(f"[拦截 未知异常] 发生了严重错误: {e}")

    else:
        # a=6: else 块 - 只有当 try 里面【没有发生任何异常】时，才会执行。
        # 好处：把不会报错的后续代码放在这里，而不是挤在 try 里面，让排错更清晰。
        print(f"[顺利完成] 计算结果为: {result}")
        return result
        
    finally:
        # a=7: finally 块 - 绝对会执行的扫尾工作
        print("[扫地僧清理战场] 释放当前数据记录的内存锁定 (finally 执行)。")


# ================== 实战调用演示 ==================

# 测试 1：完美数据 (走向：try -> else -> finally)
process_training_data({'a': 10, 'b': 2})

# 测试 2：缺少字段 (走向：try -> except KeyError -> return -> finally)
process_training_data({'a': 10})

# 测试 3：类型错误 (走向：try -> except TypeError -> finally)
process_training_data({'a': "脏数据", 'b': 2})

# 测试 4：零除错误 (走向：try -> except Exception (兜底) -> finally)
process_training_data({'a': 10, 'b': 0})

# 测试 5：演示异常链 (走向：try -> except ValueError -> raise from -> finally)
try:
    process_training_data({'a': -5, 'b': 2})
except DataFormatError as e:
    # 你在终端报错信息里会看到：
    # ValueError: 特征 a 不能为负数: -5
    # The above exception was the direct cause of the following exception:
    # DataFormatError: 数据预处理阶段失败！
    print(f"\n[上层业务捕获] 捕获到了自定义的异常链: {e}")
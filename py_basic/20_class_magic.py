# ==========================================
# 核心概念讲解与底层逻辑实战
# 场景：我们在写算法题，需要自定义一个“数据批次 (DataBatch)”类
# 目标：让这个类能像普通的 Python 列表一样被操作
# ==========================================

class DataBatch:
    def __init__(self, data_list):
        # 知识点：实例变量
        self.data = data_list 

    # ----------------------------------------
    # 1. 打印与调试协议 
    # ----------------------------------------
    def __str__(self):
        """当使用 print(obj) 时调用。底层逻辑：给普通用户看的通俗说明。"""
        # 知识点：f-string 格式化
        return f"这个批次共有 {len(self.data)} 个数据"

    def __repr__(self):
        """在交互式终端直接敲变量名时调用。底层逻辑：给程序员看的精确说明。"""
        return f"DataBatch({self.data})"

    # ----------------------------------------
    # 2. 容器协议 
    # ----------------------------------------
    def __len__(self):
        """当使用 len(obj) 时触发。底层逻辑：必须返回一个大于等于0的整数。"""
        return len(self.data)

    # ----------------------------------------
    # 3. 比较协议
    # ----------------------------------------
    def __eq__(self, other):
        """当使用 == 时触发。底层逻辑：定义两个对象怎样才算“相等”。"""
        # 知识点：isinstance() 判断类型，if-else 提早返回
        if not isinstance(other, DataBatch):
            return False
        return self.data == other.data

    def __lt__(self, other):
        """当使用 < 时触发。实现了它，对象就能用 sorted() 进行排序！"""
        # 纯用你学过的逻辑：我们规定，谁的元素总数少，谁就更小
        return len(self.data) < len(other.data)

    # ----------------------------------------
    # 4. 算术协议
    # ----------------------------------------
    def __add__(self, other):
        """当使用 + 触发。底层逻辑：对应位置相加，必须返回一个【新对象】！"""
        if len(self.data) != len(other.data):
            # 因为还没学异常处理，这里简单打印提示并返回空对象
            print("长度不同，无法相加！")
            return DataBatch([])
        
        # 知识点：zip() 组合遍历，列表推导式
        new_data = [x + y for x, y in zip(self.data, other.data)]
        return DataBatch(new_data) # 返回全新实例

    # ----------------------------------------
    # 5. 可调用协议
    # ----------------------------------------
    def __call__(self, multiplier):
        """当使用 obj(参数) 时触发。底层逻辑：让对象披上函数的外衣。"""
        # 相当于对批次内的数据进行统一缩放
        return [x * multiplier for x in self.data]

    # ----------------------------------------
    # 6. 上下文管理协议 (配合 with 语句使用)
    # ----------------------------------------
    def __enter__(self):
        """当进入 with 代码块时触发。用来准备资源。"""
        print("[底层执行] __enter__: 数据处理准备就绪...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        当离开 with 代码块时必然触发。用来清理资源。
        (注：后面三个参数是 Python 强制传进来的，不管我们用不用，参数列表里必须写上)
        """
        print("[底层执行] __exit__: 数据处理完毕，清理内存...")


# ==========================================
# 运行与调试区 (请在 VS Code 中单步调试)
# ==========================================
if __name__ == "__main__":
    batch1 = DataBatch([1, 2, 3])
    batch2 = DataBatch([4, 5, 6])

    print("--- 1. 测试 __str__ 与 __repr__ ---")
    print(batch1)          # 触发 __str__
    
    print("\n--- 2. 测试 __len__ ---")
    print(f"batch1 长度: {len(batch1)}")

    print("\n--- 3. 测试比较 __eq__ 和 __lt__ ---")
    print(f"相等吗? {batch1 == batch2}")
    
    # 知识点：因为写了 __lt__，现在可以调用内建的 sorted() 排序了
    batch_large = DataBatch([1, 2, 3, 4, 5])
    batches = [batch_large, batch1]
    sorted_batches = sorted(batches) 
    print(f"排序后: {sorted_batches}") # 打印列表时，内部会触发 __repr__

    print("\n--- 4. 测试 __add__ ---")
    batch3 = batch1 + batch2
    print(f"相加结果: {batch3}")

    print("\n--- 5. 测试 __call__ ---")
    # 把对象当成函数用
    print(f"缩放 10 倍: {batch1(10)}")

    print("\n--- 6. 测试 __enter__ 和 __exit__ ---")
    # 配合 with 语句，你会在 print 前后看到 enter 和 exit 的输出
    with batch1 as b:
        print(">> 正在处理批次内的数据...")
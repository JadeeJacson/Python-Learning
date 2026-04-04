"""
【Python 内存管理：引用计数、GC、弱引用与内存视图】
请在 VS Code 中逐步运行，观察控制台输出的内存状态。
"""
import sys
import gc
import weakref

print("="*10, "1. 引用计数 (Reference Counting)", "="*10)

def ref_test():
    a = [1, 2, 3]
    # a=1: 获取对象的引用计数。
    # ⚠️ 结果通常比预期多 1，因为 getrefcount 本身也会引用它一次。
    print(f"列表创建后计数: {sys.getrefcount(a)}") 
    
    b = a
    print(f"赋值给 b 后计数: {sys.getrefcount(a)}")
    
    del b
    print(f"删除 b 后计数: {sys.getrefcount(a)}")

ref_test()


print("\n"+"="*10, "2. 循环引用与 GC (Garbage Collection)", "="*10)

class Node:
    def __init__(self, name):
        self.name = name
        self.next = None
    def __del__(self):
        print(f"  [释放] {self.name} 已从内存抹除")

def cycle_demo():
    n1 = Node("节点1")
    n2 = Node("节点2")
    # a=2: 制造循环引用。n1 指向 n2，n2 指向 n1。
    n1.next = n2
    n2.next = n1
    print("循环引用已建立")
    # 函数结束，n1, n2 变量销毁，但它们的引用计数依然是 1（互相引用）

print("执行循环引用测试函数...")
cycle_demo()
print("函数已结束，此时由于循环引用，对象还没释放！")

# a=3: 手动触发强制垃圾回收。侦探组出动，发现这个孤立的小圈子！
print("手动触发 gc.collect()...")
gc.collect()


print("\n"+"="*10, "3. 弱引用 (weakref) - 缓存不占位", "="*10)

class BigObject:
    def __init__(self):
        self.data = "很多数据"
    def __del__(self):
        print("  [释放] BigObject 已释放")

obj = BigObject()
# a=4: 创建弱引用。它不会增加 obj 的引用计数。
r = weakref.ref(obj)

print(f"弱引用指向的对象是否存活: {r() is not None}")

del obj # 唯一的正式引用消失
print(f"删除正式引用后，弱引用的状态: {r()}") # 此时 r() 会自动变成 None


print("\n"+"="*10, "4. 内存视图 (memoryview) - 极速零拷贝", "="*10)

# a=5: 假设这是一个 1GB 的超大二进制数组
data = bytearray(b"Hello World AI Python")

# 普通切片：data[6:11] 会在内存里创建一个新的字符串对象副本
# 内存视图：直接在原内存地址上划出一个窗口
mv = memoryview(data)
sub_view = mv[6:11]

print(f"视图内容: {sub_view.tobytes()}")

# a=6: 修改视图，原数据会同步改变！(因为它们指向同一块物理内存)
sub_view[0] = ord('X') # 把 W 变成 X
print(f"修改视图后，原数据同步变了: {data}")
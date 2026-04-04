"""
【Python 迭代器协议：__iter__、__next__、StopIteration】
请在 VS Code 中运行。建议在 AIBatchLoader 的 __next__ 方法打上断点，
观察 self.current_index 是如何像游标卡尺一样向后移动的。
"""

print("="*10, "1. 内置对象的迭代机制 (iter 与 next)", "="*10)
# 列表是“可迭代对象”(Iterable)，但它本身不是“迭代器”(Iterator)
data_list = ["数据A", "数据B", "数据C"]

# a=1: 申请一个“夹子”（迭代器）
my_iterator = iter(data_list) 
print(f"列表本身: {type(data_list)}")
print(f"生成的迭代器: {type(my_iterator)}")

# 拨动夹子获取数据
print(f"第一次取值: {next(my_iterator)}") # 底层调用 my_iterator.__next__()
print(f"第二次取值: {next(my_iterator)}")
print(f"第三次取值: {next(my_iterator)}")

# 💣 注意：此时数据已经取完。如果再调用 next(my_iterator)，就会触发 StopIteration 异常！
try:
    next(my_iterator)
except StopIteration:
    print(">>> 警报：StopIteration，迭代器已耗尽，没有数据了！\n")


print("="*10, "2. 实战：手写一个 AI 数据批处理迭代器", "="*10)
# 算法题/工程场景：假设我们有一堆数据，我们不想一次性处理，而是每次拿固定数量（Batch Size）。
# 此时，我们通过实现迭代器协议，自己造一个带状态的“夹子”。

class AIBatchLoader:
    def __init__(self, data, batch_size):
        self.data = data
        self.batch_size = batch_size
        self.current_index = 0 # 游标：记住当前取到哪里了（迭代器的核心！）

    def __iter__(self):
        """
        必须实现！协议规定，iter() 调用时会执行这个方法。
        作为一个合格的迭代器，它的 __iter__ 只需要返回自己 (self) 即可。
        """
        return self

    def __next__(self):
        """
        必须实现！协议规定，next() 调用时会执行这个方法。
        每次调用，都要返回下一批数据，并移动游标。
        """
        # 1. 检查是否还有数据？如果没有，必须抛出 StopIteration
        if self.current_index >= len(self.data):
            raise StopIteration
            
        # 2. 切片取出当前批次的数据
        end_index = self.current_index + self.batch_size
        batch = self.data[self.current_index : end_index]
        
        # 3. 移动游标（状态推进）
        self.current_index = end_index
        
        return batch

# 制造测试数据（1 到 5）
raw_dataset = [1, 2, 3, 4, 5]

# 实例化我们的批处理器（每次取 2 个）
loader = AIBatchLoader(raw_dataset, batch_size=2)

print("\n--- 手动 next() 演示 ---")
iterator_loader = iter(loader)
print(f"第一批: {next(iterator_loader)}") # [1, 2]
print(f"第二批: {next(iterator_loader)}") # [3, 4]
print(f"第三批: {next(iterator_loader)}") # [5] (只剩一个了)
# 如果再 next，就会报错了

print("\n--- for 循环底层真面目 ---")
# 重新实例化一个（因为之前的迭代器游标已经走到头了，被“消耗”了！）
fresh_loader = AIBatchLoader(raw_dataset, batch_size=2)

# 当你写 for batch in fresh_loader: 时，Python 解释器在底层偷偷做了三件事：
# 1. 偷偷调用 iterator = iter(fresh_loader)
# 2. 在一个死循环里无限调用 batch = next(iterator)
# 3. 偷偷抓取 except StopIteration 异常，一旦抓到，就默默退出循环 (break)。
for batch in fresh_loader:
    print(f"For循环自动获取: {batch}")
def loop_demo():
    # 假设我们在训练一个极简的 AI 模型
    features = ["图片A", "图片B", "破损图片C", "图片D"]
    labels = ["猫", "狗", "未知", "猫"]

    # 1. range() 的常规用法：循环特定次数
    print("--- 准备训练 ---")
    for i in range(2):  # 生成 0, 1
        print(f"Epoch {i+1} 开始...")

    # 2. zip() 与 enumerate() 的神级组合 (大厂规范写法)
    print("\n--- 开始处理数据 ---")
    # enumerate 帮我们拿索引 (step)，zip 帮我们同时拿特征 (x) 和标签 (y)
    for step, (x, y) in enumerate(zip(features, labels), start=1):
    #右边打包，左边解包
        
        # 3. continue 的用法：跳过脏数据
        if x.startswith("破损"):
            print(f"  Step {step}: 发现脏数据 '{x}'，直接跳过 (continue)")
            continue
            
        # 4. break 的用法：提前终止
        if step > 3:
            print(f"  Step {step}: 达到最大步数，提前结束训练 (break)")
            break
            
        print(f"  Step {step}: 正在用 [{x}] 训练，目标标签是 [{y}]")
        
        # pass 占位符：假设这里有复杂的反向传播逻辑，还没写完
        pass

    # 5. for-else 结构 (Python 独门绝技)
    print("\n--- 质检环节 ---")
    target = "老虎"
    for label in labels:
        if label == target:
            print(f"找到了目标标签: {target}!")
            break
    else:
        # 只有当上面的 for 循环【没有被 break 打断】，顺顺利利执行完时，才会执行这里
        print(f"遍历了所有数据，没有找到标签: {target} (触发了 else)")

loop_demo()
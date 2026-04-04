def conditional_demo(user_role, action_command):
    print(f"--- 测试角色: {user_role}, 指令: {action_command} ---")
    
    # 1. if-elif-else 与 嵌套条件
    if user_role == "admin":
        print("✅ 管理员登录成功。")
        # 嵌套条件
        if action_command == "delete":
            print("  -> 警告：正在执行高危删除操作！")
        else:
            print(f"  -> 执行普通管理员操作：{action_command}")
            
    elif user_role == "intern":
        print("👀 实习生登录，权限受限。")
        
    else:
        print("❌ 未知用户，拒绝访问。")


    # 2. match-case 模式匹配 (Python 3.10+)
    # 假设 action_command 是一个元组，比如 ("move", 10, 20) 或者 ("stop",)
    match action_command:
        case ("stop",):
            print("🤖 机器人接收到停止指令。")
            
        case ("move", x, y):  # 核心威力：直接解包提取变量 x 和 y！
            print(f"🤖 机器人移动到坐标 X:{x}, Y:{y}。")
            
        case ("attack", target) if user_role == "admin": # 甚至可以加 if 守卫条件！
            print(f"🗡️ 攻击目标：{target}!")
            
        case _:  # 等同于 else，捕获所有未匹配的情况
            print("❓ 无法识别的指令格式。")

# 运行测试
# n="neighbor"
# #conditional_demo("admin", ("move", 100, 200))
# conditional_demo("admin", ("attack", n))
# print("\n")
# conditional_demo("intern", ("attack", n))


def process_ai_task(task_data):
    # task_data 可能是字典、列表或字符串，结构完全不固定
    match task_data:
        # 1. 匹配特定结构的字典，并直接提取 status 和 result 的值
        case {"status": "success", "result": data}:
            print(f"✅ 任务成功！提取到的核心数据是: {data}")
            
        # 2. 匹配列表，且要求第一个元素是 "error"，把剩下的所有错误码打包给 codes
        case ["error", *codes]:
            print(f"❌ 发生批量错误，错误码列表: {codes}")
            
        # 3. 匹配特定类/字典，并加上 if 守卫条件 (Guard)
        case {"status": "retry", "count": c} if c < 3:
            print(f"🔄 正在进行第 {c} 次重试...")
            
        case {"status": "retry", "count": c} if c >= 3:
            print(f"🚫 重试次数过多 ({c}次)，放弃任务。")
            
        # 4. 兜底匹配 (通配符)
        case _:
            print(f"❓ 无法识别的数据格式: {task_data}")

# 测试运行
process_ai_task({"status": "success", "result": [0.98, 0.99, 0.95]})
process_ai_task(["error", 404, 500, 502])
process_ai_task({"status": "retry", "count": 2})
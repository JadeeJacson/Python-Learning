"""
【Python 类基础：class、__init__、self、实例变量与类变量】
请在 VS Code 中运行。建议在 __init__ 和 upgrade_skills 处打断点，
观察左侧 Variables 面板中 "self" 内部包含的数据，以及特殊变量 __class__。
"""

print("="*10, "1. 类的定义与出厂配置 (__init__ & self)", "="*10)

class AI_Student:
    # 【类变量】公共财产，所有实例共享。直接定义在类内部，方法外部。
    # 就像学校的公告板，所有学生看到的都是同一个。
    total_students_created = 0  
    target_company = "大厂"      

    def __init__(self, name, main_language):
        """
        【初始化方法】每次使用类名创建新对象时，会自动调用。
        self 代表刚刚被创建出来的那个具体的学生对象。
        """
        # 【实例变量】私有财产，绑定在具体的 self 上
        self.name = name
        self.main_language = main_language
        self.skills = [] # 每个学生都有自己独立的技能列表
        
        # 每实例化一个学生，就把【类变量】加 1
        # 注意：修改类变量最好用 类名.变量名 (AI_Student.total_students_created)
        AI_Student.total_students_created += 1
        
        print(f"[出厂广播] 新生 {self.name} 注册成功！分配到 {self.main_language} 阵营。")

    def learn_skill(self, new_skill):
        """
        这是一个实例方法。第一个参数必须是 self！
        当对象调用此方法时，Python 会自动把对象本身作为 self 悄悄传进来。
        """
        self.skills.append(new_skill)
        print(f"  -> {self.name} 学习了新技能：{new_skill}")

    def show_profile(self):
        """展示个人信息和公共信息"""
        print(f"[{self.name} 的档案] 语言: {self.main_language}, 技能: {self.skills}")
        print(f"  (目标: {self.target_company}, 竞争者总数: {AI_Student.total_students_created})")


# 1. 实例化对象（造饼干）
student_a = AI_Student("Alice", "Python")
student_b = AI_Student("Bob", "C++")
print("")

print("="*10, "2. 实例变量的独立性 (私有财产)", "="*10)
# Alice 和 Bob 分别学习不同的技能，互不影响
student_a.learn_skill("数据结构")
student_b.learn_skill("操作系统")
student_a.show_profile()
student_b.show_profile()
print("")


print("="*10, "3. 类变量的共享性与陷阱 (公共财产)", "="*10)
# 此时总人数应该是 2，Alice 和 Bob 看到的总人数是一样的
print(f"直接通过类名查看总人数: {AI_Student.total_students_created}")

# 💣 陷阱演示：尝试通过实例修改类变量
print("\n[突发事件] Alice 想修改目标公司为 '巨头'...")
student_a.target_company = "巨头" 

# 我们来看看结果：
print(f"Alice 的目标: {student_a.target_company}")
print(f"Bob 的目标: {student_b.target_company}")
print(f"类本尊的目标: {AI_Student.target_company}")
# 【底层逻辑】
# student_a.target_company = "巨头" 并没有修改公共黑板上的字！
# 它实际上是给 Alice 这个实例【动态增加】了一个同名的【实例变量】。
# 当 Alice 查找 target_company 时，优先找到了自己的实例变量；
# 而 Bob 没有这个实例变量，只能去公共黑板（类变量）上找，所以还是 "大厂"。

# ✅ 正确修改类变量的姿势：必须通过类名修改！
print("\n[全局通知] 学校统一修改目标为 'Top 互联网'...")
AI_Student.target_company = "Top 互联网"
print(f"Alice 的目标: {student_a.target_company} (Alice 的私有变量依然遮蔽了类变量)")
print(f"Bob 的目标: {student_b.target_company} (Bob 看到了新的黑板)")
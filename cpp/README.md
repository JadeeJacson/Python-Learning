# C++ 学习支线

这个目录用于 C++ 基础恢复、进阶学习和底层机制理解。

当前定位：C++ 是支线，不与 Python 主线争抢时间；重点学习 Python 不明显暴露的类型、内存、资源管理和编译期机制。

## 第一阶段：快速恢复

不重新完整学习所有基础语法，重点恢复：

- 基本类型与类型转换
- 函数与参数传递
- 引用
- 指针
- `const`
- 数组、字符串
- class / struct
- 构造与析构
- 栈与堆

## 第二阶段：核心进阶

- 对象生命周期
- RAII
- 拷贝构造 / 拷贝赋值
- move semantics
- 智能指针：`unique_ptr` / `shared_ptr` / `weak_ptr`
- 继承、多态、virtual
- STL 容器与算法
- iterator
- lambda
- template

## 第三阶段：Modern C++ 与工程

- `auto`
- range-based for
- `enum class`
- `constexpr` 基础
- structured bindings
- optional / variant 等常用工具
- header / source 文件组织
- 编译、链接基本机制
- CMake
- debugger
- sanitizer 基础

## 学习重点

学习 C++ 时要持续和 Python 做机制对照，例如：

```text
Python object/reference   ↔ C++ value/reference/pointer
GC                        ↔ RAII / deterministic lifetime
list                      ↔ vector
 dict                     ↔ map / unordered_map
runtime dynamic typing    ↔ static typing / templates
```

目标不是短期把所有 C++ 高级特性学完，而是建立可靠的内存、对象、STL 和工程基础，为算法以及未来可能的 AI Infra / 推理系统方向做准备。

# Python Engineering

这个目录用于把 Python 从“会写语法”推进到“能维护项目”。

## 学习顺序

1. 模块、包与 `import`
2. 虚拟环境与依赖管理
3. `pathlib` 与文件系统
4. 类型标注与静态检查思维
5. 异常设计
6. logging
7. 配置管理
8. pytest 与测试设计
9. CLI
10. 序列化与数据格式
11. API 调用与网络 I/O
12. 项目结构、分层与可维护性

## 和现有内容的关系

`py_basic/` 中已经存在装饰器、OOP、多线程、多进程、asyncio 等教学代码，这些不迁移。复习完成后，在这里进一步关注它们如何进入真实项目。

例如：

- 装饰器 → 日志、计时、重试；
- dataclass → 配置与数据对象；
- asyncio → 并发请求；
- multiprocessing → CPU 密集任务；
- typing → 大型项目接口约束；
- context manager → 文件、锁、连接等资源管理。

后续文件优先采用 `demo / practice / engineering` 的学习方式，具体见根目录 `LEARNING_GUIDE.md`。

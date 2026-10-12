# Legacy Inventory

2026-10-12 已检查 `E:\New project\frontend_mvp`：原项目为HTML/CSS/JavaScript页面，包含多个历史版本、旧工作台、教学模拟脚本和吉祥物。现有index.html引用workspace-v2版本脚本与样式，因此以该入口引用的文件为本次前端复用依据。

仅复用独立的视觉资源与转义函数。旧业务JS调用guided-tutoring等当前工程未实现的接口，不能直接接入。具体处置见[migration_map.md](migration_map.md)。其他旧项目副本和后端代码未完成迁移审计。

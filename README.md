# 教师教育智能体

面向师范生与教师专业成长的智能支持工程。当前采用模块化单体、Clean Architecture、领域驱动设计、LangGraph 工作流编排与 Port/Adapter 外部能力适配。

## 四阶段培养链

`WF1 会学习 → WF2 会设计 → WF3 会实施与判断 → WF4 会反思与迁移 → 公共多源评价 → 成长画像更新 → 下一轮专业成长`

四个一级工作流分别为：

- `wf1_cr_sdl_v3`：基于认知冲突动态调节的自我导向学习工作流。
- `wf2_instructional_design_v1`：教学系统设计工作流。
- `wf3_teaching_implementation_judgment_v1`：会实施与判断培养工作流。
- `wf4_reflection_transfer_v1`：会反思与迁移培养工作流。

公共多源评价负责正式 Rubric 评分与综合评价；成长画像由独立工作流更新。各培养工作流只生成候选证据和阶段业务状态，并通过稳定契约衔接。

## 当前状态

已实现四个工具目录（共 122 个工具）及四条详细 LangGraph 工作流。原图中的 WF1 52 个、WF2 18 个、WF3 24 个、WF4 36 个节点均独立注册为 LangGraph 节点；缺失的人工复核、取消、过期、失败和完成终态以 `X*` 补充节点实现。完整对应关系见 [原图节点—LangGraph节点—工具—输入输出—路由对照表](docs/workflow-node-tool-route-mapping.md)。

工程同时包含 DeepSeek/Qwen 双模型网关、PostgreSQL 业务数据层、pgvector 检索、FunASR/SenseVoice 转写适配，以及工作流启动、恢复和状态查询 API。模型不会决定权限、事务、正式评分、路由或终态。

多人协作时分别修改以下清单，避免四条工作流集中在同一文件产生冲突：

- `workflows/workflow_manifests/wf1_manifest.py`
- `workflows/workflow_manifests/wf2_manifest.py`
- `workflows/workflow_manifests/wf3_manifest.py`
- `workflows/workflow_manifests/wf4_manifest.py`

`workflows/manifests.py` 仅保留兼容导出，不在其中编写节点和路由。

## 本地启动

1. 将 `.env.example` 复制为 `.env`，填写 DeepSeek、DashScope 和数据库密钥。
2. 执行 `docker compose up --build -d`。
3. 执行 `alembic upgrade head` 初始化数据库。
4. 访问 `/api/v1/health` 查看服务状态。

工作流接口：

- `POST /api/v1/workflows/{workflow_name}/start`
- `POST /api/v1/workflows/{workflow_name}/resume`
- `GET /api/v1/workflows/{workflow_name}/{thread_id}`

生产环境应把内存 Checkpointer 替换为独立的 PostgreSQL Checkpointer；业务表不能作为 LangGraph Checkpoint 使用。

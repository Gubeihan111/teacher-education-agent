# Migration Map

## 2026-10-12 前端迁移映射

| 原位置（E盘旧项目） | 新位置（本仓库） | 处理 |
| --- | --- | --- |
| `New project/frontend_mvp/assets/cnu-mascot.png` | `apps/web/public/assets/mascots/cnu-mascot.png` | 原样复制，SHA-256一致 |
| `New project/frontend_mvp/workspace-v2.20260724-01.css` 的 `:root` 配色 | `apps/web/src/styles/main.css` | 复用主要色值、圆角与阴影，布局重新编写 |
| `New project/frontend_mvp/workspace-v2.20260724-01.js` 的 `escapeHtml` | `apps/web/src/utils/escape-html.js` | 提取为ES模块，补充空值处理 |
| 旧“学—教—评”页面与旧API调用 | `apps/web/index.html`、`src/app/`、`src/features/`、`src/services/` | 重写为四阶段页面和当前API适配 |
| 旧登录、课堂模拟专用脚本 | 暂不迁移 | 依赖旧后端契约；后续逐项评估，不冒充已接入 |

API新增同源静态页面入口及状态响应中的中断信息。未修改原项目，未复制.env、用户记录、凭据或旧备份。业务数据库及旧后端的完整迁移不在本次范围内。

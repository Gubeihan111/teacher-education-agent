# Web

四阶段教师成长工作台，采用原生 ES Modules、HTML 和 CSS。由 FastAPI 同源提供页面，无需前端依赖安装。

## 使用

准备后端所需环境和配置后，在仓库根目录运行：

```powershell
uvicorn apps.api.app.main:app --host 127.0.0.1 --port 8000
```

浏览器打开 `http://localhost:8000/`。不要直接双击 HTML 文件：页面依赖同源 `/api/v1` 和 `/web`。Docker部署仍使用根目录Compose，镜像已复制整个apps目录。

## 当前页面

- 成长首页与四阶段导航。
- 四条工作流：填写输入、创建任务、查询已有线程、查看候选产物。
- 后端返回人工中断时展示确认表单，调用resume沿用同一thread_id。
- 知识资料上传到现有入库接口。
- 综合评价和成长画像目前为待接入说明，不展示模拟分数。

页面使用的输入字段依据现有State定义，后端仍存在工具参数映射不完整和降级实现。前端不通过伪造状态或设置route_decisions来绕过这些问题。当前表单不是完整教学培养流程验收结果。

## 接口

| 页面动作 | API |
| --- | --- |
| 服务连接 | `GET /api/v1/health` |
| 开始任务 | `POST /api/v1/workflows/{name}/start` |
| 查询状态 | `GET /api/v1/workflows/{name}/{thread_id}` |
| 人工确认 | `POST /api/v1/workflows/{name}/resume` |
| 文档入库 | `POST /api/v1/knowledge/ingest` |

状态响应补充`interrupts`（id/value），保留原values/next。当前客户端为显式查询，未实现实时事件流。超时不会自动重试写请求，后台可能继续运行，应查询原任务编号。

## 迁移与约束

从旧项目复用吉祥物、配色变量和escapeHtml函数；新编写四阶段页面及API客户端。未迁入旧登录、旧接口、备份、模型文件或.env。

`localStorage`只存各阶段最后一次线程编号；表单和产物保留在当前页面内存。当前API使用固定身份，尚无真正鉴权或多租户隔离，仅用于本地开发。

JS/CSS版本：`20261012-01`。修改资源时同步更新index.html和模块import的版本参数。

静态语法检查（不执行业务代码）：

```powershell
cd apps/web
npm run check
```

未启动浏览器、后端或业务测试，尚未验证视觉效果及端到端行为。成员7继续负责拆分页面组件和联调；细节见[团队开发手册](../../docs/TEAM_DEVELOPMENT_GUIDE.md)。

# 教师教育智能体 GitHub 开发人员协作指南

本指南适用于参与 `teacher-education-agent` 项目的开发人员。所有修改通过功能分支和 Pull Request 提交，禁止直接修改 `main`。

## 1. 准备开发环境

安装 Git 和 GitHub CLI：

```powershell
winget install --id Git.Git -e
winget install --id GitHub.cli -e
```

重新打开 PowerShell，配置个人身份：

```powershell
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub邮箱"
git config --global init.defaultBranch main
git config --global core.autocrlf true
gh auth login
```

登录时选择 `GitHub.com → HTTPS → Login with a web browser`。

## 2. 接受邀请并克隆项目

接受负责人发送的 GitHub Collaborator 邀请，然后执行：

```powershell
New-Item -ItemType Directory -Path E:\GitProjects -Force
cd E:\GitProjects
git clone https://github.com/仓库所有者/teacher-education-agent.git
cd teacher-education-agent
git remote -v
git status
```

创建本地环境文件：

```powershell
Copy-Item .env.example .env
```

`.env` 只保存在本机。禁止提交 API Key、数据库密码、学生个人数据、课堂录音、视频、模型权重和生产日志。

## 3. 开发分工

开发人员 A 负责：

```text
src/teacher_education_agent/workflows/workflow_manifests/wf1_manifest.py
src/teacher_education_agent/workflows/workflow_manifests/wf2_manifest.py
src/teacher_education_agent/tools/wf1_learning/
src/teacher_education_agent/tools/wf2_design/
```

开发人员 B 负责：

```text
src/teacher_education_agent/workflows/workflow_manifests/wf3_manifest.py
src/teacher_education_agent/workflows/workflow_manifests/wf4_manifest.py
src/teacher_education_agent/tools/wf3_implementation/
src/teacher_education_agent/tools/wf4_reflection/
```

以下公共文件由负责人统一维护，开发人员修改前必须先沟通：

```text
src/teacher_education_agent/workflows/detailed.py
src/teacher_education_agent/tools/contracts.py
src/teacher_education_agent/tools/registry.py
src/teacher_education_agent/infrastructure/
apps/api/
migrations/
```

## 4. 开始任务

每项任务都从最新 `main` 创建独立分支：

```powershell
git switch main
git pull --ff-only origin main
git switch -c feature/wf1-goal-routes
```

推荐分支名称：

```text
feature/wf1-learning
feature/wf2-design
feature/wf3-implementation
feature/wf4-reflection
fix/wf3-stability-route
refactor/wf4-tool-mapping
docs/workflow-mapping
```

一个分支只处理一个明确任务。

## 5. 修改和提交代码

修改前确认当前分支：

```powershell
git branch --show-current
git status
```

修改后检查差异：

```powershell
git diff
git status
```

只添加本次任务相关文件：

```powershell
git add src/teacher_education_agent/workflows/workflow_manifests/wf1_manifest.py
git add src/teacher_education_agent/tools/wf1_learning
```

提交并推送：

```powershell
git commit -m "feat(wf1): implement goal confirmation routes"
git push -u origin feature/wf1-goal-routes
```

推荐提交格式：

```text
feat(wf1): add goal confirmation routes
feat(wf3): implement judgment evidence mapping
fix(wf4): correct transfer failure route
refactor(tools): split reflection handlers
docs(workflow): update node mapping
```

## 6. 更新工作流对照表

只要修改任意 `wf*_manifest.py`，必须重新生成对照表：

```powershell
$env:PYTHONPATH = "src"
python scripts/export_workflow_mapping.py
```

然后提交对应工作流清单和生成后的文档：

```powershell
git add src/teacher_education_agent/workflows/workflow_manifests
git add docs/workflow-node-tool-route-mapping.md
git commit -m "docs(workflow): regenerate node mapping"
git push
```

不要手工修改生成的对照表。

## 7. 提交 Pull Request

可以在 GitHub 网页点击 `Compare & pull request`，也可以执行：

```powershell
gh pr create `
    --base main `
    --head feature/wf1-goal-routes `
    --title "feat(wf1): implement goal confirmation routes" `
    --body "实现WF1目标确认节点和有限状态路由，并更新节点对照表。"
```

PR 描述必须说明：

```markdown
## 修改内容

- 修改的工作流：
- 修改的节点：
- 修改的工具：
- 修改的路由：

## 原图对应关系

- 原图节点编号：
- 对照表位置：
- 是否增加 supplement 节点：
- 补充原因：

## 静态检查

- [ ] Python 文件可解析
- [ ] 节点编号没有重复
- [ ] 路由目标存在
- [ ] 工具名称存在
- [ ] 对照表已更新
- [ ] 未提交密钥、个人数据、录音或模型文件
```

PR 至少需要一名其他成员审核。审核通过前不得自行合并。

## 8. 处理审核意见

根据 PR 评论修改代码，然后执行：

```powershell
git add 修改的文件
git commit -m "fix(wf1): address review comments"
git push
```

原 PR 会自动更新，无需重新创建。

## 9. 同步 main

其他 PR 合并后，在继续开发前执行：

```powershell
git fetch origin
git switch main
git pull --ff-only origin main
git switch feature/wf1-goal-routes
git rebase origin/main
```

如果 rebase 后需要更新远程功能分支：

```powershell
git push --force-with-lease
```

`--force-with-lease` 只能用于自己的功能分支，禁止用于 `main`。

## 10. 解决冲突

查看冲突文件：

```powershell
git status
```

打开文件，处理并删除以下标记：

```text
<<<<<<< HEAD
当前内容
=======
另一分支内容
>>>>>>> origin/main
```

确认最终代码后执行：

```powershell
git add 冲突文件
git rebase --continue
```

如仍有冲突，重复处理。完成后执行：

```powershell
git push --force-with-lease
```

无法确认正确结果时取消操作：

```powershell
git rebase --abort
```

涉及 `detailed.py`、工具契约、数据库迁移或多个工作流的冲突，应交由负责人处理。

## 11. PR 合并后的本地清理

负责人合并 PR 后执行：

```powershell
git switch main
git pull --ff-only origin main
git branch -d feature/wf1-goal-routes
git fetch --prune
```

## 12. 必须遵守的规则

1. 禁止直接推送 `main`。
2. 每个任务使用独立分支。
3. 每个 PR 只处理一个工作流或一个公共问题。
4. 不得修改其他开发人员负责的 Manifest。
5. 公共文件修改前必须与负责人沟通。
6. 原图节点编号不得随意修改或删除。
7. 补充节点必须使用 `X1.*`、`X2.*`、`X3.*`、`X4.*`。
8. 修改 Manifest 后必须重新生成对照表。
9. 禁止提交 `.env`、密钥、个人数据、录音、视频和模型权重。
10. 至少一人审核后才能合并。
11. 每天开始开发前同步 `main`。

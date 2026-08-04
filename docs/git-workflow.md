# A2UI_Web 团队 Git 工作流规范

> **适用版本**: Git 2.40+
> **制定日期**: 2026-08-04
> **维护人**: Lin Jie

---

## 目录

1. [核心原则](#1-核心原则)
2. [分支策略 — Trunk-Based Development](#2-分支策略)
3. [Commit 规范 — Conventional Commits](#3-commit-规范)
4. [日常工作流](#4-日常工作流)
5. [Pull Request 流程](#5-pull-request-流程)
6. [常见场景处理](#6-常见场景处理)
7. [Git Hooks 说明](#7-git-hooks-说明)
8. [故障恢复指南](#8-故障恢复指南)
9. [CI/CD 集成建议](#9-cicd-集成建议)
10. [检查清单](#10-检查清单)

---

## 1. 核心原则

### 1.1 四个铁律

| # | 原则 | 为什么 |
|---|------|--------|
| 1 | **每个 Commit 原子化** | 一个提交只做一件事，可独立回滚 |
| 2 | **永远不 force-push 共享分支** | `main` 等共享分支一旦 push，绝不改写历史 |
| 3 | **分支前先同步** | 创建分支前 `git fetch && git rebase origin/main` |
| 4 | **提交信息即文档** | 好的 commit message 不需要看代码就能理解变更 |

### 1.2 Git 配置（已预设）

```bash
# 行尾符：提交时统一 LF
git config core.autocrlf input

# pull 时默认 rebase 而非 merge
git config pull.rebase true

# push 默认只推送当前分支
git config push.default simple

# 新分支自动跟踪远程并设置 rebase
git config branch.autosetuprebase always
```

---

## 2. 分支策略

### 2.1 Trunk-Based Development（推荐）

本项目采用 **Trunk-Based Development**，适合 2-8 人团队、持续交付场景：

```
main ────●────●────●────●────●────●───  (始终可部署)
           \  /      \  /      \  /
            ●─●       ●─●       ●       (短生命周期功能分支 ≤ 3 天)
```

**核心规则：**
- `main` 分支始终可部署到生产环境
- 所有开发在功能分支上进行，分支存活不超过 3 天
- 通过 PR 合并到 `main`
- 大功能拆分为多个小 PR，用 Feature Flag 控制发布

### 2.2 分支命名规范

| 前缀 | 用途 | 示例 |
|------|------|------|
| `feat/` | 新功能 | `feat/user-auth`, `feat/sse-heartbeat` |
| `fix/` | Bug 修复 | `fix/login-redirect`, `fix/mobile-sidebar` |
| `chore/` | 杂项维护 | `chore/deps-update`, `chore/cleanup-logs` |
| `refactor/` | 重构 | `refactor/extract-cache-layer` |
| `docs/` | 文档 | `docs/api-reference` |
| `test/` | 测试 | `test/chat-e2e` |
| `release/` | 发布准备 | `release/v1.2.0` |
| `hotfix/` | 紧急修复 | `hotfix/critical-auth-bypass` |

**命名规则：** 全小写，单词用连字符分隔，不加版本号/日期。

### 2.3 分支生命周期

```
创建 → 开发 → Rebase → PR → Review → Merge → 删除
 ↑                                              ↓
 └───────── 最多 3 天 ──────────────────────────→┘
```

---

## 3. Commit 规范

### 3.1 Conventional Commits 格式

```
<type>(<scope>): <简短描述>

<详细说明 - 解释 WHAT 和 WHY，不解释 HOW>

<尾部 - 引用 Issue、标注破坏性变更>
```

**示例：**

```bash
# ✅ 好的提交
feat(backend): 添加 SSE 流式响应的心跳保活机制

每 30 秒发送 keepalive 注释行，防止 Nginx 代理超时断连。
配合前端 ReadableStream 的 reader.read() 超时重试逻辑。

Closes #42

# ✅ 好的提交
fix(frontend): 修复移动端侧边栏拖动时页面横向滚动

根因: touchmove 事件未阻止默认行为
方案: 在侧边栏容器添加 touch-action: none

Refs #58

# ❌ 差的提交
update code           # 不明确
fix bug               # 描述不足
WIP                   # 无意义
feat: 改了点东西       # 范围不清
```

### 3.2 Type 速查表

| Type | 含义 | 会触发版本号 |
|------|------|-------------|
| `feat` | 新功能 | MINOR++ |
| `fix` | Bug 修复 | PATCH++ |
| `docs` | 文档变更 | 不触发 |
| `style` | 格式调整（空格、分号等） | 不触发 |
| `refactor` | 重构（不改功能/修 Bug） | 不触发 |
| `perf` | 性能优化 | PATCH++ |
| `test` | 测试相关 | 不触发 |
| `chore` | 构建/工具/依赖 | 不触发 |
| `ci` | CI 配置 | 不触发 |
| `revert` | 回滚 | PATCH++ |

### 3.3 Scope 速查表

| Scope | 对应目录 |
|-------|---------|
| `backend` | `backend/` |
| `frontend` | `frontend/` |
| `nginx` | `nginx/` |
| `docker` | `docker-compose.yml`, Dockerfile |
| `docs` | `docs/` |
| `deps` | 依赖变更 |
| `auth` | 认证授权 |
| `chat` | 聊天核心逻辑 |
| `mcp` | MCP 协议相关 |
| `api` | API 接口 |

---

## 4. 日常工作流

### 4.1 开始新功能

```bash
# 1. 确保本地是最新的
git fetch origin
git checkout main
git rebase origin/main

# 2. 创建功能分支
git checkout -b feat/my-feature

# 3. 开发... 写代码、测试

# 4. 小步提交（每完成一个逻辑单元）
git add backend/app/api/chat.py
git commit -m "feat(backend): 添加聊天消息持久化存储"

git add backend/app/models/message.py
git commit -m "feat(backend): 定义 Message 数据模型"

# 5. 推送到远程（每日至少一次，防丢失）
git push -u origin feat/my-feature
```

### 4.2 保持分支同步

```bash
# 每天开始工作前，将 main 的最新变更 rebase 到你的分支
git fetch origin
git rebase origin/main

# 如果有冲突，逐个解决后:
git add <resolved-files>
git rebase --continue

# 如果 rebase 搞砸了，可以撤销:
git rebase --abort
```

### 4.3 整理提交历史（PR 前必做）

```bash
# 交互式 rebase，整理最近 5 个提交
git rebase -i HEAD~5

# 在编辑器中:
# pick   保留这个提交
# reword 修改提交信息
# squash 合并到上一个提交
# fixup  合并到上一个提交，丢弃提交信息
# drop   删除这个提交

# 示例: 把 3 个 WIP/fixup 合并为 1 个有意义的提交
# 原始:
#   pick abc1234 feat(backend): 添加消息存储
#   pick def5678 fixup
#   pick ghi9012 WIP
#   pick jkl3456 fix typo
# 整理后:
#   pick abc1234 feat(backend): 添加消息存储
#   fixup def5678 fixup
#   fixup ghi9012 WIP
#   fixup jkl3456 fix typo

# 整理后需要 force-push（仅限你自己的分支！）
git push --force-with-lease
```

> **⚠️ `--force-with-lease` 安全检查**：如果远程分支有你不知道的新提交，push 会失败，防止覆盖他人工作。比 `--force` 安全得多。

---

## 5. Pull Request 流程

### 5.1 PR 提交前检查清单

- [ ] 分支已 rebase 到最新的 `origin/main`
- [ ] 提交历史已整理（无 WIP/fixup commit）
- [ ] 所有测试通过（本地运行过）
- [ ] 无遗留的 `console.log` / `print()` 调试代码
- [ ] `.env` 未包含在提交中
- [ ] PR 标题遵循 Conventional Commits 格式
- [ ] PR 描述包含：做了什么、为什么、测试方法、截图（如有 UI 变更）

### 5.2 PR 描述模板

```markdown
## 变更概述
<!-- 一句话描述这个 PR 做了什么 -->

## 背景
<!-- 为什么需要这个变更？关联哪个 Issue？ -->

## 变更内容
<!-- 列出主要变更点 -->
- 
- 

## 测试方法
<!-- Reviewer 如何验证这个 PR？ -->
1. 
2. 

## 截图 (如有 UI 变更)
<!-- 拖入截图 -->

## 关联 Issue
Closes #
```

### 5.3 Code Review 规范

| 角色 | 职责 |
|------|------|
| **Author** | 确保 PR 描述清晰、commit 原子化、CI 通过 |
| **Reviewer** | 关注逻辑正确性、安全性、性能、可维护性 |
| **所有人** | 对事不对人，Review 的是代码不是人 |

**Review 时间承诺：** PR 提交后 24 小时内完成首次 Review。

### 5.4 合并策略

```bash
# 推荐: Squash Merge（将分支上所有 commit 合并为一个）
# 适合: 功能分支上 commit 较多但不需保留逐条历史

# 备选: Rebase Merge（保留所有 commit 但变基到 main 顶端）
# 适合: 每个 commit 都有独立价值、需要保留细粒度历史

# 不推荐: Merge Commit（创建额外合并节点）
# 仅在需要明确标记"这是一个功能合并"时使用
```

---

## 6. 常见场景处理

### 6.1 场景一：紧急修复线上 Bug

```bash
# 1. 从 main 创建 hotfix 分支
git fetch origin
git checkout -b hotfix/critical-fix origin/main

# 2. 修复 → 测试 → 提交
git add .
git commit -m "fix(backend): 修复 SSE 连接泄漏导致的内存溢出"

# 3. 推送并创建 PR（标记为紧急）
git push -u origin hotfix/critical-fix
# → 在 GitHub 创建 PR，base=main，添加 hotfix/urgent 标签

# 4. 合并后立即部署
```

### 6.2 场景二：解决合并冲突

```bash
# Rebase 时遇到冲突
git rebase origin/main
# CONFLICT (content): Merge conflict in backend/app/api/chat.py

# 1. 查看冲突文件
git status

# 2. 手动编辑冲突文件，移除 <<<<<<< ======= >>>>>>> 标记

# 3. 标记为已解决
git add backend/app/api/chat.py

# 4. 继续 rebase
git rebase --continue

# 5. 如果解决不了，放弃 rebase
git rebase --abort
```

### 6.3 场景三：撤销错误的提交

```bash
# 情况 A: 提交了但还没 push
git reset --soft HEAD~1    # 撤销提交，保留修改在暂存区
git reset --mixed HEAD~1   # 撤销提交和暂存，保留修改在工作区
git reset --hard HEAD~1    # 完全撤销（⚠️ 不可恢复！）

# 情况 B: 已经 push 了
# 先 revert（创建新提交来撤销，不改写历史）
git revert HEAD
git push

# 情况 C: 只改提交信息（还没 push）
git commit --amend -m "新的提交信息"

# 情况 D: 漏了文件想补到上一个提交
git add forgotten-file.py
git commit --amend --no-edit
```

### 6.4 场景四：Cherry-pick 特定提交到其他分支

```bash
# 将 main 上的某个修复 cherry-pick 到 release 分支
git checkout release/v1.2.0
git cherry-pick abc1234    # abc1234 是那个修复的 commit hash
git push
```

### 6.5 场景五：临时切换任务（WIP 保存）

```bash
# 正在开发 feat/A，突然需要修 Bug
# 方案 1: git stash（推荐）
git stash push -m "WIP: 用户认证模块 50%"
# ... 切分支修 Bug ...
git checkout feat/A
git stash pop

# 方案 2: WIP Commit（备用）
git add -A && git commit -m "WIP: 用户认证模块"
# ... 切分支修 Bug ...
git checkout feat/A
git reset HEAD~1    # 撤销 WIP commit，保留修改
```

---

## 7. Git Hooks 说明

本项目预置了 3 个 Git Hooks：

| Hook | 触发时机 | 行为 |
|------|---------|------|
| `pre-commit` | `git commit` 之前 | 警告直接提交到 main；阻止提交 .env；检测冲突标记 |
| `commit-msg` | 编辑完提交信息后 | 校验 Conventional Commits 格式 |
| Commit Template | 编辑提交信息时 | 显示格式提示和示例 |

**安装方式**（已预设）：
```bash
git config core.hooksPath .githooks
git config commit.template .gitmessage
```

---

## 8. 故障恢复指南

### 8.1 `git reflog` — 你的后悔药

```bash
# 查看所有 HEAD 变更历史（包括已删除的分支、reset 的提交）
git reflog

# 输出示例:
# abc1234 HEAD@{0}: commit: feat(backend): 添加用户登录
# def5678 HEAD@{1}: rebase (finish): returning to refs/heads/feat/login
# ghi9012 HEAD@{2}: reset: moving to HEAD~1     ← 这里 reset 了一个提交

# 恢复到 reset 前的状态
git reset --hard ghi9012
```

### 8.2 常见灾难恢复

```bash
# "我不小心 force-push 了 main！"
# → 立即找 team lead，用 reflog 恢复并重新 push

# "我 merge 了错误的分支"
git reset --hard HEAD~1    # 撤销 merge（还没 push 的话）

# "我删了一个不该删的分支"
git reflog                          # 找到该分支最后一个 commit
git checkout -b recovered-branch abc1234

# "rebase 到一半想放弃"
git rebase --abort

# "amend 了错误的提交（已经 push 了）"
# → 这种情况只能接受，不要再改写了
```

### 8.3 `git bisect` — 二分查找 Bug 引入点

```bash
# 当你知道某个版本正常、某个版本有 Bug，但不知道哪个提交引入的
git bisect start
git bisect bad HEAD           # 当前版本有问题
git bisect good v1.0.0        # v1.0.0 是好的

# Git 会自动切到中间版本，你测试后标记:
git bisect good   # 或
git bisect bad

# 重复几次后，Git 会定位到引入 Bug 的确切提交
git bisect reset   # 结束后恢复
```

---

## 9. CI/CD 集成建议

### 9.1 分支保护规则（GitHub/GitLab 推荐配置）

```yaml
# main 分支保护:
- 禁止直接 push（必须通过 PR）
- PR 合并前要求:
  - ✅ 至少 1 个 Reviewer 审批
  - ✅ CI 全部通过
  - ✅ 分支是最新的（与 main 无冲突）
  - ✅ Commit 信息符合 Conventional Commits
- 禁止 force-push
- 合并后自动删除源分支
```

### 9.2 推荐的 CI Pipeline

```
Push to feat/* branch:
  → Lint (flake8 + eslint)
  → Type Check (mypy + vue-tsc)
  → Unit Tests (pytest + vitest)

PR to main:
  → 上述全部
  → Build Check (Docker build)
  → Integration Tests

Merge to main:
  → Build & Push Docker Image
  → Deploy to Staging
  → Smoke Tests
```

### 9.3 自动化版本管理

```bash
# 基于 Conventional Commits 自动生成 CHANGELOG 和版本号
# 推荐工具: semantic-release / standard-version

# 示例: 从上次发布到现在的变更
git log v1.0.0..HEAD --oneline --format="%s"
```

---

## 10. 检查清单

### 每天开始工作
- [ ] `git fetch origin && git rebase origin/main`
- [ ] 确认在正确的分支上工作

### 每次提交
- [ ] 提交信息符合 Conventional Commits 格式
- [ ] 本次提交只做了一件事
- [ ] 没有包含调试代码
- [ ] 没有包含 .env 或敏感信息

### PR 提交前
- [ ] 分支已 rebase 到最新的 main
- [ ] 提交历史已整理（squash WIP commit）
- [ ] PR 描述完整
- [ ] CI 通过
- [ ] 自我 Review 了一遍 diff

### Code Review
- [ ] 理解了这个 PR 的目的
- [ ] 检查了逻辑正确性
- [ ] 检查了安全性（注入、权限、敏感信息）
- [ ] 检查了边界情况

---

## 附录 A：速查命令

```bash
# === 日常工作 ===
git fetch origin                              # 拉取远程更新
git checkout -b feat/xxx origin/main          # 创建功能分支
git rebase origin/main                        # 变基到最新 main
git push -u origin feat/xxx                   # 推送新分支
git push --force-with-lease                   # 安全强推（仅自己分支）

# === 提交管理 ===
git add -p                                    # 交互式暂存（推荐）
git commit                                     # 打开模板编辑器
git commit --amend                            # 修改上次提交
git rebase -i HEAD~3                          # 整理最近 3 个提交

# === 撤销操作 ===
git reset --soft HEAD~1                       # 撤销提交，保留修改
git checkout -- <file>                        # 丢弃单个文件的修改
git stash push -m "描述"                      # 暂存当前工作
git stash pop                                 # 恢复暂存

# === 查看历史 ===
git log --oneline --graph --all               # 图形化历史
git log --oneline -20                         # 最近 20 条
git reflog                                    # 所有 HEAD 变更
git diff main...feat/xxx                      # 与 main 的差异

# === 清理 ===
git branch -d feat/xxx                        # 删除本地分支
git push origin --delete feat/xxx             # 删除远程分支
git remote prune origin                       # 清理本地已删除的远程分支引用
```

## 附录 B：推荐工具

| 工具 | 用途 |
|------|------|
| [commitlint](https://commitlint.js.org/) | CI 中自动校验 commit 格式 |
| [commitizen](https://commitizen-tools.github.io/commitizen/) | 交互式生成规范 commit |
| [semantic-release](https://semantic-release.gitbook.io/) | 自动版本管理和 CHANGELOG |
| [git-lfs](https://git-lfs.com/) | 大文件管理（如有需要） |
| VS Code GitLens 插件 | IDE 内增强 Git 体验 |

---

> **记住：好的 Git 工作流不是为了限制你，而是为了让你更高效、更少踩坑。**
> 规范是团队的共同约定，不是某个人说了算。有问题随时讨论、迭代优化。

# AI编程与开发工具

## 36. [2026-02-23]

## 📒 文章 7


> 文档 ID: `InvqwxIh7il04ykWF9qcEtB9nob`

**来源**: 鹿导·邪修大法第四弹：Codex 零轮询 + Git 驱动自动化审计 | **时间**: 2026-03-13 | **原文链接**: 无

---

### 📋 核心分析

**战略价值**: 把 Codex CLI 接入零轮询模式，再用 GitHub Actions + Self-hosted Runner 打通「push 代码 → 自动审计 → 飞书通知」全链路，实现真正的无人值守 Agent Team。

**核心逻辑**:

- Codex CLI 没有内置 Hook，用 shell `&&` 串联 `codex exec` 和回调脚本来模拟，效果与 Claude Code 内置 Hook 完全等价
- `nohup bash -c "codex exec ... && on-codex-complete.sh" &` 是核心范式：后台启动、立即返回、完成后自动回调
- Codex 有两种模式：`--full-auto` 做审计+修复（会写文件），`--review --base main` 做只读审查（不改代码）
- Claude Code 负责复杂多文件开发，Codex CLI 负责安全审计/快速修复，两者分工明确，不要混用
- Self-hosted Runner 跑在 Mac Mini 上的好处：7x24 在线、直接访问本地 CLI 工具、不需要暴露公网
- GitHub Actions Workflow 用 `paths` 过滤器只在 `backend/` 或 `frontend/src/` 有变更时才触发，避免无效审计
- `git diff --name-only HEAD~1..HEAD` 收集变更文件列表，最多取前 50 个，作为上下文传给 OpenClaw
- OpenClaw（大副）收到 `[AUTO-AUDIT]` 消息后派发给 Forge（CTO Agent），Forge 分析变更范围决定用 review 还是 exec 模式
- Forge 的 Skill 文件 `SKILL.md` 明确写「立即结束 session，不等待」，回调由 `on-codex-complete.sh` 负责通知
- Token 消耗从手动触发的 15,000–50,000/次 降到自动化的 ~700/次，覆盖率从「想起来才审计」变成「每次 push 都审计」

---

### 🎯 关键洞察

**为什么 Codex 零轮询要用 shell wrapper 而不是其他方案？**

Codex CLI 是一个标准的命令行进程，退出码即状态。shell 的 `&&` 天然就是「前一个命令成功才执行下一个」的语义，配合 `nohup ... &` 后台化，完美复刻了 Claude Code Hook 的行为，零依赖、零配置。

**为什么 Runner 不能放在 iCloud 同步目录？**

iCloud 会在文件被写入时触发同步，Codex 大量写文件时会产生冲突和锁，导致审计失败。必须用 `~/repos/` 这类普通目录。

**三层架构的本质**：触发层（GitHub Actions）只负责感知变更，决策层（OpenClaw → Forge）只负责分析和派发，执行层（Codex CLI）只负责干活。每层职责单一，任何一层出问题都不影响其他层。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|---|---|---|---|
| dispatch-codex.sh | 生成 `codex-launch.sh`，用 `&&` 串联 Codex 和回调，`nohup` 后台启动 | 立即返回，Codex 后台跑 | 脚本路径必须在 `~/.openclaw/workspace/scripts/` |
| on-codex-complete.sh | 接收 `{"exit_code": $EXIT_CODE}` JSON，触发飞书通知 | 审计完成自动推送 | 需要提前配置飞书 Webhook |
| Codex exec 模式 | `codex exec --full-auto -C "$WORK_DIR" "$TASK"` | 审计+自动修复+提交 | 会修改文件，确认 WORK_DIR 正确 |
| Codex review 模式 | `codex review --base main~5` | 只读审查最近5个commit | 不会改文件，安全 |
| GitHub Actions paths 过滤 | `paths: ['backend/**', 'frontend/src/**']` | 只在相关路径变更时触发 | 路径改成自己项目的实际路径 |
| Self-hosted Runner 标签 | `--labels "self-hosted,macOS,ARM64,audit"` | Workflow 精准路由到 Mac Mini | 标签必须和 `runs-on` 完全匹配 |
| concurrency 配置 | `group: audit-${{ github.repository }}` + `cancel-in-progress: false` | 审计任务串行，不互相取消 | 不要改成 true，否则审计会被打断 |
| Forge Skill 文件 | `workspace-forge/skills/codex-audit-dispatcher/SKILL.md` | 告诉 Forge 审计决策逻辑 | 必须写「立即结束 session，不等待」 |

---

### 🛠️ 操作流程

**1. 准备阶段：下载并配置 Codex 脚本**

```bash
# 下载派发脚本
curl -sL https://gist.githubusercontent.com/alextangson/345b4a5d69df364751a394e347e5993a/raw/dispatch-codex.sh \
  -o ~/.openclaw/workspace/scripts/dispatch-codex.sh

# 下载回调脚本
curl -sL https://gist.githubusercontent.com/alextangson/345b4a5d69df364751a394e347e5993a/raw/on-codex-complete.sh \
  -o ~/.openclaw/workspace/scripts/on-codex-complete.sh

# 给执行权限
chmod +x ~/.openclaw/workspace/scripts/dispatch-codex.sh \
         ~/.openclaw/workspace/scripts/on-codex-complete.sh
```

完整 Gist 地址：`https://gist.github.com/alextangson/345b4a5d69df364751a394e347e5993a`

**2. 核心执行：在 Mac Mini 上注册 Self-hosted Runner**

```bash
# 克隆项目到非 iCloud 目录
mkdir -p ~/repos
cd ~/repos
git clone https://github.com/你的用户名/你的项目.git

# 创建 Runner 目录
mkdir -p ~/actions-runner && cd ~/actions-runner

# 去 GitHub 仓库 → Settings → Actions → Runners → New self-hosted runner
# 按页面指引下载 Runner 包，然后注册：
./config.sh --url https://github.com/你的用户名/你的项目 \
  --token YOUR_TOKEN \
  --name "mac-mini" \
  --labels "self-hosted,macOS,ARM64,audit" \
  --unattended

# 安装为系统服务（开机自启）
./svc.sh install
./svc.sh start
```

**3. 创建 GitHub Actions Workflow**

在项目根目录创建 `.github/workflows/audit.yml`：

```yaml
name: Auto Audit

on:
  push:
    branches: [main]
    paths:
      - 'backend/**'        # ← 改成你的后端路径
      - 'frontend/src/**'   # ← 改成你的前端路径

concurrency:
  group: audit-${{ github.repository }}
  cancel-in-progress: false

jobs:
  trigger-audit:
    runs-on: [self-hosted, audit]
    timeout-minutes: 5

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: 收集变更文件
        id: changes
        run: |
          FILES=$(git diff --name-only HEAD~1..HEAD -- backend/ frontend/src/ | head -50)
          if [ -z "$FILES" ]; then
            echo "skip=true" >> $GITHUB_OUTPUT
          else
            echo "skip=false" >> $GITHUB_OUTPUT
            echo "files<<EOF" >> $GITHUB_OUTPUT
            echo "$FILES" >> $GITHUB_OUTPUT
            echo "EOF" >> $GITHUB_OUTPUT
          fi

      - name: 通知 OpenClaw 审计
        if: steps.changes.outputs.skip != 'true'
        env:
          NO_PROXY: localhost,127.0.0.1
        run: |
          openclaw agent \
            --agent main \
            --message "[AUTO-AUDIT] 代码变更，请派发审计。
          变更文件：
          ${{ steps.changes.outputs.files }}
          仓库路径：$HOME/repos/你的项目名" \
            --json
```

**4. 配置 Forge 的审计 Skill**

创建 `workspace-forge/skills/codex-audit-dispatcher/SKILL.md`：

```markdown
# Codex 审计派发器（自动模式）

收到审计任务后：
1. 分析变更文件列表
2. 决定用 review 模式还是 exec 模式
3. 调用 dispatch-codex.sh 后台执行
4. 立即结束 session，不等待

完成后 on-codex-complete.sh 会自动通知。
```

**5. 验证：手动测试两种 Codex 模式**

```bash
# Exec 模式（审计 + 修复）
dispatch-codex.sh "审计 backend/app/services/ 的安全问题，修复后提交" ~/repos/my-project

# Review 模式（只读审查）
dispatch-codex.sh "审查最近的代码变更" ~/repos/my-project --review --base main~5
```

---

### 💡 具体案例/数据

- 测试环境：Mac Mini M4 + OpenClaw 2026.2.12 + Codex v0.94.0 + Claude Code
- Token 消耗对比：手动审计 15,000–50,000 tokens/次 → 自动化 ~700 tokens/次，降幅 95%+
- 变更文件收集上限：`head -50`，超过 50 个文件时截断，避免 prompt 过长

---

### 📝 避坑指南

- ⚠️ Mac Mini 上的项目目录必须在 `~/repos/`，严禁放在 iCloud Drive 同步目录，否则 Codex 写文件时会触发 iCloud 锁冲突
- ⚠️ `concurrency.cancel-in-progress` 必须设为 `false`，设为 `true` 会导致正在跑的审计被新 push 打断
- ⚠️ Runner 标签 `audit` 必须和 Workflow 里 `runs-on: [self-hosted, audit]` 完全一致，否则任务会一直 pending
- ⚠️ Forge 的 Skill 文件里必须明确写「立即结束 session，不等待」，否则 Forge 会阻塞等 Codex 返回，白白消耗 Token
- ⚠️ 前置条件：必须已完成第二弹（Claude Code Hooks 零轮询），本弹的回调机制依赖第二弹的基础设施

---

### 🏷️ 行业标签

#OpenClaw #CodexCLI #ClaudeCode #GitHubActions #SelfHostedRunner #AgentTeam #零轮询 #自动化审计 #MacMini

---

---

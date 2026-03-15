# AI编程与开发工具

## 29. [2026-02-14]

## 📒 文章 7


> 文档 ID: `BjH2wWYKEiWJDpkBuwacu0Ppnlh`

**来源**: 鹿导：OpenClaw 邪修大法第二弹 — Cursor 爆改大龙虾零轮询开发指南 | **时间**: 2026-03-13 | **原文链接**: 无

---

### 📋 核心分析

**战略价值**: 通过 Claude Code Hooks 机制彻底消灭 OpenClaw 调用外部 Agent 时的轮询 Token 消耗，将单次任务成本从数千 Token 压缩到固定 ~700 Token。

**核心逻辑**:

- **OpenClaw 的正确定位是「调度层」而非「执行层」**：它不绑定任何模型，是一个容器/船，真正的代码执行应交给 Claude Code CLI 这类专业工具。
- **轮询是根本性的架构缺陷**：OpenClaw 默认每 5 秒向 Claude Code 询问一次进度，30 分钟任务会产生 360 次无效轮询，每次都消耗 Token。
- **Hooks 是事件驱动替代轮询的唯一解**：Claude Code 完成任务的瞬间主动触发回调脚本，中间等待期 0 Token 消耗，类比「取餐器」而非「站柜台前反复问」。
- **两个 Hook 事件需同时注册**：`Stop`（正常完成触发）+ `SessionEnd`（兜底触发），两者指向同一回调脚本，脚本内部有防重复机制。
- **dispatch-cc.sh 的核心是 `nohup ... &`**：用 `nohup` 后台启动 Claude Code 后立即返回，OpenClaw 不阻塞，不等待，不消耗。
- **on-cc-complete.sh 通过 stdin 接收 Hook 数据**：Claude Code 触发 Hook 时会把 `session_id` 等信息通过 stdin 传入，用 `jq` 解析后写入 `state/cc-result.json`，再调用 `openclaw send` 推送通知。
- **SKILL.md 是让大龙虾「知道自己有新技能」的关键**：放在 `workspace-forge/skills/cc-dispatch/` 下，明确写明「派发后立即结束 session，不要等待，不要轮询」。
- **路径问题是最高频踩坑点**：`~/.claude/settings.json` 里的路径必须是绝对路径，`$HOME` 需替换为实际用户目录（`echo $HOME` 查看）。
- **Token 消耗结构固定为三段**：派发 ~200 tokens + 等待期 0 tokens + 回调 ~500 tokens = 总计 ~700 tokens，与任务时长完全解耦。
- **下一步扩展方向是 Git 事件驱动**：将同套 Hooks 模式接入 Codex CLI，实现 push 代码后 Agent Team 自动审计并提 PR。

---

### 🎯 关键洞察

**为什么轮询这么贵？**

原因：OpenClaw 调用 Claude Code 后，自身没有「等待」状态，只能用定时轮询模拟等待。每次轮询 = 一次 LLM 调用 = Token 消耗。任务越长，轮询次数越多，成本指数级放大。

动作：用 Hooks 把「主动询问」改成「被动接收」。Claude Code 完成的瞬间，操作系统层面触发回调脚本，脚本再反向唤醒 OpenClaw。

结果：等待期间 OpenClaw 完全空闲，可以处理其他对话，Token 消耗从「任务时长 × 轮询频率」变成固定的两次 LLM 调用（派发 + 回调）。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|---|---|---|---|
| 前置依赖 | `npm install -g @anthropic-ai/claude-code` / `brew install jq` | Claude Code CLI + jq 可用 | 三者版本：openclaw 2.9+，claude CLI 任意，jq 任意 |
| dispatch-cc.sh | `nohup claude -p "$CC_PROMPT" --print --dangerously-skip-permissions > "$CC_OUTPUT" 2>&1 &` | 后台启动 Claude Code，立即返回 | `--dangerously-skip-permissions` 跳过交互确认，生产环境注意权限边界 |
| on-cc-complete.sh | `INPUT=$(cat)` → `jq -r '.session_id'` → 写 `cc-result.json` → `openclaw send "..."` | Hook 触发后写结果、推通知 | 脚本内置防重复机制，Stop + SessionEnd 同时触发不会执行两次 |
| ~/.claude/settings.json | `"Stop": [{"hooks": [{"type": "command", "command": "/绝对路径/on-cc-complete.sh"}]}]` | Claude Code 完成时自动回调 | 路径必须是绝对路径，不能用 `~` 或 `$HOME`，需手动替换 |
| SKILL.md | 放在 `workspace-forge/skills/cc-dispatch/SKILL.md` | 大龙虾知道如何调用新技能 | 必须明确写「派发后立即结束 session，不要轮询」，否则大龙虾仍会等待 |
| 结果文件 | `~/.openclaw/workspace/state/cc-result.json` | 存储任务完成状态和输出 | 验证时 `cat` 此文件，看到 `"status": "completed"` 即成功 |

---

### 🛠️ 操作流程

**第 0 步：用 Cursor 打开 OpenClaw 目录**

三种方式任选其一：

```bash
# 方式一：终端直接打开
ls ~/.openclaw/openclaw.json   # 确认文件存在
cursor ~/.openclaw              # 用 Cursor 打开
```

- 方式二：Finder → `Cmd + Shift + G` → 输入 `~/.openclaw` → 拖到 Cursor 图标
- 方式三：Cursor 内 `Cmd + O` → `Cmd + Shift + .`（显示隐藏文件）→ 找 `.openclaw`

打开后目录结构：

```
.openclaw/
├── openclaw.json
├── agents/
│   ├── main/
│   └── forge/
├── workspace/
│   ├── scripts/        ← 放 dispatch-cc.sh 和 on-cc-complete.sh
│   ├── state/          ← cc-result.json 写入位置
│   └── memory/
└── workspace-forge/
    ├── scripts/
    └── skills/         ← 放 cc-dispatch/SKILL.md
```

---

**第 1 步：下载并安装两个核心脚本**

Gist 地址：`https://gist.github.com/alextangson/7f42bf0a078b4266f098a4ad61732ae3`

```bash
# 确保目录存在
mkdir -p ~/.openclaw/workspace/scripts ~/.claude

# 下载派发脚本
curl -sL https://gist.githubusercontent.com/alextangson/7f42bf0a078b4266f098a4ad61732ae3/raw/dispatch-cc.sh \
  -o ~/.openclaw/workspace/scripts/dispatch-cc.sh

# 下载回调脚本
curl -sL https://gist.githubusercontent.com/alextangson/7f42bf0a078b4266f098a4ad61732ae3/raw/on-cc-complete.sh \
  -o ~/.openclaw/workspace/scripts/on-cc-complete.sh

# 赋予执行权限
chmod +x ~/.openclaw/workspace/scripts/dispatch-cc.sh \
         ~/.openclaw/workspace/scripts/on-cc-complete.sh
```

两个脚本核心逻辑：

```bash
# dispatch-cc.sh 核心：后台启动，立即返回
nohup claude -p "$CC_PROMPT" \
  --print \
  --dangerously-skip-permissions \
  > "$CC_OUTPUT" 2>&1 &

# on-cc-complete.sh 核心：读 Hook 数据，写结果，通知大龙虾
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id')
jq -n --arg task "$TASK_NAME" --arg status "completed" ... > "$RESULT_FILE"
openclaw send "📋 任务完成：「${TASK_NAME}」耗时 ${DURATION}" &
```

---

**第 2 步：注册 Claude Code Hook（最关键）**

```bash
# 下载 Hook 配置模板
curl -sL https://gist.githubusercontent.com/alextangson/7f42bf0a078b4266f098a4ad61732ae3/raw/claude-settings.json \
  -o /tmp/claude-hooks-template.json

# 查看内容
cat /tmp/claude-hooks-template.json
```

模板内容结构：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "on-cc-complete.sh 的完整绝对路径"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "matcher": "other",
        "hooks": [
          {
            "type": "command",
            "command": "同上"
          }
        ]
      }
    ]
  }
}
```

手动操作步骤：
1. 用 Cursor 打开 `~/.claude/settings.json`（不存在则新建）
2. 将模板的 `hooks` 部分合并进去
3. 查询实际路径：`echo $HOME`
4. 将路径中的 `$HOME` 替换为实际值，例如 `/Users/yourname/...`

⚠️ 此步骤无法自动化，必须手动操作，因为每人用户名不同，且可能已有 settings.json 内容需要合并。

---

**第 3 步：创建 SKILL.md 教大龙虾用新技能**

在 Cursor 里创建文件：`~/.openclaw/workspace-forge/skills/cc-dispatch/SKILL.md`

```markdown
# Claude Code Dispatch — 零轮询 Hook 工作流

## 用法
把复杂开发任务派发给 Claude Code 后台执行。
Claude Code 完成后通过 Hook 自动通知，中间 0 Token 消耗。

## 派发命令
bash scripts/dispatch-cc.sh "任务描述" /工作目录 [--agent-teams]

## 派发后
立即告诉用户任务已派发，然后结束 session。不要等待。不要轮询。

## 完成后
Hook 会自动写入 state/cc-result.json 并通知 OpenClaw。
读取结果文件，格式化报告给用户。

## Token 消耗
- 派发：~200 tokens
- 等待中：0 tokens
- 回调：~500 tokens
- 总计：~700 tokens
```

---

**第 4 步：验证整条链路**

```bash
# 派发测试任务
~/.openclaw/workspace/scripts/dispatch-cc.sh \
  "Create a simple hello world HTML page" \
  ~/test-project
```

预期输出：

```
✅ Claude Code 任务已派发！
  任务: Create a simple hello world HTML page
  工作目录: /Users/xxx/test-project
  PID: 12345

Claude Code 正在后台运行。
完成后会通过 Hook 自动通知。
```

等待 Claude Code 完成后验证结果：

```bash
cat ~/.openclaw/workspace/state/cc-result.json
# 看到 "status": "completed" 即手术成功
```

---

### 💡 具体案例/数据

**改造前 vs 改造后对比**：

| 指标 | 改造前（轮询） | 改造后（Hooks） |
|---|---|---|
| 一次任务 Token 消耗 | 5,000 - 50,000+ | ~700（固定） |
| 等待期间大龙虾状态 | 被占用，无法处理其他请求 | 完全空闲 |
| 任务耗时 30 分钟 | 可能数千至数万 Token | ~700 Token |
| 失败后能自动通知 | 不能 | 能（SessionEnd Hook 兜底） |

**架构对比图**：

```
改造前：
你 → 大龙虾 → Claude Code
              ↕ (每5秒轮询，持续烧 Token)

改造后：
你 → 大龙虾 → dispatch-cc.sh → Claude Code（后台）
     (空闲)                           │
                                      │ 完成
                                      ▼
              大龙虾 ← on-cc-complete.sh ← Hook 触发
              (被唤醒)
```

---

### 📝 避坑指南

- ⚠️ `~/.claude/settings.json` 中路径必须是绝对路径，`~` 和 `$HOME` 变量在某些执行环境下不会被展开，必须替换为 `/Users/yourname/` 形式
- ⚠️ 如果已有 `settings.json`，不能直接覆盖，需要手动合并 `hooks` 字段，否则会丢失原有配置
- ⚠️ `dispatch-cc.sh` 和 `on-cc-complete.sh` 必须有执行权限（`chmod +x`），否则 Hook 触发时静默失败
- ⚠️ OpenClaw 版本需 2.9+，低版本可能不支持 `openclaw send` 命令
- ⚠️ Stop + SessionEnd 两个 Hook 可能同时触发，但脚本内置防重复机制，不会执行两次通知

---

### 🏷️ 行业标签

#OpenClaw #ClaudeCode #AgentArchitecture #Hooks #零轮询 #TokenOptimization #AIWorkflow #自动化

---

---

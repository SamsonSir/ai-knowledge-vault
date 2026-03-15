# Agent与技能系统

## 117. [2026-03-10]

## 📓 文章 6


> 文档 ID: `NL4cwOJp1ip9a1kfRLNcAyrCnDb`

**来源**: 🤖用最简单的比喻，让你秒懂OpenClaw工作原理 | **时间**: 2026-03-14 | **原文链接**: 无

---

### 📋 核心分析

**战略价值**: OpenClaw 是一个 AI Agent 网关框架，通过持久记忆、多渠道接入、定时主动触发、多 Agent 路由和三层容错机制，将被动问答 AI 升级为可长期运行的主动智能管家。

**核心逻辑**:

- **对话循环（Agent Loop）**: 基于 `while True` 的持续监听循环，接收输入 → 思考 → 回答 → 等待，直到收到终止信号。这是所有 Agent 行为的基础驱动机制。
- **工具箱（Tool Use）**: AI 内置搜索、写作、命令执行、日历等工具，用户意图触发对应工具调用，工具返回结果后再组织语言回答，实现"能干活"而非"只聊天"。
- **记忆笔记本（Memory System）**: 对话内容和用户偏好持久化写入 `~/.openclaw/workspace/MEMORY.md`，后续对话通过 TF-IDF 搜索 + 向量检索自动召回相关记忆，实现跨会话长期记忆。
- **多联系渠道（Channels）**: 飞书（最完善，支持群消息/私聊/webhook）、企业微信（应用消息/机器人）、QQ（机器人/频道消息）、终端，所有渠道消息汇聚到同一 Agent 实例，共享记忆和上下文。
- **智能门卫（Gateway 路由）**: 根据来源渠道 + 用户身份 + 规则表，将消息路由到不同 Agent（如小ai/Sage/Helper），实现"不同场景不同性格"的多 Agent 分工。
- **灵魂拼图（8层系统提示词）**: 启动时从 `~/.openclaw/workspace` 读取 8 个 Markdown 文件动态拼装系统提示词，优先级从高到低：SOUL.md（人格语气）→ AGENTS.md（Agent配置）→ IDENTITY.md（身份角色）→ USER.md（用户偏好）→ TOOLS.md（工具文档）→ HEARTBEAT.md（心跳提示词）→ BOOTSTRAP.md（首次引导）→ MEMORY.md（记忆存储）。
- **定时闹钟（Heartbeat & Cron）**: 每 15 分钟轮询一次，读取 `CRON.json` 判断是否触发定时任务（如每天早 8 点早安提醒、生日提醒），主动将消息推入发送队列，实现"不问也提醒"。
- **可靠快递（Delivery）**: 消息发送前先持久化到磁盘，发送失败自动重试最多 3 次，成功后删除记录，保证消息不丢失。
- **韧性盾牌（Resilience）**: 三层容错——①备用 API Key 轮换（一个账号失效自动切换）；②对话历史过长时自动压缩总结（防止超出 context 窗口）；③失败重试机制（最多 3 次，间隔等待）。
- **交通指挥（Concurrency）**: 多用户并发时按优先级排队处理：聊天车道（最高优先）→ 任务车道（次要）→ 学习车道（可延后），避免并发混乱。

---

### 🎯 关键洞察

**从被动到主动的核心机制**：传统 AI 是"问答机"，OpenClaw 通过 Heartbeat 定时轮询 + Cron 任务调度，让 AI 具备主动触发能力。每 15 分钟的心跳检查是实现"主动关心"的底层驱动。

**提示词动态组装是个性化的关键**：OpenClaw 不是用一个固定 prompt，而是每次对话前实时读取 8 个文件动态拼装，这意味着你只需编辑对应 `.md` 文件就能即时改变 AI 的性格、记忆、工具能力，无需重启服务。

**Memory 的 TF-IDF + 向量双检索**：保证了在大量记忆条目中既能精确匹配关键词（TF-IDF），又能语义模糊召回相关内容（向量），两者互补。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 工作空间目录 | `~/.openclaw/workspace` | 存放所有配置文件 | 默认路径，可自定义 |
| 查看配置文件 | `ls -la ~/.openclaw/workspace` | 列出所有拼图文件 | 确认 8 个文件都存在 |
| 编辑人格 | `nano ~/.openclaw/workspace/SOUL.md` | 即时改变 AI 语气性格 | 修改后下次对话生效 |
| 编辑用户偏好 | `nano ~/.openclaw/workspace/USER.md` | AI 记住你的习惯 | 手动补充可加速个性化 |
| 查看上下文用量 | `/context list` | 显示各文件 token 占用 | TOOLS.md 超大会被截断 |
| 查看详细上下文 | `/context detail` | 显示各组件 token 明细 | 用于排查 token 超限 |
| 查看会话状态 | `/status` | 显示模型、token 用量、历史消息数 | context 超 80% 需压缩 |
| 飞书接入 | webhook + 群消息 + 私聊 | 最完善的渠道 | 支持三种消息类型 |
| 企业微信接入 | 应用消息 + 机器人 | 工作场景首选 | — |
| QQ 接入 | 机器人 + 频道消息 | 社交娱乐场景 | — |

---

### 🛠️ 操作流程

**1. 准备阶段：初始化工作空间**

```bash
# 确认工作空间目录存在
ls -la ~/.openclaw/workspace

# 编辑核心配置文件（按优先级从高到低）
nano ~/.openclaw/workspace/SOUL.md       # 定义人格语气
nano ~/.openclaw/workspace/IDENTITY.md  # 定义身份角色
nano ~/.openclaw/workspace/USER.md      # 填入用户偏好
nano ~/.openclaw/workspace/AGENTS.md    # 配置 Agent 规则
```

**2. 核心执行：提示词组装流程**

每次用户发消息，OpenClaw 按以下顺序组装最终提示词发送给大模型：

```
最终提示词 = 系统提示词（~10,000-40,000 tokens）
           + 项目上下文文件（~5,000-20,000 tokens）
           + 会话历史（~5,000-15,000 tokens）
           + 当前用户消息（~100-500 tokens）
总计：约 20,000-75,000 tokens
```

发送给大模型的 JSON 格式：

```json
{
    "model": "anthropic/claude-sonnet-4-20250514",
    "messages": [
        {
            "role": "user",
            "content": "[系统提示词 + 项目上下文 + 会话历史 + 当前消息]"
        }
    ],
    "tools": [
        {"name": "read", "description": "Read file contents", "input_schema": {}},
        {"name": "write", "description": "Create or overwrite files", "input_schema": {}},
        "..."
    ],
    "system": "[可选的系统级覆盖]"
}
```

会话历史存储格式（JSON Lines）：

```json
{"type":"session","version":2,"id":"session-abc123","timestamp":"2024-01-15T10:30:00Z","cwd":"/Users/user/project"}
{"type":"user","role":"user","content":"你好","timestamp":"2024-01-15T10:30:01Z"}
{"type":"assistant","role":"assistant","content":"你好！有什么我可以帮助你的吗？","timestamp":"2024-01-15T10:30:02Z"}
{"type":"tool_call","name":"write","parameters":{"path":"script.py","content":"def hello():..."},"timestamp":"2024-01-15T10:30:04Z"}
{"type":"tool_result","name":"write","result":"Written successfully","timestamp":"2024-01-15T10:30:05Z"}
```

**3. 验证与优化**

```bash
# 检查上下文占用
/context list
# 输出示例：
# System prompt (run): 38,412 chars (~9,603 tok)
# TOOLS.md: TRUNCATED | raw 54,210 chars | injected 20,962 chars

# 检查会话状态
/status
# 输出示例：
# Context usage: 65,200 / 200,000 tokens (32.6%)
# History: 47 messages (23 user, 24 assistant)
```

---

### 💡 具体案例/数据

**系统提示词 25 个组件的完整构成**：

| # | 组件名称 | 类型 | 必需 | 作用 |
|---|---------|------|------|------|
| 1 | Identity Declaration | 核心 | ✅ | 定义 AI 基本身份 |
| 2 | Tooling | 核心 | ✅ | 列出可用工具及描述 |
| 3 | Tool Call Style | 行为 | ✅ | 指导如何使用工具 |
| 4 | Safety | 约束 | ✅ | 安全限制和指导原则 |
| 5 | CLI Quick Reference | 参考 | ✅ | 命令行快速参考 |
| 6 | Skills | 能力 | ⚪ | 技能系统指导 |
| 7 | Memory Recall | 记忆 | ⚪ | 记忆检索指导 |
| 8 | Self-Update | 能力 | ⚪ | 自更新指导（主模式） |
| 9 | Model Aliases | 配置 | ⚪ | 模型别名 |
| 10 | Workspace | 上下文 | ✅ | 工作空间信息 |
| 11 | Documentation | 参考 | ⚪ | 文档链接 |
| 12 | Sandbox | 环境 | ⚪ | 沙盒运行时信息 |
| 13 | Authorized Senders | 安全 | ⚪ | 授权发送者 |
| 14 | Date & Time | 上下文 | ⚪ | 时区信息 |
| 15 | Reply Tags | 交互 | ✅ | 回复标签指导 |
| 16 | Messaging | 交互 | ✅ | 消息传递指导 |
| 17 | Voice/TTS | 交互 | ⚪ | 语音合成提示 |
| 18 | Reactions | 交互 | ⚪ | 表情符号指导 |
| 19 | Group Chat Context | 上下文 | ⚪ | 群聊额外上下文 |
| 20 | Reasoning Format | 输出 | ⚪ | 思考格式 |
| 21 | Project Context | 上下文 | ⚪ | 项目特定文件 |
| 22 | Silent Replies | 交互 | ✅ | 静默回复规则（主模式） |
| 23 | Heartbeats | 监控 | ✅ | 心跳轮询机制（主模式） |
| 24 | Runtime | 元数据 | ✅ | 运行时元数据 |
| 25 | Context Files | 上下文 | ⚪ | 用户自定义上下文 |

**8 个工作空间文件的 token 规模参考**：

| 文件名 | 优先级 | 典型大小 |
|-------|--------|---------|
| SOUL.md | 🔴 最高 | 500-2,000 chars |
| AGENTS.md | 🟠 高 | 1,000-5,000 chars |
| IDENTITY.md | 🟠 高 | 200-1,000 chars |
| USER.md | 🟡 中 | 200-1,000 chars |
| TOOLS.md | 🟡 中 | 5,000-50,000 chars（超大，会被截断） |
| HEARTBEAT.md | 🟢 低 | 50-500 chars |
| BOOTSTRAP.md | 🟢 低 | 0-3,000 chars |
| MEMORY.md | 🟢 低 | 1,000-10,000 chars |

**实际案例 token 消耗**（用户消息："帮我分析这个项目的代码结构，并生成文档"）：
- 系统提示词：~30,000 tokens
- 项目上下文：~15,000 tokens
- 会话历史：~20,000 tokens
- 当前消息：~200 tokens
- **总计：~65,200 tokens**（这是 OpenClaw 高 token 消耗的根本原因）

**Gateway 路由规则示例**：

| 来源 | 条件 | 路由到 | 原因 |
|------|------|--------|------|
| 飞书 + 工作群 | — | 小ai | 处理工作任务 |
| 企业微信 + 用户小明 | — | Sage | 亲切聊天 |
| 其它所有情况 | — | Helper | 通用助手兜底 |

---

### 📝 避坑指南

- ⚠️ **TOOLS.md 超大会被截断**：raw 54,210 chars 只注入 20,962 chars，工具文档过长会导致部分工具描述丢失，需

---

---

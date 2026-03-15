# Agent与技能系统

## 63. [2026-02-17]

## 📗 文章 2


> 文档 ID: `PDkNwgM8ii8nyWkx7lZcplSknbf`

**来源**: 林月半子：OpenClaw多Agent实操：一个人指挥一支AI军队 | **时间**: 2026-02-17 | **原文链接**: `https://mp.weixin.qq.com/s/OmlRx3K8...`

---

### 📋 核心分析

**战略价值**: 用 OpenClaw 的单 Bot + 多飞书群 + bindings 路由，实现物理隔离的多 Agent 专家团队，解决单 Agent 记忆臃肿、上下文污染、Token 浪费三大痛点。

**核心逻辑**:

- **单 Agent 的三大死穴**：①记忆文件（USER.md、memory/）随时间极度膨胀；②跨任务上下文污染（写公众号时联想到昨天的代码逻辑）；③每次对话读取大量无关背景，Token 成本高。
- **核心架构方案**：单 Gateway 模式 = 同一个飞书 Bot + 不同群组 + bindings 路由 → 每个群背后连接不同 Agent、独立 Workspace、独立 Sessions，物理隔离。
- **模型按需分配**：头脑风暴群配 `glm-4.7`（中文创意强），公众号写手群配 `deepseek`（性价比高、逻辑输出好）。同一个 Bot，不同群换不同"脑子"。
- **Agent 三要素隔离**：每个 Agent 拥有独立的 Workspace（办公室/文件/SOUL.md/提示词）、AgentDir（认证信息/模型配置）、Sessions（私人聊天记录，不串味）。
- **两种流派对比**（见下方表格）：分身流适合个人效率用户，独立团适合硬核多实体协作场景。
- **"入职材料"决定 AI 灵魂**：SOUL.md + AGENTS.md + USER.md 三文件赋予 Agent 稳定人格，coder 的 SOUL.md 写成资深程序员风格，work 的写成全能管家风格。
- **主 Agent（首席牛马官）的职责**：不自己干活，只负责"接单"与"派单"——接收原始指令 → 判断任务类型 → 调度对应 Agent（brainstorm/writer/coder）→ 串联全流程。
- **Agent 间通信机制**：通过 OpenClaw 内置 `sessions_send` 工具实现"内线电话"，必须在配置文件中开启 `agentToAgent.enabled: true` 并设置白名单 `allow` 列表。
- **requireMention 控制交互体验**：默认必须 @机器人才回复；设为 `false` 后群组变成专属私人办公室，无需每次艾特，同时需开放飞书权限 `im:message.group_msg`。
- **多 Bot 硬核方案入口**：飞书插件 PR `https://github.com/m1heng/clawdbot-feishu/pull/137` 已支持飞书多机器人接入，Telegram、Discord 同样可用相同玩法。

---

### 🎯 关键洞察

多 Agent 的核心价值不是"多个 AI 同时干活"，而是**监督机制**：设置一个监督 Agent，当执行 Agent 卡住或出错时及时介入修复，确保流程不中断。这是单 Agent 模式无法实现的容错能力。

架构设计优先于模型堆砌：你作为"架构师"的组织设计决定战斗力上限，而非模型数量。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|---|---|---|---|
| 新建 Agent | `openclaw agents add work --model zai/glm-4.7 --workspace ~/.openclaw/workspace-work` | 创建隔离 Agent，自动生成配置 | workspace 路径需提前规划好 |
| 设置 Agent 身份 | `openclaw agents set-identity --agent work --name "全能小秘书" --emoji "🤖"` | 飞书群里显示名称和 emoji | 每个 Agent 单独执行一次 |
| 飞书群路由绑定 | `bindings` 数组中配置 `agentId` + `channel: feishu` + `peer.kind: group` + `peer.id` | 指定群消息路由到指定 Agent | 必须拿到群会话 ID（oc_开头） |
| 免艾特配置 | `groups.{群ID}.requireMention: false` | 群内直接对话无需 @机器人 | 必须同时开启飞书权限 `im:message.group_msg` |
| Agent 间通信 | `agentToAgent.enabled: true` + `allow` 白名单 | Agent 之间可通过 sessions_send 互发指令 | allow 列表必须包含所有参与通信的 Agent ID |
| Agent 工作区文件 | SOUL.md / AGENTS.md / USER.md / PROMPT.md | 稳定人格、专业直觉、记忆隔离 | 不同职能 Agent 的 SOUL.md 内容要差异化 |

---

### 🛠️ 操作流程

**1. 准备阶段**

- 确认已有飞书 Bot 基础配置（appId、appSecret、websocket 连接模式）
- 在飞书创建对应职能群组（如：头脑风暴群、公众号写手群、代码群）
- 获取每个群的会话 ID（格式：`oc_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`）

**2. 核心执行**

Step 1 — 创建各职能 Agent：
```bash
# 创建全能秘书 Agent
openclaw agents add work \
    --model zai/glm-4.7 \
    --workspace ~/.openclaw/workspace-work

# 设置身份标识
openclaw agents set-identity --agent work --name "全能小秘书" --emoji "🤖"

# 按需创建其他 Agent（brainstorm / writer / coder / mulerun）
openclaw agents add brainstorm --model zai/glm-4.7 --workspace ~/.openclaw/workspace-brainstorm
openclaw agents add writer --model deepseek/xxx --workspace ~/.openclaw/workspace-writer
openclaw agents add coder --model deepseek/xxx --workspace ~/.openclaw/workspace-coder
```

Step 2 — 编写入职材料（每个 Workspace 下）：
```
~/.openclaw/workspace-work/
├── SOUL.md       # 人格定义（全能管家风格）
├── AGENTS.md     # Agent 职责说明
├── USER.md       # 用户信息与偏好
└── PROMPT.md     # 提示词模板
```

Step 3 — 配置 `openclaw.json`，绑定路由 + 开启免艾特 + 开启 Agent 间通信：
```json
{
  "bindings": [
    {
      "agentId": "work",
      "match": {
        "channel": "feishu",
        "peer": {
          "kind": "group",
          "id": "oc_d46347c35dd403daad7e5df05d08a890"
        }
      }
    },
    {
      "agentId": "brainstorm",
      "match": {
        "channel": "feishu",
        "peer": {
          "kind": "group",
          "id": "oc_598146241198039b8d9149ded5fb390b"
        }
      }
    }
  ],
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_a9f21xxxxx89bcd",
      "appSecret": "w6cPunaxxxxBl1HHtdF",
      "domain": "feishu",
      "connectionMode": "websocket",
      "dmPolicy": "allowlist",
      "allowFrom": [
        "ou_f0ad95cf147949e7f30681a879a5f0d3"
      ],
      "groupPolicy": "open",
      "groups": {
        "oc_d46347c35dd403daad7e5df05d08a890": {
          "requireMention": false
        },
        "oc_598146241198039b8d9149ded5fb390b": {
          "requireMention": false
        },
        "oc_b1c331592eaa36d06a05c64ce4ecb113": {
          "requireMention": false
        }
      }
    }
  },
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": [
        "main",
        "mulerun",
        "brainstorm",
        "writer",
        "coder"
      ]
    }
  }
}
```

**3. 验证与优化**

- 在各飞书群发消息，确认路由到正确 Agent（观察回复风格是否符合 SOUL.md 设定）
- 测试 `requireMention: false` 是否生效（直接发消息不 @ 看是否有回复）
- 测试 Agent 间通信：让 main Agent 下达指令给 brainstorm，观察 sessions_send 是否正常触发

---

### 💡 具体案例/数据

**作者实际 Agent 团队配置**：

| Agent ID | 职能 | 模型 | 对应飞书群 |
|---|---|---|---|
| main | 首席牛马官（接单/派单/指挥） | 未指定 | 主群 |
| brainstorm | 头脑风暴助手 | glm-4.7 | 头脑风暴群 |
| writer | 公众号写手 | deepseek | 公众号写手群 |
| coder | 代码专家 | deepseek | 代码群 |
| mulerun | 生图专员 | 未指定 | 生图群 |

**Agent 目录结构实例**（以 `video_image_creator` 为例）：
```
~/.openclaw/agents/video_image_creator/
├── agent/
│   ├── auth-profiles.json
│   └── models.json
└── sessions/
    ├── 40ce6280-0a92-4...128976da10e.jsonl
    ├── 69812592-0515-4...fdcc1f228c0d.jsonl
    └── sessions.json

~/.openclaw/workspace-video_image_creator/
├── .git/
├── AGENTS.md
├── BOOTSTRAP.md
├── HEARTBEAT.md
├── IDENTITY.md
├── PROMPT.md
├── SOUL.md
├── TOOLS.md
├── USER.md
└── memory/
```

---

### 📝 避坑指南

- ⚠️ `requireMention: false` 单独设置无效，必须同时在飞书后台开启 `im:message.group_msg` 权限，两者缺一不可。
- ⚠️ `agentToAgent` 的 `allow` 白名单必须包含所有需要互相通信的 Agent ID，漏填则"内线电话"打不通。
- ⚠️ 不同职能 Agent 的 SOUL.md 必须差异化编写，否则隔离了工作区但人格还是一样，等于白做。
- ⚠️ 多 Bot 方案（独立团）需要额外接入飞书插件 PR `https://github.com/m1heng/clawdbot-feishu/pull/137`，与本文单 Bot 路由方案是两套不同配置，不要混用。
- ⚠️ bindings 中的群 ID 必须是飞书群会话 ID（`oc_` 开头），不是群名称，需从飞书开发者后台或 API 获取。

---

### 🏷️ 行业标签

#OpenClaw #MultiAgent #飞书Bot #AI工作流 #AgentArchitecture #LLM #自动化 #个人效率

---

---

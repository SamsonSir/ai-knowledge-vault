# Agent与技能系统

## 72. [2026-02-22]

## 📙 文章 4


> 文档 ID: `NtiLwrsytin0p3kQIMMcRn0lnHS`

**来源**: OpenClaw多Agent实操：5个AI当着你的面分工协作，全程透明不黑箱 | **时间**: 2026-02-22 | **原文链接**: `https://mp.weixin.qq.com/s/xLzHLwFD...`

---

### 📋 核心分析

**战略价值**: 用 OpenClaw + Discord 实现"单渠道多账户"多 Agent 同频可见协作，5个独立 Bot 在同一频道实时分工，全程透明可干预，解决的是协作可见性而非纯效率问题。

**核心逻辑**:

- **两种模式本质区别**：飞书"分身术"= 单账户按群 ID 路由，一个 Bot 扮多角色，极简轻量；Discord"独立团"= 每个专家角色对应独立 Bot 账户，同频群聊，身份边界清晰，适合演示、团队展示、过程可干预场景
- **为什么需要"灵统"指挥官**：平等协作会导致"全部抢答"或"全部沉默"两种灾难，灵统作为唯一拍板者负责任务接收与分派，其他 Agent 只负责执行本职
- **广播机制 vs 后台调用**：传统 `sessions_send` 是后台静默，用户只看结果；本方案用全公开广播机制，每个 Bot 的发言都在频道可见，可随时打断修正
- **物理隔离防神经错乱**：每个 Agent 对应独立 Workspace 目录（`~/.openclaw/workspace-ds-xxx`），防止上下文污染和角色混淆
- **`sessions.visibility: "all"` 是灵魂开关**：不开启则每个 Bot 只知道自己被艾特，看不见其他 Bot 的输出；开启后所有 Agent 共享频道全量上下文，实现"圆桌会议"效果
- **`allowBots: true` 是必须项**：OpenClaw 默认 Bot 不理会 Bot（防死循环），但军团模式下指令由灵统发出，不开此项子 Agent 全部装聋
- **`requireMention: true` 防死循环**：必须艾特才响应，配合 users 白名单（只听指定用户和其他4个 Bot 的指令），防止 Bot 间对话无限循环
- **三层 mentionPatterns 保证唤醒精度**：`<@!?BotID>`（原生 ID 最稳健）+ 昵称简称（增强）+ 纯数字 ID（兜底），三层匹配缺一不可
- **channels 白名单逻辑**：不写 channels 默认监听全服；只要写了一个频道，立即进入白名单模式，其他频道全部屏蔽，防止 Bot 在闲聊区刷屏
- **agentToAgent 权限是协作前提**：必须在 tools 中显式开启并列出所有允许互通的 Agent ID，灵统才能向其他专家发派任务

---

### 🎯 关键洞察

**多 Agent 本质是组织管理问题，不是技术问题。**

- 原因：技术层面 Sub-agent 已经够用，但"谁在做决策、决策过程是否可见、中途能否干预"这些是组织设计问题
- 动作：设计清晰的指挥链（灵统→灵策/灵工/灵文/灵核），用 `requireMention` + `users` 白名单 + `allowBots` 三重机制约束行为边界
- 结果：实现"所见即所得"协作——灵文能感知灵策刚定的调性，直接在其基础上创作，无需人工中转

**两种统帅逻辑的实战差异**：
- 模糊指派：只 @灵统 说目标，由灵统判断派给谁 → 适合目标明确但不想管细节的场景
- 精准委派：在指令里直接排兵布阵，指定灵策定调、灵文执行 → 适合对产出有特定要求的场景

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| Bot 感知能力 | Discord 开发者门户 → Bot → 勾选 `SERVER MEMBERS INTENT` + `MESSAGE CONTENT INTENT` | Bot 能读取消息内容和成员信息 | 两个都要勾，漏一个 Bot 变聋子/瞎子 |
| OAuth2 邀请 | OAuth2 → URL Generator → 勾选 `bot` → 勾选必要 Bot Permissions → 复制链接邀请入服务器 | Bot 进入私有服务器 | 5个应用各做一遍 |
| Agent 创建 | `openclaw agents add ds-xxx --model zai/glm-4.7 --workspace ~/.openclaw/workspace-ds-xxx` | 生成独立 Workspace 目录 | 验证：查看 `~/.openclaw/openclaw.json` 的 `agents.list` 是否有5个独立 ID 块 |
| 路由绑定 | `bindings` 数组中 `agentId` 对应本地 Agent，`accountId` 对应 Token 别名 | Discord 消息路由到正确 Agent | `accountId` 必须与 `channels.discord.accounts` 键名完全一致，写反必翻车 |
| Bot 互通 | `"allowBots": true` | 子 Agent 响应灵统发出的指令 | 默认为 false，不改则子 Agent 全部无视灵统 |
| 防死循环 | `"requireMention": true` + `users` 白名单列表 | 只响应艾特+白名单用户 | 白名单必须包含你自己的 ID 和所有5个 Bot 的 ID |
| 上下文穿透 | `"sessions": {"visibility": "all"}` | 所有 Agent 共享频道全量上下文 | 不开则每个 Bot 只知道自己被艾特，看不见其他 Bot 的输出 |
| Agent 互发任务 | `"agentToAgent": {"enabled": true, "allow": ["ds-lingzong", ...]}` | 灵统能向其他专家发派任务 | allow 列表必须包含所有参与协作的 Agent ID |
| 唤醒识别 | `mentionPatterns`: 原生 ID 正则 + 昵称 + 纯数字 ID | 精准捕捉属于自己的指令 | 三层都要配，只配一层在复杂群聊中容易漏触发 |
| 频道隔离 | `channels: {"频道ID": {"allow": true}}` | Bot 只在指定频道活动 | 写了一个频道就进入白名单模式，其他频道全屏蔽 |
| 关闭 reactions | `"reactions": false` | 防止 Bot 互刷表情触发意外 | 保持 `"messages": true` 即可 |

---

### 🛠️ 操作流程

**Step 1. Discord 开发者门户 — 为每个角色创建应用**

1. 访问 `https://discord.com/developers/applications` → New Application
2. 命名建议统一前缀：灵统、灵策、灵工、灵文、灵核
3. 左侧 Bot 页面 → 勾选 `SERVER MEMBERS INTENT` + `MESSAGE CONTENT INTENT`（两个都要）
4. Reset Token → 保存密钥（唯一身份证）
5. OAuth2 → URL Generator → 勾选 `bot` + 必要 Bot Permissions → 复制链接 → 浏览器打开 → 邀请进私有服务器 → 授权
6. 重复以上步骤完成全部5个应用

**Step 2. 本地终端 — 创建5个独立 Agent**

```bash
# 1. 招募总指挥
openclaw agents add ds-lingzong --model zai/glm-4.7 --workspace ~/.openclaw/workspace-ds-lingzong
openclaw agents set-identity --agent ds-lingzong --name "总指挥"

# 2. 招募军师
openclaw agents add ds-lingce --model zai/glm-4.7 --workspace ~/.openclaw/workspace-ds-lingce
openclaw agents set-identity --agent ds-lingce --name "军师"

# 3. 招募工程师
openclaw agents add ds-linggong --model zai/glm-4.7 --workspace ~/.openclaw/workspace-ds-linggong
openclaw agents set-identity --agent ds-linggong --name "工程师"

# 4. 招募灵文（依此类推）
openclaw agents add ds-lingwen --model zai/glm-4.7 --workspace ~/.openclaw/workspace-ds-lingwen
openclaw agents set-identity --agent ds-lingwen --name "创作官"

# 5. 招募灵核
openclaw agents add ds-linghe --model zai/glm-4.7 --workspace ~/.openclaw/workspace-ds-linghe
openclaw agents set-identity --agent ds-linghe --name "灵核"
```

验证：打开 `~/.openclaw/openclaw.json`，确认 `agents.list` 中有5个独立 ID 块。

**Step 3. 配置路由绑定 — `~/.openclaw/openclaw.json` 的 `bindings` 数组**

```json
"bindings": [
  {
    "agentId": "ds-lingzong",
    "match": { "channel": "discord", "accountId": "lingzong" }
  },
  {
    "agentId": "ds-lingce",
    "match": { "channel": "discord", "accountId": "lingce" }
  },
  {
    "agentId": "ds-linggong",
    "match": { "channel": "discord", "accountId": "linggong" }
  },
  {
    "agentId": "ds-lingwen",
    "match": { "channel": "discord", "accountId": "lingwen" }
  },
  {
    "agentId": "ds-linghe",
    "match": { "channel": "discord", "accountId": "linghe" }
  }
]
```

**Step 4. 配置账号行为、白名单、工具权限**

在 `channels -> discord -> accounts` 下为每个账号补全（以 `lingce` 为例，其余4个同结构）：

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "allowBots": true,
      "actions": {
        "reactions": false,
        "messages": true,
        "threads": false
      },
      "accounts": {
        "lingce": {
          "token": "你的Bot Token",
          "groupPolicy": "open",
          "guilds": {
            "你的服务器ID": {
              "requireMention": true,
              "users": [
                "你的UserID",
                "灵工BotID",
                "灵文BotID",
                "灵核BotID",
                "灵统BotID",
                "灵策BotID"
              ],
              "channels": {
                "频道ID": { "allow": true }
              }
            }
          }
        }
      }
    }
  },
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": ["ds-lingzong", "ds-lingce", "ds-linggong", "ds-lingwen", "ds-linghe"]
    },
    "sessions": {
      "visibility": "all"
    }
  }
}
```

> 获取 ID 方法：Discord 开启开发者模式 → 右键目标 → 复制服务器ID / 频道ID / 用户ID

**Step 5. 配置每个 Agent 的 mentionPatterns**

在 `agents -> list` 下找到对应 Agent，添加 `groupChat` 配置（以灵统为例）：

```json
{
  "id": "ds-lingzong",
  "name": "ds-lingzong",
  "identity": { "name": "总指挥" },
  "groupChat": {
    "mentionPatterns": [
      "<@!?1474005066569617551>",
      "灵统",
      "1474005066569617551"
    ]
  }
}
```

其余4个 Agent 按此格式，替换对应 Bot ID 和昵称。

---

### 💡 具体案例/数据

**场景一：模糊指派**
- 指令：`@灵统 启动'灵系极简协作'！我想发个朋友圈，主题是'深夜还在折腾 OpenClaw 终于跑通了'`
- 结果：灵统判断核心在"内容创作"→ 直接委派灵文 → 灵文输出"简洁成就感"、"略带调侃"、"极简有力"三个版本 + 配图建议

**场景二：精准委派**
- 指令：`@灵统 启动'灵系极简协作'！主题同上，灵策：帮我定文案风格；灵文：根据军师调性写两段文案`
- 结果：灵统完成分工调度 → 灵策出列定调 → 灵文感知灵策在频道定的"凡尔赛"调性，直接在其基础上完成创作，无需人工中转

---

### 📝 避坑指南

- ⚠️ `MESSAGE CONTENT INTENT` 未勾选：Bot 无法读取任何消息内容，表现为上线但完全不响应
- ⚠️ `bindings` 中 `accountId` 与 `accounts` 键名不一致：某个 Bot 在 Discord 说话但不触发本地 Agent，优先检查此处映射
- ⚠️ `allowBots` 未设为 `true`：子 Agent 集体无视灵统发出的所有指令，表现为灵统说话后无人响应
- ⚠️ 白名单 `users` 未包含灵统 Bot ID：灵策等子 Agent 认为灵统是陌生人，拒绝执行任务
- ⚠️ `sessions.visibility` 未设为 `"all"`：灵文看不见灵策的定调输出，无法实现上下文穿透协作
- ⚠️ `channels` 写了一个频道后其他频道全屏蔽：这是白名单模式的默认逻辑，不是 Bug，确保把所有需要的频道都加进去
- ⚠️ `mentionPatterns` 只配一层：复杂群聊中容易漏触发，三层（原生ID正则 + 昵称 + 纯数字ID）都要配
- ⚠️ SOUL.md / IDENTITY.md / AGENTS.md 为空：Bot 上线但行为像空壳，角色人格文件决定 Agent 是"听话工具"还是"真正专家"

---

### 🏷️ 行业标签

#多Agent #OpenClaw #Discord #同频协作 #AgentOrchestration #LLM工程 #自动化工作流 #AI组织设计

---

---

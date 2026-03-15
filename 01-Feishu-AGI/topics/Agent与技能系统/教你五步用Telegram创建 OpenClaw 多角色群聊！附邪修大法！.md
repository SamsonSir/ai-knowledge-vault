# Agent与技能系统

## 107. [2026-03-07]

## 📙 文章 4


> 文档 ID: `RwGdwGJy6itKSkkNXjZcalk1n8e`

**来源**: 教你五步用Telegram创建 OpenClaw 多角色群聊！附邪修大法！ | **时间**: 2026-03-07 | **原文链接**: `https://mp.weixin.qq.com/s/qnMg3ApZ...`

---

### 📋 核心分析

**战略价值**: 用一个 OpenClaw Gateway + 一个 Bot Token，通过群组路由机制，在 Telegram 实现多角色 AI 团队（产品经理/工程师/QA/内容），记忆隔离、互不干扰，还能主 Agent 调度协作。

**核心逻辑**:

- **架构选择决定复杂度**：单 Bot 多群组适合个人/小团队（一个 Token 管所有 Agent）；多 Bot 多 Agent 适合需要人格隔离的场景（每个 Bot 独立记忆、独立身份）
- **Gateway 是核心枢纽**：它是本地 AI 代理服务器，负责接收 Telegram 消息 → 路由到对应 Agent → 调用 LLM → 返回结果，一个 Gateway 可托管无限个 Agent
- **群组路由是关键机制**：每个 Telegram 群的 Group ID（负数，如 `-1001234567890`）就是路由地址，Bot 通过 Group ID 判断该把消息交给哪个 Agent 处理
- **隐私模式是最高频踩坑点**：Bot 默认开启隐私模式，只能看到 @ 它的消息；必须在 BotFather 关闭 Group Privacy，且关闭后必须把 Bot 踢出群再重新拉入，否则设置不生效
- **Workspace 实现记忆隔离**：每个 Agent 有独立的 `workspace-xxx/` 目录，包含 `IDENTITY.md`（身份）、`MEMORY.md`（长期记忆）、`memory/`（日记），Agent 之间完全隔离
- **requireMention 控制抢消息**：多 Bot 共存时，只让一个 Bot 设为 `requireMention: false`（默认响应），其他全设为 `true`（需 @ 才响应），避免混乱
- **Prompt 驱动自动创建子 Agent**：不需要手动改配置文件，直接在主 Bot 私聊发一段结构化 Prompt，主 Agent 会自动完成子 Agent 创建、Workspace 初始化、路由绑定
- **权限管理分两层**：私聊用 `dmPolicy: "pairing"`（需配对码）；群组用 `groupPolicy: "allowlist"` + `allowFrom` 白名单（填用户 ID 或群组 ID）
- **模型按角色分配**：`gpt-4o` 综合能力强，`claude-3-5-sonnet` 写代码/推理更强，`gpt-4o-mini` 快速省资源，在创建子 Agent 的 Prompt 里直接指定 Model 字段
- **主 Agent 可调度子 Agent 协作**：在主 Bot 私聊里发指令，主 Agent 自动调用对应子 Agent，把结果汇总返回，实现"一个人指挥 AI 团队"

---

### 🛠️ 操作流程

#### 第一步：创建主 Bot（约 5 分钟）

1. Telegram 搜索 `@BotFather`，发送 `/newbot`
2. 输入 Bot 名称（如 `lifezhushou`）
3. 输入用户名（必须以 `bot` 结尾，如 `lifezhushou_bot`）
4. 复制返回的 Token（格式：`123456:ABC-DEF...`），**不要泄露**
5. 接入 OpenClaw：
   ```
   openclaw config
   # 进入 Channels → Telegram → 粘贴 Token
   ```
6. 配对：在 Telegram 与 Bot 私聊，发送 `/start` 获取 Pairing Code，然后执行：
   ```
   openclaw pairing approve telegram <你的Pairing Code>
   ```
   > Pairing Code 类似验证码，一次配对永久生效。也可以直接把操作步骤发给 OpenClaw，让它引导你完成。

---

#### 第二步：开启群组权限（必做，勿跳过）

```
@BotFather → /mybots → 选择你的 Bot
→ Bot Settings
→ Allow Groups: Enable（允许加群）
→ Group Privacy: Disable（关闭隐私模式）
```

⚠️ **改完后必须把 Bot 从群里踢出，再重新邀请进群，否则设置不生效。**

---

#### 第三步：创建群组，获取 Group ID

1. 新建 Telegram 群（建议用角色命名，如 `虾友们`）
2. 把主 Bot 拉进群
3. 在群里 @ 你的 Bot，发送：`当前群组的 ID 是什么？`
4. Bot 回复一串负数，如 `-1001234567890`，复制保存备用

---

#### 第四步：用 Prompt 自动创建子 Agent（核心步骤）

回到主 Bot 私聊，发送以下 Prompt（替换 `【】` 内容）：

```
你现在是我的 OpenClaw 主控 Agent，请严格按照以下步骤为我创建一个全新的独立子 Agent：

1. Agent 基本信息：
- Name: 【子 Agent 名称，例如 产品经理】
- Model: 【模型，例如 gpt-4o 或 claude-3-5-sonnet】
- Workspace: 新建独立 workspace（名称同 Name）
- Personality: 【角色描述，例如"你是资深产品经理，擅长需求分析、用户研究和产品规划"】

2. 配置路由 Bindings：
- 使用 accountId: "main"
- 绑定两种 peer 类型：
  - peer.kind: "group", peer.id: 【你的 Group ID】
  - peer.kind: "channel", peer.id: 【同上】
- 所有消息路由到这个新 Agent

3. 群组策略：
- requireMention: false（群内无需 @ 就能直接回复）
- groupPolicy: "open"（所有人消息可见）
- allowFrom: ["*"]（开放权限）

4. 防抢消息：
- 为主 Agent 添加 client: "direct" + 你的 Telegram 用户 ID 白名单

请立即执行以上配置，完成后回复确认信息。
```

发送后等待 **10-30 秒**，主 Agent 自动创建子 Agent 并返回确认。

---

#### 第五步：测试 + 扩展更多角色

1. 去刚创建的群组，直接发消息（如：`帮我汇总今天的最新 AI 新闻`）
2. 子 Agent 正常回复 → 配置成功
3. 重复第三步 + 第四步，继续创建更多角色：
   - QA Agent：擅长写测试用例、找 Bug
   - 工程师 Agent：写代码、做架构
   - 内容 Agent：写推文、做文案
4

---

---

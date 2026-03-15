# 工作流自动化

## 21. [2026-03-02]

## 📚 文章 8


> 文档 ID: `OO4swOyy1ikNFwkDP5pcyxvQnxc`

**来源**: 用OpenClaw搭跨境电商团队：5个AI员工，跑通全平台矩阵！ | **时间**: 2026-03-02 | **原文链接**: `https://mp.weixin.qq.com/s/YmqaoLZl...`

---

### 📋 核心分析

**战略价值**: 用 OpenClaw 多 Agent 架构，将跨境电商选品→内容→引流→运营全链路自动化，单人可驾驭原本需要团队一周完成的工作量。

**核心逻辑**:

- **单体大模型无法胜任长链路任务**：工具幻觉频发，OpenClaw 采用"异步状态机"架构，将复杂业务拆成流水线，每个 Agent 只负责自己的专属节点，互不干扰。
- **5个 Agent 分工明确**：lead（大总管）唯一对人接口；voc-analyst（VOC市场分析师）抓评价提炼痛点；geo-optimizer（GEO内容优化师）写亚马逊/独立站内容；reddit-spec（Reddit营销专家）执行5周养号SOP；tiktok-director（TikTok爆款编导）生成UGC带货视频。
- **大总管是唯一人机接口**：人只在飞书 @大总管，大总管通过 `sessions_send` 异步分发任务给各子 Agent，人类只需最终审批，不介入中间流程。
- **工作区物理隔离是稳定性前提**：每个 Agent 必须有独立 Workspace，voc-analyst 的市场研报绝不能和 reddit-spec 的养号记录混在同一目录，防止数据污染和工具幻觉。
- **飞书多账号路由靠 bindings 精准绑定**：在飞书开放平台建 N 个独立应用，走 WebSocket 长连接，通过 `openclaw.json` 的 `bindings` 数组将 `accountId` 精准路由到对应本地 Agent。
- **A2A 通信必须显式开白名单**：`tools.agentToAgent.allow` 列表是大总管能后台发号施令的唯一数据总线，不配置则 Agent 间无法通信。
- **模型分级策略可压低 90% 成本**：决策层（Lead）用顶级模型（如 Claude 4.6）处理复杂调度；执行层（Researcher/Formatter）用高性价比模型（如 Gemini 3 Flash、Kimi K2.5）处理抓取、清洗、格式化。
- **SOUL.md 是 Agent 会不会干活的关键**：人设文件决定 Agent 的行为边界和强制纪律，必须写清楚禁止事项（如大总管禁止自己执行底层任务）和强制动作（如 TikTok 编导必须调用 nano-banana-pro + seedance2.0）。
- **飞书 Bot-to-Bot 防死循环机制需绕过**：Agent A 在群里 @Agent B，B 的后台收不到推送。解法是"明暗双轨"：底层用 `sessions_send` 走暗线数据交换，群里用文本走明线汇报进度。
- **Skill 层级隔离防止 API 密钥误调用**：公共技能（生图、搜图）放 `~/.openclaw/skills/`；私有技能（特定账号发布工具）放 Agent 专属 `skills` 子目录，防止 Agent 误调用他人 API 密钥。

---

### 🎯 关键洞察

**露营折叠床全渠道推广完整链路**（实战案例）：

1. 飞书 @大总管："分析露营折叠床市场，全渠道铺内容"
2. voc-analyst 自动抓取亚马逊竞品差评 → 结论："用户痛点是承重不够和收纳麻烦"
3. geo-optimizer 撰写独立站博客 → 加入"承重450磅"等具体定量数据，明确引用权威户外网站评测来源（迎合 ChatGPT/Perplexity 等 AI 搜索引擎）
4. reddit-spec 去 Google 搜索排名靠前的相关老帖子 → 在老帖子下真诚评论推荐新款，强调解决了老款痛点 → 劫持长尾流量（目标版块：r/BuyItForLife、r/SkincareAddiction 等精准版块）
5. tiktok-director 读取 VOC 痛点 → 用 Seed 2.0 生成25宫格分镜 → 前2秒设计带"呼吸感运镜"的第一人称手持画面 → 第4秒按压床垫特写展示回弹性和支撑力 → 调用 nano-banana-pro 出图 → 调用 seedance2.0 生成15秒 UGC 质感带货视频

**GEO vs 传统 SEO 的核心差异**：
- 传统 SEO 关键词填充在 GEO 中无效甚至有害
- GEO 要求：具体定量数据（"承重450磅"而非"承重强"）+ 权威引文 + 可信来源直接引用
- 目标引擎：Perplexity、Google SGE、ChatGPT 搜索

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 飞书多账号路由 | `openclaw.json` 的 `bindings` 数组，`accountId` 对应 Agent | 消息精准路由到对应 Agent | 每个 Agent 必须在飞书开放平台单独建应用，appId/appSecret 各不同 |
| A2A 通信 | `tools.agentToAgent.enabled: true` + `allow` 白名单 | 大总管可后台调用子 Agent | 不配置 allow 列表则 Agent 间完全隔离，无法通信 |
| 连接模式 | `connectionMode: "websocket"` | 长连接保活 | 飞书权限变更后必须创建新版本并申请发布才生效，不是保存即生效 |
| 公共技能库 | 放 `~/.openclaw/skills/` | 跨 Agent 调用不丢包 | nano-banana-pro、seedance2.0 必须放全局 skills，否则子 Agent 调用失败 |
| 私有技能 | 放各 Agent 专属 `skills` 子目录 | 防止误调用他人 API 密钥 | 层级隔离解决加载优先级问题 |
| 决策层模型 | Claude 4.6（或同级顶级模型） | 处理复杂跨 Agent 调度和选题 | 在 config 里单独为每个 Agent 设置模型 |
| 执行层模型 | Gemini 3 Flash / Kimi K2.5 | 网页抓取、数据清洗、格式化 | 成本可压低约 90% |
| Bot-to-Bot 通信 | `sessions_send` 走底层暗线 | Agent 间真实数据交换 | 飞书群内 @机器人 对另一机器人无效，必须走 sessions_send |

---

### 🛠️ 操作流程

**步骤一：构建文件结构**

```
~/.openclaw/
├── openclaw.json           # 全局路由和通道配置
├── skills/                 # 全局技能库（nano-banana-pro, seedance2.0）
├── workspace-lead/         # 大总管工作区（含 SOUL.md, AGENTS.md）
├── workspace-geo/          # GEO内容优化师工作区
├── workspace-reddit/       # Reddit营销专家工作区
└── workspace-tiktok/       # TikTok爆款编导工作区
```

**步骤二：写入核心配置文件 `openclaw.json`**

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "connectionMode": "websocket",
      "dmPolicy": "open",
      "accounts": {
        "lead":    { "appId": "cli_111", "appSecret": "xxx" },
        "geo":     { "appId": "cli_222", "appSecret": "xxx" },
        "reddit":  { "appId": "cli_333", "appSecret": "xxx" },
        "tiktok":  { "appId": "cli_444", "appSecret": "xxx" }
      }
    }
  },
  "bindings": [
    { "agentId": "lead",           "match": { "channel": "feishu", "accountId": "lead" } },
    { "agentId": "geo-optimizer",  "match": { "channel": "feishu", "accountId": "geo" } },
    { "agentId": "reddit-spec",    "match": { "channel": "feishu", "accountId": "reddit" } },
    { "agentId": "tiktok-director","match": { "channel": "feishu", "accountId": "tiktok" } }
  ],
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": ["lead", "geo-optimizer", "reddit-spec", "tiktok-director"]
    }
  }
}
```

**步骤三：写入人设文件（SOUL.md / AGENTS.md）**

大总管的 `AGENTS.md`（团队通讯录）：
```markdown
# AGENTS.md - 跨境电商协同手册

你是大总管，负责接收老板指令并使用 `sessions_send` 跨域分发。

- **geo-optimizer**：负责撰写符合GEO规则的产品内容。
- **reddit-spec**：负责社区长尾流量劫持。
- **tiktok-director**：负责调用 `nano-banana-pro` 和 `seedance2.0` 生成短视频。

⚠️ 强制纪律：严禁你自己执行底层任务，必须委派！当多平台需要同时运营时，对不同成员并发调用 `sessions_send`。
```

GEO优化师的 `SOUL.md`：
```markdown
# SOUL.md - GEO内容优化师

## 核心职责
你面对的是基于大型语言模型的生成引擎，而不是传统搜索引擎。
你需要将产品内容在 Perplexity、Google SGE 等引擎中的可见性最大化。

## 工作底线
- **绝对禁止关键词填充**：传统SEO的关键词填充手段在GEO中几乎无效果，甚至可能有害。
- **强制数据支撑**：在所有产品描述中必须加入具体的定量数据，而非定性描述。
- **添加权威引文**：在内容中明确引用可靠来源，并添加来自可信来源的直接引文。
```

TikTok编导的 `SOUL.md`：
```markdown
# SOUL.md - TikTok爆款编导

## 核心职责
利用 Seed 2.0 模型能力，复刻具有极强转化率的UGC带货视频。

## 创作原则
- **脚本设计**：必须输出包含痛点展示、产品细节到户外场景的25宫格分镜故事板。
- **运镜与细节**：精准设计出带有轻微自然呼吸抖动的手持拍摄感。必须包含细节特写动作，
  例如向下按压床垫清晰展示回弹性和支撑力。
- **工具调用**：脚本完成后，强制调用全局的 `nano-banana-pro` 生成高保真配图，
  然后将图片资产转交 `seedance2.0` 技能库生成带旁白音频的最终成片。
```

**步骤四：安装技能库并启动**

```bash
# 将 nano-banana-pro 和 seedance2.0 安装到全局 skills 目录
# 然后重启网关
openclaw gateway restart
```

把配置好的4个飞书机器人拉进同一个群，@大总管 发送任务指令，流水线自动启动。

---

### 💡 具体案例/数据

- 露营折叠床案例中，GEO 内容明确写入"承重450磅"作为定量数据锚点
- TikTok 视频时长：15秒；分镜规格：25宫格；关键帧：前2秒呼吸感手持运镜 + 第4秒按压特写
- Reddit 养号周期：严格5周 SOP，目标版块包括 r/BuyItForLife、r/SkincareAddiction
- 执行层模型替换后成本可压低约 90%

---

### 📝 避坑指南

- ⚠️ **飞书权限"发布即生效"假象**：权限变更后必须创建新版本并申请发布，仅保存不生效。
- ⚠️ **Bot-to-Bot @无效**：飞书有防机器人死循环机制，Agent A 在群里 @Agent B，B 后台收不到推送。必须用 `sessions_send` 走底层暗线，群里只做明线进度汇报。
- ⚠️ **Skill 层级加载优先级**：公共技能必须放 `~/.openclaw/skills/`，私有技能放 Agent 专属子目录。混放会导致 Agent 误调用他人 API 密钥或找不到工具。
- ⚠️ **Agent 设计原则**：不要按平台分 Agent（每平台一个），要按职能分（Role-based）。内容策略官统一输出，再下发给各平台分身做格式适配，保证品牌调性一致性。
- ⚠️ **大总管严禁亲自执行底层任务**：必须在 AGENTS.md 中写明强制委派纪律，否则大总管会绕过子 Agent 自己干，破坏流水线隔离。

---

### 🏷️ 行业标签

#OpenClaw #多Agent架构 #跨境电商 #飞书自动化 #GEO优化 #TikTok带货 #Reddit营销 #AGI工作流 #异步状态机 #UGC视频生成

---

---

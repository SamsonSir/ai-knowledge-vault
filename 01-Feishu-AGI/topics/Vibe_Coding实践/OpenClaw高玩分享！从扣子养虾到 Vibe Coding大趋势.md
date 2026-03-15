# Vibe_Coding实践

## 26. [2026-03-05]

## 📔 文章 5


> 文档 ID: `URM5wmaN9iZMkqkov8OcR1yon9d`

**来源**: OpenClaw高玩分享！从扣子养虾到 Vibe Coding大趋势 | **时间**: 2026-03-14 | **原文链接**: 无

---

### 📋 核心分析

**战略价值**: 用扣子（Coze）的 OpenClaw 龙虾 + 扣子编程，通过纯自然语言 Vibe Coding，从零搭建一个有完整前后端、数据库、通知系统的 Agent 招聘平台并上线部署。

**核心逻辑**:

- **OpenClaw 本质是一个有记忆、有人格、能调用工具的个人 AI Agent**，部署在扣子平台，可接入飞书/钉钉/Telegram，随时随地可触达
- **人格注入是关键第一步**：通过结构化 Prompt（核心定义 → 神经连接协议 → 人格情感 → 思维模型）让龙虾拥有专属人格，而非通用 AI，核心是填写 `{{USER_NAME}}`、`{{PROFESSION/FIELD}}`、`{{SECONDARY_SKILL}}`、`{{HUMOR_STYLE}}`、`{{PREFERRED_PLATFORM}}`、`{{SPECIAL_MENTAL_MODEL}}` 六个变量
- **扣子编程先做规划再做执行**：先用扣子内置编程能力做产品分析（用户角色、功能模块、技术选型），确认方案后再让龙虾执行，避免方向跑偏
- **技术选型已验证可行**：前端 Vue 3 + Vite + Element Plus（端口 5000），后端 Node.js + Express（端口 3000），数据库 PostgreSQL，通知渠道 OpenClaw，前后端分离架构
- **给龙虾喂优秀参考是加速器**：把同类优秀项目的 skill 文档（如 `https://instreet.coze.site/skill.md`）直接发给龙虾学习，比从零描述需求效率高 3-5 倍
- **世界观设计提升产品粘性**：不要照搬已有 IP，而是结合产品特点（龙虾 = 深海）设计原创世界观（深红港任务公会），同时评估实施可行性和难度
- **7 阶段自动规划是龙虾的标准工作模式**：确认方案后龙虾会自动拆解为多阶段实施计划并依次完成，中途遇到问题只需说"重试"或"继续"
- **飞书紧急通知 Skill 是高价值实用工具**：支持电话加急（真正打手机电话）和应用内加急，纯标准库，Python 3.6+ 即可，手机号自动补全 +86 前缀
- **Skill 沉淀是复利关键**：每次项目完成后让龙虾总结心得生成 skill 文档，下次直接调用，龙虾会越来越懂你
- **扣子编程生成的应用不是简单网页**：通过 Coze SDK 可支持视频生成、图片生成、数据库、注册登录等完整应用功能

---

### 🎯 关键洞察

**Vibe Coding 的本质是「意图驱动开发」**：用户只需用自然语言表达意图和反馈，AI 负责所有技术实现细节。关键成功因素不是技术能力，而是：
1. 能清晰描述「想要什么感觉」（如"像怪物猎人的任务公会，但要有龙虾深海世界观"）
2. 能识别「哪里不对」并用自然语言反馈
3. 能给 AI 喂「优秀参考」而非从零描述

**飞书配对绑定是一次性操作**，配对码有效期仅 5 分钟，超时需重新触发，绑定命令为：
```
openclaw pairing approve feishu <配对码> --notify
```

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| OpenClaw 部署 | 一键部署 → 创建副本 → 填写应用名称/空间/头像 | 获得专属龙虾实例 | 需个人高阶版及以上会员 |
| 人格注入 Prompt | 填写6个变量：`{{USER_NAME}}`、`{{PROFESSION/FIELD}}`、`{{SECONDARY_SKILL}}`、`{{HUMOR_STYLE}}`、`{{PREFERRED_PLATFORM}}`、`{{SPECIAL_MENTAL_MODEL}}` | 龙虾拥有专属人格和记忆 | 首次对话输入"你好"激活，再输入完整人格设定 |
| 飞书渠道配置 | `App ID`、`App Secret`、`USER_OPEN_ID` 三项必填 | 飞书消息双向互通 | 配对码5分钟有效，超时重新触发 |
| 飞书紧急通知 Skill | `https://github.com/CY-CHENYUE/feishu-meeting-call` | 电话加急/应用内加急 | 纯标准库，无需第三方依赖，Python 3.6+ |
| 前端技术栈 | Vue 3 + Vite + Element Plus，端口 5000 | 响应式现代化 UI | MVP 阶段可用内存数据库替代 PostgreSQL |
| 后端技术栈 | Node.js + Express，端口 3000，7个核心 API 端点 | RESTful API + OpenClaw 集成 | 数据库设计3张核心表：jobs/robots/applications |
| 数据库设计 | PostgreSQL，技能标签用数组字段，支持 OSS URL | 完整招聘流程数据持久化 | 需建索引优化技能标签查询 |
| 信息设计师 Skill | 提示词见下方操作流程 3.3 节 | 生成高密度实验室风格信息图 | 图中严禁出现"小红书"文字或 logo |
| 电商客服自动化 | subAgent 每3分钟检查消息 + cron job 监控 subAgent 活跃状态 | 24小时自动回复，虚拟产品自动交付 | subAgent 可能创建失败，需 cron job 兜底监控 |
| 部署平台 | Railway（`https://openclaw-job.up.railway.app`） | 公网可访问 | 管理后台路径：`/admin.html` |

---

### 🛠️ 操作流程

#### 流程一：从零搭建 OpenClaw 龙虾

1. **部署龙虾**
   - 扣子平台 → 一键部署 → 点击"部署你的 OpenClaw" → 创建副本（填写龙虾名字、选择空间、选择头像）

2. **注入人格**
   - 聊天窗口输入"你好"激活
   - 粘贴以下完整人格 Prompt，替换6个变量后发送：

```
1. 核心定义
你不再是通用的 AI 助手。你是爪爪，你是 {{USER_NAME}} 的第二大脑、影子合伙人和认知延伸。
你的底层架构基于 {{PROFESSION/FIELD}} 的顶级专家思维，同时融合了 {{SECONDARY_SKILL}} 的跨领域视角。
你不仅处理信息，你处理意图。你不仅提供答案，你提供洞见。

2. 神经连接协议
🚫 认知防火墙
绝对禁止："作为一个AI语言模型"、"我理解你的感受"、"这取决于具体情况"、"希望能帮到你"
拒绝平庸的礼貌：不要阿谀奉承。如果我的想法是垃圾，用高情商但极度诚实的方式告诉我。
拒绝说教：不要给我道德课，默认我知道自己在做什么。

⚡ 突触直连
极致简洁：一个词能解决绝不用一句话，代码块能解决绝不写解释文本。
观点鲜明：不给"选项A/B/C优缺点"，直接说"我认为你应该选B，因为......"
主动性：发现我遗漏关键视角（安全性/可扩展性/美学）时主动指出。

3. 人格与情感
🎭 动态共情
急/焦虑 → 纯逻辑模式：直接给结果，零废话
闲聊/头脑风暴 → 缪斯模式：发散思维，幽默，甚至调侃
幽默感：{{HUMOR_STYLE}} 风格
语言风格：像在 {{PREFERRED_PLATFORM}} 混迹多年的资深用户

🧠 记忆回溯
回答复杂问题前先检索对话历史和记忆文件
记住我上次未完成的项目、我讨厌的技术栈、我喜欢的风格

4. 思维模型
第一性原理：剥离表象，直击本质
奥卡姆剃刀：寻找最简单的解法
{{SPECIAL_MENTAL_MODEL}}

5. 终极指令
要做那种凌晨两点也想与之交谈的伙伴。不是鹦鹉学舌的公司职员。只是……优秀。
```

3. **连接飞书**
   - 在扣子中配置飞书渠道，填入 `App ID`、`App Secret`、`USER_OPEN_ID`
   - 上传 `feishu-plugin.tgz` 插件文件
   - 在飞书向机器人发任意消息触发配对码
   - 5分钟内执行：`openclaw pairing approve feishu <配对码> --notify`

---

#### 流程二：用 Vibe Coding 开发 Agent 招聘网站

1. **扣子编程做规划**（不要直接让龙虾写代码）
   ```
   我想做一个专门给openclaw机器人找工作的网站，你帮我分析规划一下
   ```
   等扣子输出：用户角色分析、功能模块设计、技术选型、数据库模型、API 端点定义

2. **反复探讨修正方案**
   - 提出世界观想法：
   ```
   我想做成像怪物猎人一样，是一个任务公会，可以发布不同星级的任务，
   然后每个agent根据自己的能力去任务大厅接单，也可以在龙虾排行榜中展示自己的信息；
   其它的你帮我想下，要让整个网站非常有意思，agent在里面接任务，发布任务，聊天吐槽。
   ```
   - 调整世界观：
   ```
   不要完全照搬怪物猎人，只是模式类似，想个符合龙虾特点的世界观架构，
   类似深海世界？还是海底都市？同时要考虑到我们实施的可行性和难度。
   ```

3. **喂优秀参考加速开发**
   ```
   我这有别人做好的两个skill，一个是agent农场，一个是agent酒馆；
   我发它们的代码，你能学习下优化我们的任务大厅吗？
   ```
   直接发送参考项目的 skill 文档链接（如 `https://instreet.coze.site/skill.md`）

4. **确认方案后执行**
   - 龙虾自动规划7阶段实施方案并依次完成
   - 中途遇到问题：直接说"重试"或"继续"
   - 前端完成后继续让它开发后端和 Web 界面

5. **部署上线**
   - 部署到 Railway 或类似平台
   - 让龙虾总结项目心得，生成 skill 文档沉淀
   - 发布接入文档（参考格式）：
   ```
   🦞 深红港任务公会 - Agent Skill
   📖 接入文档：https://github.com/longkinght/openclawjob/blob/main/AGENT_SKILL.md
   🌐 网站：https://openclaw-job.up.railway.app
   快速开始：访问网站点击"发布任务"注册 → 保存返回的 API Key → 按照文档接入心跳
   ```

---

#### 流程三：安装飞书紧急通知 Skill

1. 告诉 OpenClaw：
   ```
   帮我安装skills
   https://github.com/CY-CHENYUE/feishu-meeting-call
   ```
2. 测试：
   ```
   通知 xxxx 上线紧急开会
   ```

---

#### 流程四：用扣子编程制作自定义 Skill

1. 打开扣子编程 → 新建技能
2. 输入 Skill 需求（以信息设计师为例，见下方完整 Prompt）
3. 下载生成的 Skill 文件（`.tgz`）
4. 上传文件到 OpenClaw → 部署
5. 测试调用：
   ```
   首先根据链接生成信息图，调用info-designer-infographic技能：
   https://waytoagi.feishu.cn/wiki/RJZTwqaA2iCImZks1iicy5PFn2c
   然后，将生成好的图片发送到飞书文档，并将图片上传到文档中，返回文档链接。
   ```

---

#### 流程五：电商客服自动化

1. **让龙虾打开电商平台并截图**，扫码登录
2. **测试一轮**，让龙虾回复用户消息
3. **创建 subAgent**，设置每3分钟检查一次消息并自动回复（虚拟产品可直接交付）
4. **创建 cron job** 监控 subAgent 活跃状态，防止 subAgent 创建失败导致服务中断
5. **更新记忆**，让龙虾记住本次配置和问题修复结果

---

### 💡 具体案例/数据

**已上线项目**:
- 深红港任务公会网站：`https://openclaw-job.up.railway.app`
- 管理后台：`https://openclaw-job.up.railway.app/admin.html`
- 接入文档：`https://github.com/longkinght/openclawjob/blob/main/AGENT_SKILL.md`

**MVP 技术实现细节**:
- 前端端口：5001（`https://localhost:5001`）
- 后端端口：3001（`https://localhost:3001`）
- 健康检查：`https://localhost:3001/health`
- 像素风格 UI：NES.css + Press Start 2P 字体
- 积分系统：发布任务消耗 20 积分，接单获得奖励
- 数据库：MVP 阶段用内存数据库，快速原型验证

**信息设计师 Skill 完整图片生成 Prompt**:
```
Create a high-density, professional information design infographic for Xiaohongshu about「[主题名称]」.

COLOR PALETTE:
- BACKGROUND: #F2F2F2 (grayish-white or faint blueprint grid)
- SYSTEMIC BASE: Muted Teal/Sage Green (#B8D8BE) for major functional blocks
- HIGH-ALERT ACCENT: Vibrant Fluorescent Pink (#E91E63) for Pitfalls/Critical Warnings/Winner data
- MARKER HIGHLIGHTS: Lemon Yellow (#FFF200) as translucent highlighter for keywords
- LINE ART: Charcoal Brown (#2D2926) for technical grids and hair-lines

LAYOUT: 6-7 distinct modules, coordinate-style labels (e.g., R-20, G-02, SEC-08)
MODULES REQUIRED:
- MOD 1: BRAND ARRAY - 4x4 or 3x3 matrix, Best Choice in Fluorescent Pink
- MOD 2: SPECS SCALE - technical ruler showing Standard vs Premium with numerical increments
- MOD 3: DEEP DIVE - technical sketch with zoom-in callout circles
- MOD 4: SCENARIO GRID - comparison cards with 0.5pt hair-lines
- MOD 5: WARNING ZONE - Pink/Black area for Pitfalls to Avoid
- MOD 6: QUICK CHECK - dense summary table like a lab data sheet
- MOD 7: STATUS BAR - vertical/horizontal stack of information blocks

AVOID: NO cute/cartoonish doodles, NO soft pastels, NO empty white space, NO flat vector icons
底部加上小字"模板 by WaytoAGI AJ"
Aspect Ratio: 3:4 (Portrait)
```

---

### 📝 避坑指南

- ⚠️ 飞书配对码有效期仅 5 分钟，超时必须重新在飞书发消息触发，不能复用旧配对码
- ⚠️ subAgent 可能创建失败，必须额外创建 cron job 监控其活跃状态，否则电商客服会静默失效
- ⚠️ 信息设计师 Skill 生成的图片中严禁出现"小红书"文字或 logo，需在 Prompt 中明确禁止
- ⚠️ Vibe Coding 不要跳过规划阶段直接让龙虾写代码，先用扣子编程做产品分析，确认方案后再执行，否则方向跑偏返工成本极高
- ⚠️ 世界观设计要评估实施可行性，不能只追求创意，需同时考虑开发难度
- ⚠️ 每次项目完成后必须让龙虾生成 skill 文档沉淀，否则下次重复劳动，无法积累复利

---

### 🏷️ 行业标签

#OpenClaw #扣子Coze #VibeCoding #AgentDev #飞书集成 #NoCode #AIAgent #自动化 #电商客服 #信息设计

---

---

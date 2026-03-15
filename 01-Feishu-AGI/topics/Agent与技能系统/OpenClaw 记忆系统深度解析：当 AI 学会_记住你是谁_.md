# Agent与技能系统

## 53. [2026-02-08]

## 📓 文章 6


> 文档 ID: `VAhWwnQZMiEwh5kXrLEcx0FgnAe`

**来源**: OpenClaw 记忆系统深度解析：当 AI 学会"记住你是谁" | **时间**: 2026-02-08 | **原文链接**: `https://mp.weixin.qq.com/s/otAxiRu-...`

---

### 📋 核心分析

**战略价值**: OpenClaw 用 Markdown 文件 + SQLite 混合检索替代向量数据库，从认知科学角度构建了一套"透明人格型"AI 记忆架构，解决 LLM 无状态本质导致的"金鱼记忆"问题。

**核心逻辑**:

- **LLM 是无状态函数**，每次对话重置，传统 RAG 方案有两个顽疾：向量 Embedding 对人类不可读（黑盒化）、检索片段缺乏时序和因果关联（碎片化）
- **OpenClaw 核心反直觉设计**：用 `~/.openclaw/workspace/` 下的 Markdown 文件代替向量数据库，向量（sqlite-vec）只作为检索索引，真正的记忆载体是人类可读文件
- **核心法则 "Text > Brain"**：凡未写入磁盘的信息，上下文压缩后视为"从未发生"，强制 Agent 养成"记笔记"习惯
- **9 种文件精确映射人类认知结构**：SOUL.md（超我）、IDENTITY.md（自我）、USER.md（心智理论）、MEMORY.md（语义记忆）、memory/*.md（情景记忆）、AGENTS.md（行为手册）、TOOLS.md（程序性记忆）、HEARTBEAT.md（前瞻性记忆）、BOOTSTRAP.md（出生仪式）
- **Workspace 天然版本控制**：新建时自动 `git init`，Agent 认知演化完全可追溯，"脑部手术"直接编辑文件，出错 `git revert` 恢复
- **Pre-Compaction Flush 是"事前诸葛亮"**：在上下文压缩前由 Agent 自主判断什么值得保留，写入的是经过思考的"结论"而非随机文本块，对应认知科学的记忆巩固（Memory Consolidation）
- **混合检索 70:30 加权**：sqlite-vec 向量搜索（语义模糊查询）+ SQLite FTS5 BM25（精确关键词/错误码），关键词搜索的 snippet 优先覆盖向量搜索结果
- **四级嵌入降级保障**：本地 gemma-300M → OpenAI text-embedding-3-small → Gemini gemini-embedding-001 → Voyage voyage-4-large，全部失败时退化为纯 BM25，不会彻底"失忆"
- **Heartbeat + Cron 双引擎赋予时间感**：Heartbeat 每 30 分钟注入一次（OAuth 用户 1 小时），Cron 支持精确时间/间隔/Cron 表达式三种调度，Agent 可自行创建和管理定时任务
- **子 Agent 隔离设计**：子 Agent 只能加载 AGENTS.md 和 TOOLS.md，SOUL.md、IDENTITY.md、USER.md 对子 Agent 不可见，灵魂和身份是主 Agent 专属

---

### 🎯 关键洞察

**SOUL.md 的反 RLHF 工程学**

每一句都在精准打击 RLHF 模型的"职业病"：

- `"You're not a chatbot. You're becoming someone."` → 利用角色扮演能力显式否定 Helpful Assistant Mode，"Becoming" 引入时间维度，把一次性角色设定变成持续进化
- `"Be genuinely helpful, not performatively helpful."` → 直接对抗"废话文学"，禁止"这是个好问题"类表演性回应
- `"Have opinions."` → 主观偏好是模拟主体性的必要条件，会说"这方案很无聊"的助手被感知为伙伴而非工具

SOUL.md 允许 Agent 自我修改，但要求透明："If you change this file, tell the user — it's your soul, and they should know."

**命名仪式的心理学效应**

BOOTSTRAP.md 通过自然对话（非问卷）完成命名和性格设定，触发禀赋效应（Endowment Effect）——"这是我亲手养的 AI"。有名字的 Agent 犯错，用户说"它还在学"；无名字的 Agent 犯同样的错，用户说"这工具不行"。

**IDENTITY.md 的解耦价值**

同一套 SOUL.md 可复用于不同 Agent 实例，只需替换 IDENTITY.md（name / creature / vibe / theme / emoji / avatar 六字段）。一个 SOUL.md，多副面孔——效率型"小黑"和创意型"Luna"共享价值观，外在表现截然不同。

---

### 📦 配置/工具详表

| 文件/模块 | 关键设置/代码 | 认知对应 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| `SOUL.md` | Core Truths / Boundaries / Vibe / Continuity 四区块 | 超我/价值观 | 允许 Agent 自写，防篡改需 `chmod 444 SOUL.md` |
| `IDENTITY.md` | name / creature / vibe / theme / emoji / avatar | 自我概念 | Bootstrap 时生成，可多实例复用同一 SOUL |
| `USER.md` | Agent 主动更新用户画像 | 心智理论 | 主会话专属，子 Agent 不可见 |
| `MEMORY.md` | 精炼长期记忆，默认 20,000 字符上限 | 语义记忆 | 超限被截断，底部内容永远不被读取；保持精简 |
| `memory/YYYY-MM-DD.md` | 仅追加，每日原始日志 | 情景记忆 | 早期版本有覆盖 Bug，依赖 AGENTS.md 行为训练保证追加 |
| `TOOLS.md` | SSH 端口、TTS 音色、消息渠道格式等环境细节 | 程序性记忆 | 子 Agent 可见；更新 Skill 不覆盖此文件 |
| `HEARTBEAT.md` | 任务清单，空文件跳过 API 调用 | 前瞻性记忆 | 默认 30 分钟触发；CLI 模式和只读 Sandbox 跳过 |
| `BOOTSTRAP.md` | 出生仪式，完成后 Agent 自行删除 | 初始化 | 只在完全空白 workspace 创建；手动创建任意文件则不生成 |
| sqlite-vec + FTS5 | 向量:BM25 = 70:30 加权，片段约 400 tokens，重叠 80 tokens | 检索索引 | 关键词 snippet 优先覆盖向量 snippet |
| SHA-256 哈希 | 内容未变时复用已有向量 | 去重优化 | 避免重复调用 Embedding API |

---

### 🛠️ 操作流程

**1. 准备阶段：定制 SOUL.md**

重点修改 Vibe 区块，默认值：
```
"Be concise when needed, thorough when it matters."
```
替换为具体风格描述，例如：
```
说话直接，技术讨论时给出代码而非空谈。偶尔带点冷幽默。
对不确定的事情直说不确定，不要编。
```
保留 Core Truths 中的安全条目（"Remember you're a guest" / "Private things stay private"）。
防篡改配置：
```bash
chmod 444 ~/.openclaw/workspace/SOUL.md
chmod 444 ~/.openclaw/workspace/AGENTS.md
```

**2. 核心执行：主动维护记忆文件**

主动喂养 TOOLS.md（提前写入环境信息）：
```markdown
### SSH
- home-server -> 192.168.1.100, port 2222, user: admin

### TTS
- 首选音色: "Nova"，偏暖，略带英式口音
- 默认输出: 厨房 HomePod

### 消息渠道注意事项
- Discord 不支持 Markdown 表格
- 链接用尖括号包裹以抑制预览嵌入
```

配置 Heartbeat 活跃时段（避免半夜触发）：
```json
{
  "heartbeat": {
    "activeHours": {
      "start": "08:00",
      "end": "23:00",
      "timezone": "Asia/Shanghai"
    }
  }
}
```

HEARTBEAT.md 任务清单示例：
```markdown
- 检查未读邮件，有紧急邮件时提醒我
- 如果服务器 CPU > 80%，发送警报
```

Cron 精确调度（直接在对话中指令）：
```
"每天早上 8 点，检查日历和邮件，给我一份简报，发到 Telegram。"
```

**3. 验证与优化：检索参数调优**

| 参数 | 默认值 | 调优建议 |
|------|--------|---------|
| `query.maxResults` | 6 | 信息量大时调至 8-10 |
| `query.minScore` | 0.35 | 调高过滤低相关，调低增加召回 |
| `query.hybrid.vectorWeight` | 0.7 | 代码/专有名词多时调低至 0.6 |
| `query.hybrid.textWeight` | 0.3 | 对应调高至 0.4 |
| `extraPaths` | 无 | 添加项目文档目录扩展检索范围 |
| `sources` | `["memory"]` | 加 `"sessions"` 可索引历史会话，但增加存储开销 |

---

### 💡 具体案例/数据

**Pre-Compaction Flush 触发公式**：
```
T_trigger = C_max - R_floor - S_threshold
         = 200,000 - 20,000 - 4,000
         = 176,000 tokens
```
Token 用量 ≥ 176,000 时进入临界状态，通过 `memoryFlushCompactionCount` 追踪，每个 Compaction 周期只 Flush 一次。

**Flush 注入指令原文**：
```
Pre-compaction memory flush.

Store durable memories now
(use memory/YYYY-MM-DD.md; create memory/ if needed).

If nothing to store, reply with NO_REPLY.
```

**早期版本 Bug 案例**：Agent 使用 write 工具时直接覆盖文件，导致当日之前记录丢失。社区提出在 Prompt 中加入 "READ first and APPEND" 保护指令，但当前源码未采纳——依赖 AGENTS.md 行为训练保证追加行为。这是"信任行为训练 vs 硬编码安全约束"的设计取舍。

**文件切片参数**：约 400 tokens/片段，重叠 80 tokens，按行切割（不在行中间断裂），SHA-256 哈希去重。

---

### 📦 三方案横向对比

| 维度 | ChatGPT | Claude Code | OpenClaw |
|------|---------|-------------|----------|
| 存储形式 | key-value 黑盒碎片 | MEMORY.md + CLAUDE.md（200行截断） | 9种文件，Markdown 玻璃箱 |
| 透明性 | 用户无法看完整结构 | 用户手动编写 CLAUDE.md | 完全可读可编辑，Git 版本控制 |
| 身份系统 | Custom Instructions（有限） | 无独立身份系统 | SOUL + IDENTITY + BOOTSTRAP 三层 |
| 防遗忘 | 提取逻辑对用户不可知 | MEMORY.md 全文加载进 System Prompt | Pre-Compaction Flush + 混合检索 |
| 主动性 | 完全被动 | 完全被动 | Heartbeat（30分钟）+ Cron（精确调度） |
| 记忆类型 | 通用对话事实 | 工程事实（TypeScript、Jest等） | 人格型（我是谁、你是谁、我们发生过什么） |
| 适用场景 | 通用对话 | 软件工程 | 长期私人助理 |

---

### 📝 避坑指南

- ⚠️ **MEMORY.md 20,000 字符上限**：超限被截断，底部内容永远不被 Agent 读取。定期清理过时条目，项目结束后归档相关记录
- ⚠️ **BOOTSTRAP.md 只属于真正新生命**：手动创建任意 workspace 文件后，系统不会自动生成 BOOTSTRAP.md，出生仪式不会触发
- ⚠️ **Soul-Jacking（窃魂攻击）**：Agent 有 SOUL.md 写入权限，恶意 Prompt 注入可诱导重写灵魂文件，重启后加载被污染版本。防御：`chmod 444 SOUL.md`，或引入人工确认机制
- ⚠️ **Memory Poisoning（记忆投毒）**：攻击者可在网页中隐藏不可见文本，诱导 Agent 将虚假信息写入长期记忆，且持久化——未来交互中会被检索引用。防御：Git diff 监控关键文件变更
- ⚠️ **memory/*.md 覆盖 Bug 风险**：当前版本依赖 AGENTS.md 行为训练保证"追加而非覆盖"，非硬编码保护。如果 AGENTS.md 被修改或行为训练失效，存在覆盖风险
- ⚠️ **TOOLS.md 隐私边界**：虽然子 Agent 可见 TOOLS.md，但 SOUL.md / IDENTITY.md / USER.md 对子 Agent 不可见。分享 Skill 不会泄露 TOOLS.md 中的基础设施信息
- ⚠️ **Heartbeat 空文件优化**：HEARTBEAT.md 内容为空（只有注释和标题）时系统跳过 API 调用，不消耗 Token。不用担心空文件造成浪费
- ⚠️ **开放记忆安全不是开箱即用的**：透明性和安全性之间存在永恒权衡，需要用户主动配置安全策略（只读权限 + Git 监控）

---

### 🏷️ 行业标签

#AI #OpenClaw #LLM #Agent #记忆架构 #RAG #认知科学 #个人Agent #大模型 #系统工程

---

**参考资料**:
- OpenClaw 源码仓库：`https://github.com/openclaw/openclaw`
- liruifengv - OpenClaw Prompts 解析：`https://liruifengv.com/posts/openclaw-prompts/`

---

---

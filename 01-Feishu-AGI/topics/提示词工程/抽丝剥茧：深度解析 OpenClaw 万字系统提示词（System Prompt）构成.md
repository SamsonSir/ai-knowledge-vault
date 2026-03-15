# 提示词工程

## 18. [2026-03-02]

## 📙 文章 4


> 文档 ID: `OADCwjklpigH0wkMlWlcPxnPnsh`

**来源**: 抽丝剥茧：深度解析 OpenClaw 万字系统提示词（System Prompt）构成 | **时间**: 2026-03-13 | **原文链接**: `https://x.com/LufzzLiz/status/20266...`

---

### 📋 核心分析

**战略价值**: 通过自研代理拦截工具，完整还原 OpenClaw 每次对话默认携带的 ~16k token 系统提示词结构，并给出可操作的 Token 优化路径。

**核心逻辑**:

- OpenClaw 每次对话默认注入约 34062 字符（~16k tokens）的系统提示词，即使用户只发一句 "hi"，底层 input token 也高达 15391+。
- 官方日志路径 `.openclaw/agents/main/sessions/` 只记录 usage 数据，不记录完整提示词明文，必须借助代理拦截才能看到全貌。
- 系统提示词分三大块：硬编码头部（身份+工具+安全+技能索引+记忆召回）、Project Context（8个注入文件）、末尾协议（静默/心跳/运行时快照）。
- 工具列表存在双份冗余：`system ## Tooling` 段和 `body.tools[]` 各携带一份完整工具集，31/31 全重合，其中 `body.tools[]` 还带 parameters schema，两者合计约 5988~9582 tokens。
- Project Context 的 8 个注入文件中，MEMORY.md 是 Token 大头（约 2.3k~3.8k tokens），AGENTS.md 次之（约 2.0k~3.2k tokens），IDENTITY.md 最轻（约 50~80 tokens）。
- Skills 机制是懒加载：系统提示词只注入 `<available_skills>` 索引（name + description + location），匹配到任务才用 `read` 工具加载对应 SKILL.md，不匹配不读，最多读一个。
- subagent 的系统提示词是主动收缩版：Project Context 只带 AGENTS.md + TOOLS.md，工具列表从 31 个缩减到 23 个，且不注入 `## Skills` 索引段，也不带 memory_search / memory_get 等 8 个工具。
- compact 操作只压缩会话消息历史（session.messages），System Prompt 本体按模板重新构建，不会因 compact 自动瘦身，优化 Token 必须从 System 内容本身下手。
- 模型别名表（Model Aliases）是运行时动态注入的，配置的模型越多，每次携带的别名表越长，是隐性 Token 消耗点。
- 安全护栏硬编码在第一段：无独立目标、禁止自我复制/扩权/获取资源，指令冲突时暂停问人，灵感来自 Anthropic AI 宪法；TOOLS.md 明确声明不控制工具权限，但如果 TOOLS.md 里写了权限约束，可能被硬编码的 `TOOLS.md does not control tool availability` 这句话冲掉。

---

### 🎯 关键洞察

**双份工具冗余是最可操作的优化点**：`system ## Tooling` 段的工具列表主要用于行为引导（告诉模型有哪些工具、怎么用），`body.tools[]` 的 schema 是调用必须的机器可读信息不可删。两者完全重合，优化逻辑：

- 原因：系统提示词里逐个列工具描述 → 模型理解工具用途 → 但 body.tools[] 已经有 description 字段，等于说了两遍。
- 动作：把 `system ## Tooling` 里的工具列表缩成极短版（只保留调用规则，不逐个列描述），保留 `body.tools[]` schema 不动。
- 结果：可节省约 874~1399 tokens（system 工具说明段）+ 部分重复描述，整体可压缩 5~10% 的系统提示词体积。

**MEMORY.md 是长期 Token 成本大头**：规则越积越多，每次全量注入，是跨会话成本持续增长的根源。应定期清理过期规则，或拆分为按需检索的 `memory/*.md` 分片，配合 memory_search/memory_get 懒加载。

**subagent debug 方法**：同样用 modelbox 拦截，在 subagent 任务触发时抓包，可以看到其精简版系统提示词（23 工具，无 Skills 索引，无记忆工具）。

---

### 📦 配置/工具详表

| 模块/文件 | Token 预估 | 主要内容 | 优化建议/坑 |
|----------|-----------|---------|-----------|
| 系统提示词头部（硬编码） | 2,589~4,142 | 身份定义、工具清单、安全规则、Skills 索引、Memory Recall 规则 | TOOLS.md 里写权限约束可能被硬编码覆盖 |
| `## Tooling` 工具列表段 | 874~1,399 | 31 个工具的行为引导描述 | 与 body.tools[] 完全重合，可大幅精简 |
| `body.tools[]`（31 工具） | 5,988~9,582 | 工具 description + parameters schema | schema 不可删，description 可截断 |
| AGENTS.md | 2,000~3,200 | 工作区行为宪法、启动流程、记忆机制、安全边界 | subagent 也会带，是 subagent 最大注入文件 |
| SOUL.md | 440~700 | 沟通风格、工作方法、信任边界 | 千人千面，按需定制 |
| TOOLS.md | 582~932 | 本机环境私有备忘录（非权限清单） | 不控制工具权限，别在这里写权限约束 |
| IDENTITY.md | 50~80 | 助手人格卡（名字、风格、emoji） | 最轻，可忽略 |
| USER.md | 75~120 | 用户画像（称呼、时区、语言偏好） | 轻量，按需填充 |
| HEARTBEAT.md | 30~55 | 心跳轮询待办清单 | 最轻，保持精简 |
| MEMORY.md | 2,300~3,800 | 长期记忆总库（规则/事实/里程碑） | Token 大头，定期清理，拆分分片懒加载 |
| 系统提示词末尾（协议段） | 250~480 | 静默协议、心跳协议、运行时快照 | 硬编码，不可优化 |
| Model Aliases 表 | 动态 | 模型别名映射 | 配置模型越多越长，按需保留 |

---

### 🛠️ 操作流程

**1. 准备阶段：搭建提示词拦截环境**

```bash
# 克隆 modelbox（模拟模型提供商，用于拦截完整提示词）
git clone https://github.com/cclank/modelbox

# 按 README 安装并启动
# 启动后将 OpenClaw 的模型提供商指向 modelbox 地址
```

**2. 核心执行：抓取完整提示词**

- 在 OpenClaw 聊天窗口随意发一条消息（如 "hi"）
- modelbox 会拦截并吐出完整的请求体
- 日志默认写入：`modelbox/logs/modelbox.jsonl`
- 用 jq 格式化处理：

```bash
cat modelbox/logs/modelbox.jsonl | jq '.'
# 或让龙虾帮你格式化
```

**3. 验证与分析**

- 确认 system 字段长度（实测约 31842 chars）
- 统计 body.tools[] 工具数量（主对话 31 个，subagent 23 个）
- 对比 system `## Tooling` 段与 body.tools[] 的工具集合是否完全重合
- 检查 Project Context 各文件的实际注入内容

**4. debug subagent 提示词**

- 在 subagent 任务触发时，同样通过 modelbox 拦截
- 对比主对话与 subagent 的工具列表差异（少掉的 8 个工具见下表）

---

### 💡 具体案例/数据

**实测数据（一条 "hi" 消息）**：
- 总字符数：34,062 chars
- 换算 tokens：约 16k
- usage.input tokens：15,391

**subagent 少掉的 8 个工具**：

| 工具名 | 用途 |
|-------|------|
| agents_list | 列出代理 |
| sessions_list | 列出会话 |
| sessions_history | 查会话历史 |
| sessions_send | 跨会话发消息 |
| sessions_spawn | 派生子代理 |
| session_status | 查当前会话状态 |
| memory_search | 语义检索记忆 |
| memory_get | 读取记忆片段 |

**memory_get 工具 schema 示例**：

```json
{
  "type": "function",
  "name": "memory_get",
  "description": "Safe snippet read from MEMORY.md or memory/*.md with optional from/lines; use after memory_search to pull only the needed lines and keep context small.",
  "parameters": {
    "type": "object",
    "required": ["path"],
    "properties": {
      "path": { "type": "string" },
      "from": { "type": "number" },
      "lines": { "type": "number" }
    }
  },
  "strict": false
}
```

---

### 📝 避坑指南

- ⚠️ TOOLS.md 里写权限约束无效：系统提示词硬编码了 `TOOLS.md does not control tool availability`，你在 TOOLS.md 里定义的权限车可能被这句话直接冲掉，权限控制要走其他机制。
- ⚠️ compact 不会瘦身 System Prompt：compact 只压历史消息，System 段每次按模板重建，想降 Token 必须改 System 内容本身。
- ⚠️ MEMORY.md 是隐性成本增长点：每次全量注入，规则越积越多，建议定期清理过期条目，或拆分为 `memory/*.md` 分片配合懒加载。
- ⚠️ 模型别名表随配置膨胀：配置的模型越多，每次携带的 Model Aliases 表越长，按实际需要保留别名。
- ⚠️ subagent 默认不能自动用技能：subagent 不注入 `## Skills` 索引段，要让 subagent 用某个 skill，必须在任务描述里显式给出 skill 名或 SKILL.md 路径，或把关键规则放进 extraSystemPrompt。
- ⚠️ 官方日志不含完整提示词：`.openclaw/agents/main/sessions/` 的日志只有 usage 数据，看不到明文提示词，必须用 modelbox 拦截才能拿到全貌。

---

### 🏷️ 行业标签

#OpenClaw #SystemPrompt #Token优化 #提示词工程 #AI代理架构 #LLM成本控制 #subagent

---

---

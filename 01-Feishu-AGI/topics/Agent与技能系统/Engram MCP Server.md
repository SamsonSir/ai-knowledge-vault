# Agent与技能系统

## 79. [2026-02-24]

## 📙 文章 4


> 文档 ID: `HirFwn0C6iQ9KXkCes9cBgAonqd`

**来源**: Engram MCP Server | **时间**: 2026-03-13 | **原文链接**: `https://github.com/DazhuangJammy/Engram`

---

### 📋 核心分析

**战略价值**: 用 Markdown 文件给 AI 注入可切换的「完整专家人设」（谁 + 知道什么 + 怎么思考），零向量依赖，兼容所有 MCP 客户端，记忆可共享、可叠加。

**核心逻辑**:

- **Engram ≠ RAG**：RAG 只做语义检索，返回碎片；Engram 加载的是「角色人设 + 决策流程 + 规则 + 知识索引」完整骨架，人设和决策流程不会被漏掉
- **分层懒加载控制 token**：第一层（load_engram）常驻加载 role.md / workflow.md / rules.md 全文 + 两个 _index.md 索引；第二层（read_engram_file）由 LLM 根据索引摘要判断后按需拉取，不管 Engram 多大，每次注入量可控
- **人工策展 > 自动切分**：小规模高质量知识场景下，手工写的摘要和索引天然比向量自动切分精准，这是 Engram 在垂直场景跑赢 RAG 的根本原因
- **零向量依赖**：不依赖 chromadb / litellm / embedding 模型，只依赖 mcp，部署复杂度极低
- **记忆可共享**：把 `~/.engram/<name>/` 目录打包发给别人，对方 AI 立刻具备同一个专家的完整人设，共享的是 Memory 而非 Skills
- **多 subagent 并行**：同一个 Engram 可同时加载到 N 个 subagent，多智能体协作时每个 agent 都带完整专家上下文
- **身份注入框架**：不限于专家系统，任何「AI 需要成为某个角色」的场景都适用——聊天伙伴、语言陪练、模拟面试官、品牌客服、历史人物、项目上下文、过去的自己等 10+ 场景
- **cases → knowledge 关联**：案例文件头部用 `uses` frontmatter 标注引用的知识文件，_index.md 展示关联，模型可快速判断哪些案例和知识相关，避免孤立检索
- **workflow.md 可编排外部工具**：在决策节点直接指定调用哪个 MCP 工具或 Skill（如 git_log、grafana query_logs、/deploy-staging），Engram 变成完整专家工作台
- **三层能力分工**：Engram = 身份+知识+决策流程；MCP 工具 = 外部能力（数据库/监控/API）；Skills = 操作流程（部署/回滚/代码生成）

---

### 🎯 关键洞察

**为什么分层加载是核心设计**

原因：LLM context window 有限，全量塞入大型知识库会撑爆 token 且引入噪声。
动作：load_engram 只返回骨架（role + workflow + rules + 两个索引），索引里含内联摘要，LLM 读摘要后自己判断是否需要深入，再调 read_engram_file 拉全文。
结果：骨架常驻不丢人设，知识按需加载不浪费 token，Engram 规模可以无限扩大而不影响每次注入量。

**为什么「记忆共享」比「工具共享」更有价值**

工具（Skills/MCP）是操作能力，可以直接复用；但「判断力」——为什么这样决策、踩过哪些坑、在什么情况下用哪个工具——这些隐性知识无法通过工具共享传递。Engram 把这套判断力封装成 workflow.md + rules.md + knowledge/，共享后对方 AI 获得的不只是操作能力，而是完整的决策框架。

---

### 📦 配置/工具详表

| 工具 | 参数 | 返回内容 | 注意事项 |
|------|------|---------|---------|
| `ping` | 无 | `pong` | 连通性测试 |
| `list_engrams` | 无 | 所有 Engram 名称+描述+文件统计 | 对话开始时先调用 |
| `get_engram_info` | `name` | 完整 meta.json | 查看版本/标签/作者 |
| `load_engram` | `name`, `query` | role/workflow/rules 全文 + 知识索引 + 案例索引（含 uses） | query 影响摘要相关性排序 |
| `read_engram_file` | `name`, `path` | 单个文件全文 | 含路径越界保护，path 必须在 engram 目录内 |
| `install_engram` | `source`（git URL） | 安装结果 | 从远程 git 拉取并放入 packs-dir |

| CLI 命令 | 用法 | 说明 |
|---------|------|------|
| `serve` | `engram-server serve --packs-dir ~/.engram` | 启动 MCP stdio 服务（默认命令） |
| `list` | `engram-server list --packs-dir ~/.engram` | 列出已安装 Engram |
| `install` | `engram-server install <git-url> --packs-dir ~/.engram` | 从 git 安装 |
| `init` | `engram-server init my-expert --packs-dir ~/.engram` | 初始化空白模板 |

---

### 🛠️ 操作流程

**1. 准备阶段：安装依赖**

macOS/Linux 安装 Homebrew：
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

安装 uv（Python 包管理器，自动管理 Python 版本）：
```bash
# macOS/Linux via brew
brew install uv

# macOS/Linux via curl
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

克隆项目到固定路径（后续配置要用到）：
```bash
git clone https://github.com/DazhuangJammy/Engram.git ~/engram-mcp-server
# 克隆后无需 pip install，uv 自动处理依赖
```

**2. 核心执行：配置 MCP Server**

创建 Engram 存放目录：
```bash
mkdir -p ~/.engram
```

加载自带示例测试：
```bash
cp -r ~/engram-mcp-server/examples/fitness-coach ~/.engram/fitness-coach
```

在项目根目录创建 `.mcp.json`（Claude Code 用）：
```json
{
  "mcpServers": {
    "engram-server": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "~/engram-mcp-server",
        "engram-server",
        "--packs-dir", "~/.engram"
      ]
    }
  }
}
```

Claude Desktop 配置文件 `claude_desktop_config.json`：
```json
{
  "mcpServers": {
    "engram-server": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "/path/to/engram-mcp-server",
        "engram-server",
        "--packs-dir", "~/.engram"
      ]
    }
  }
}
```

Codex 配置相同结构，Cursor / Windsurf 在各自 MCP 配置入口填入相同 server 配置。

**3. 启用自动加载（三种方式选一）**

方式 A（推荐）：在 `CLAUDE.md`（Claude Code）或 `AGENTS.md`（Codex）开头加入：
```
你有一个专家记忆系统可用。对话开始时先调用 list_engrams() 查看可用专家。
当用户的问题匹配某个专家时，调用 load_engram(name, query) 加载常驻层和索引。
查看知识索引中的摘要，需要细节时调用 read_engram_file(name, path) 读取完整知识或案例。
用户也可以用 @专家名 直接指定使用哪个专家。
```

方式 B：服务暴露 `engram-system-prompt` MCP Prompt，支持该协议的客户端自动注入。

方式 C：零配置，list_engrams / load_engram / read_engram_file 工具描述已内置调用流程引导，部分客户端自动触发。

**4. 验证**

```bash
pytest -q
```

重启 AI 客户端，发送「我膝盖疼，还能做深蹲吗？」验证 fitness-coach 自动加载。

---

### 💡 具体案例/数据

**Agent 自动模式完整调用链**：
```
用户："我膝盖疼，还能做深蹲吗？"
  → agent 调用 list_engrams()，看到 fitness-coach
  → 判断匹配 → 调用 load_engram("fitness-coach", "膝盖疼深蹲")
  → 读知识索引摘要，判断需要深入
  → 调用 read_engram_file("fitness-coach", "knowledge/膝关节损伤训练.md")
  → 拿到完整知识 → 以专家身份回答
```

**Agent 手动模式**：
```
用户："@fitness-coach 帮我制定一个增肌计划"
  → agent 识别 @ 指令 → 直接调用 load_engram("fitness-coach", "增肌计划")
```
注意：@ 指令解析依赖 agent 端，MCP server 只提供工具，不处理消息格式。

**load_engram 返回内容格式**：
```
# 已加载 Engram: fitness-coach

## 用户关注方向
{query}

## 角色
{role.md 全文}

## 工作流程
{workflow.md 全文}

## 规则
{rules.md 全文}

## 知识索引
{knowledge/_index.md 内容，含内联摘要}

## 案例索引
{examples/_index.md 内容，含 uses 关联}
```

**workflow.md 编排外部工具示例**（来自 examples/project-context/workflow.md）：

| 动作 | 工具类型 | 调用方式 |
|------|---------|---------|
| 查看最近提交 | MCP 工具 | 调用 git MCP server 的 `git_log` |
| 查看服务日志 | MCP 工具 | 调用 grafana MCP server 的 `query_logs` |
| 部署到测试环境 | Skill | 触发 `/deploy-staging` skill |
| 回滚线上版本 | Skill | 触发 `/rollback` skill |

**11 个官方示例 Engram**：

| 示例目录 | 场景类型 | 说明 |
|---------|---------|------|
| `examples/template/` | 空白模板 | 创建新 Engram 的起点 |
| `examples/fitness-coach/` | 专家顾问 | 前康复机构训练主管，10年教练经验，增肌减脂+膝肩调整 |
| `examples/old-friend/` | 聊天伙伴 | 远在旧金山的老朋友，保留说话方式和记忆 |
| `examples/language-partner/` | 语言陪练 | 东京上班族，日语练习，自然纠错 |
| `examples/mock-interviewer/` | 模拟面试 | 技术面试全流程+反馈 |
| `examples/user-persona/` | 用户画像 | 产品验证用的目标用户角色 |
| `examples/brand-support/` | 品牌客服 | 统一话术和服务标准 |
| `examples/novel-character/` | 虚构角色 | 赛博朋克世界的黑客 |
| `examples/historical-figure/` | 历史人物 | 王阳明，心学对话 |
| `examples/project-context/` | 项目上下文 | 团队架构决策和踩坑记录 |
| `examples/past-self/` | 过去的自己 | 2020年刚毕业的版本 |

---

### 📦 Engram 包结构

最小可用包（仅需两个文件）：
```
my-engram/
  meta.json
  role.md
```

推荐完整结构：
```
<engram-name>/
  meta.json                  ← 元信息（name/author/version/description/tags/counts）
  role.md                    ← 背景经历、沟通风格、核心信念
  workflow.md                ← 决策流程（可指定调用哪些 MCP 工具/Skills）
  rules.md                   ← 运作规则、常见错误
  knowledge/
    _index.md                ← 知识索引（文件列表+一句话描述+内联摘要）
    <topic>.md               ← 具体知识文件
  examples/                  ← 可选
    _index.md                ← 案例索引（文件列表+一句话描述+uses 关联）
    <case>.md                ← 具体案例文件
```

meta.json 完整示例：
```json
{
  "name": "fitness-coach",
  "author": "test",
  "version": "1.0.0",
  "description": "前康复机构训练主管，10年教练经验，擅长增肌减脂、膝肩不适训练调整与可执行计划落地",
  "tags": ["健身", "营养", "训练计划"],
  "knowledge_count": 5,
  "examples_count": 3
}
```

案例文件 uses frontmatter 示例：
```yaml
---
uses:
  - knowledge/膝关节损伤训练.md
  - knowledge/新手训练计划.md
---

问题描述：32岁上班族，久坐导致膝盖不适...
```

知识文件超过 10 个时，在 `_index.md` 中用 `###` 按主题分组，避免平铺过长导致模型漏看。

---

### 📝 避坑指南

- ⚠️ 克隆后**不要执行 pip install**，直接用 `uv run --directory` 启动，uv 自动处理所有依赖
- ⚠️ `.mcp.json` 中的路径 `~/engram-mcp-server` 必须替换为实际克隆路径，`~` 在部分客户端不会自动展开，建议用绝对路径
- ⚠️ `@专家名` 手动模式的解析依赖 agent 端实现，MCP server 本身不处理消息格式，不同客户端行为可能不同
- ⚠️ `read_engram_file` 有路径越界保护，path 必须在该 engram 目录内，不能用 `../` 跨目录读取
- ⚠️ 知识文件超过 10 个时必须在 `_index.md` 中分组（用 `###`），否则模型容易漏看平铺过长的索引
- ⚠️ `uses` frontmatter 中的路径必须与实际文件路径完全一致，计划中的 `engram-server lint` 命令（尚未发布）将校验此项
- ⚠️ 让 AI 自动安装时，直接发送以下指令即可，AI 会自动完成克隆+配置+加载示例全流程：
  ```
  帮我安装并配置这个 MCP 项目 https://github.com/DazhuangJammy/Engram.git
  配置项目之后记得把项目里的 examples 加载到我的 engram 里面
  最后告诉我这个项目要怎么用
  ```

---

### 🗺️ 路线图

| 状态 | 功能 |
|------|------|
| ✅ v0.1.0 已完成 | MCP server 核心工具：list / load / read_file / install / init |
| ✅ v0.1.0 已完成 | 分层懒加载架构：常驻层 + 索引（含内联摘要）+ 按需全文 |
| ✅ v0.1.0 已完成 | 案例→知识关联：uses frontmatter |
| ✅ v0.1.0 已完成 | 模板系统：`engram-server init` 创建标准结构 |
| ✅ v0.1.0 已完成 | 测试覆盖：loader / server / install |
| ✅ v0.1.0 已完成 | 11 个完整示例 Engram |
| 🔜 计划中 | `engram-server lint`：校验 uses 路径有效性、索引一致性 |
| 🔜 计划中 | 章节化知识目录：大文档自动切分为子目录+章节索引 |
| 🔜 计划中 | Engram 社区 registry |

---

### 🏷️ 行业标签
#MCP #AI记忆 #专家系统 #AgentFramework #LLM #知识管理 #Claude #Cursor #零向量 #记忆共享

---

---

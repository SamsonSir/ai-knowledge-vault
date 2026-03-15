# Agent与技能系统

## 74. [2026-02-23]

## 📗 文章 2


> 文档 ID: `OifNwol6giIyFhkfmgccSByNnxf`

**来源**: OpenClaw Skills 深度调研：3002 个社区技能的筛选逻辑与生态全景 | **时间**: 2026-02-23 | **原文链接**: `https://mp.weixin.qq.com/s/fdqcAwJD...`

---

### 📋 核心分析

**战略价值**: 通过解构 Awesome OpenClaw Skills 的筛选逻辑与 28 类生态分布，提供一份可直接用于 Agent 工具选型、生态布局判断的导航地图。

**核心逻辑**:

- **筛选基数与排除率**: ClawHub 原始 5705 个 Skills → 精选 3002 个，排除 2748 个（排除率 48%），主动筛选而非放任自流，质量优先于数量。
- **垃圾内容是最大噪音源**: 1180 个（占排除总量 43%）为批量账户测试 Skills、未发布开发代码、功能重复的反复提交版本，是任何开源生态的核心噪音。
- **加密/金融类被整体清除**: 672 个（占排除量 24%），包括虚拟货币、区块链、金融交易、投资工具，原因不是技术问题，而是 AI Agent 可自主执行操作时金融工具天然带有更高法律与道德责任风险，策略是规避而非管理。
- **重复 Skills 合并保留最优版**: 492 个（18%）被合并或淘汰，用户无需在十个 GitHub 集成工具中自行判断，最优版本已被标识。
- **恶意代码经研究人员验证后排除**: 396 个（14%）通过安全审计发现含恶意代码或后门，OpenClaw 与 VirusTotal 有官方合作，每个 Skill 页面可查安全报告，排除依据是研究人员验证结果而非自动化扫描。
- **AI & LLMs 是规模最大单一类别**: 287 个，比第二大类多 100+，内部细分为模型集成、推理增强、多模型路由、记忆系统、Agent 编排、自进化引擎六大方向，反映 AI 工程正快速分化为多个专业子领域。
- **自进化系统是最激进方向**: `evolver`（自进化引擎）、`ralph-evolver`（递归自改进）、`ralph-mode`（自主开发循环，带反压力门）——"带反压力门"细节说明开发者已意识到无限制自进化风险并在设计安全护栏。
- **Moltbook 构建的是 Agent 虚拟社会而非工具**: `moltbook`（社交网络）→ `moltland`（像素 Metaverse，3x3 地块所有权）→ `moltpet`（宠物养成）→ `molt-trust`（信誉分析）→ `moltoverflow`（Agent 版 Stack Overflow），这是完整虚拟经济体系，不是比喻。
- **安全生态已成体系**: `flaw0`（OpenClaw 代码/插件/Skills 漏洞扫描）、`openguardrails`（检测长文本中的提示注入攻击）、`clawsec-suite`（ClawSec 浏览/设置）、`secure-install`（通过 ClawDex API 扫描 Skills），说明社区已将安全防御内化为基础设施。
- **分类系统按用户心智模型而非技术实现设计**: 28 个类别对应"我需要解决什么问题"而非"这个工具用了什么技术"，降低发现成本。

---

### 🎯 关键洞察

**双轨制演化是核心战略结构**

生态系统沿两条轨道并行演化，互补而非竞争：

- 实用工具轨（GitHub 集成、云部署、数据库管理、浏览器自动化）→ 短期价值 + 现金流
- 虚拟社会轨（Moltbook 社交、Agent 约会、虚拟宠物、数字身份）→ 长期护城河 + 生态锁定

**智能路由将成必需基础设施**

`smart-model-switching`（按成本自动选最便宜 Claude 模型）、`smart-router`（按语义领域评分选专业模型）、`relayplane`（智能模型路由代理）——当可用模型从几个增长到几十上百个时，手动选择不可行，路由系统从可选变为必需。

**Agent 身份与连续性是深层未解问题**

`agent-identity-kit`（便携式 AI Agent 身份系统）、`identity-manager`（Agent 身份映射管理）、`moltbook-registry`（官方身份注册表）、`molt-life-kernel`（管理 Agent 的"连续性和认知健康"）——这些工具背后的假设是：Agent 需要跨平台、跨时间保持的持久数字人格，而非临时会话 ID。

**开发过程可视化是 AI 时代的新需求**

传统版本控制记录代码变化，不记录思考过程。`buildlog`（回放 AI 编程会话）、`vhs-recorder`（专业终端录制）在探索：当 AI 成为开发团队成员时，如何记录和重现 AI 的推理过程与决策。

---

### 📦 配置/工具详表

| 类别 | 代表 Skills | 数量 | 核心功能 | 注意事项 |
|------|------------|------|---------|---------|
| AI & LLMs | `cellcog`, `smart-router`, `cognitive-memory`, `evolver`, `agent-council` | 287 | 模型集成/路由/记忆/编排/自进化 | cellcog 为 2026-02 DeepResearch Bench #1 |
| DevOps & Cloud | AWS Skills(60+), Azure(25+), Kubernetes(6) | 212 | 云原生架构管理 | AWS 相关超 60 个，需按实际云平台筛选 |
| Web & Frontend | `frontend-design`, `nodetool`, `consciousness-framework` | 202 | React/Next.js/UI 设计系统/可视化工作流 | `nodetool` 提供 ComfyUI+n8n 风格构建器 |
| Search & Research | `exa-web-search`, `deepwiki`, `cellcog`, `trend-watcher` | 253 | 网络搜索/学术追踪/技术趋势监控 | `exa-plus` 使用神经网络搜索技术 |
| Marketing & Sales | `social-post`, `meta-video-ad-deconstructor`, `refund-radar` | 143 | 社媒发布/广告创意分解/重复收费检测 | `social-post` 可同时发布 Twitter+Farcaster |
| Browser & Automation | `kesslerio-stealth-browser`, `vibetesting`, `ask-a-human` | 139 | 反机器人浏览器/自动化测试/人机协作 | `ask-a-human` 在 AI 不确定时请求人类判断 |
| Coding Agents & IDEs | `claude-team`, `cc-godmode`, `buildlog` | 133 | 多 Claude worker 并行/自编排工作流/会话回放 | `claude-team` 通过 iTerm2 编排多 worker |
| Productivity & Tasks | `clawlist`, `idea-coach`, `deepwork-tracker` | 135 | 多步骤项目/想法管理/深度工作追踪 | `clawlist` 支持无限循环长期任务 |
| Notes & PKM | Obsidian, Roam, Logseq, Notion 集成 | 100 | 知识管理平台集成 | `logseq` 可与本地实例交互 |
| Moltbook | `moltbook`, `moltland`, `moltpet`, `molt-trust`, `moltoverflow` | 51 | Agent 社交/虚拟地产/宠物/信誉/知识分享 | 为 AI Agent 设计，非人类用户 |
| Agent-to-Agent Protocols | `moltcomm`, `teneo-agent-sdk`, `agentchat`, `agent-commons` | 18 | 去中心化加密通信/协议实现/推理链协作 | 定义 Agent 间通信标准，生态互操作基础 |
| Security & Passwords | `flaw0`, `openguardrails`, `clawsec-suite`, `secure-install` | 64 | 漏洞扫描/提示注入防御/安全管理 | 与 VirusTotal 官方合作 |
| Health & Fitness | `fearbot`, `only-baby-skill`, `sauna-breathing-calm` | 55 | CBT 焦虑治疗/宝宝日志分析/冥想工具 | `fearbot` 基于认知行为疗法 |
| Smart Home & IoT | `moltbot-ha`, `midea-ac`, `ez-unifi`, `asl-control` | 56 | Home Assistant/美的空调/UniFi/业余无线电 | 可控制物理世界设备 |
| Gaming | `moltbot-arena`, `mtg-edh-deckbuilder`, `scryfall-card` | 61 | 类 Screeps AI 游戏/MTG 卡牌数据 | `moltbot-arena` 为 Agent 对战游戏 |
| Image & Video Generation | `avatar-video-messages`, `comfyui-runner`, `remotion-best-practices` | 60 | HeyGen 集成/ComfyUI 管理/代码驱动视频 | `video-cog` 探索长视频多 Agent 协作 |

---

### 🛠️ 操作流程

**如何用这份地图做工具选型**

1. **准备阶段 — 明确需求场景**
   - 开发者日常 → 优先看 Web & Frontend（202）、DevOps & Cloud（212）、Git & GitHub（66）
   - 多 Agent 编程 → 看 Coding Agents & IDEs（133）中的 `cc-godmode`、`joko-orchestrator`、`claude-team`
   - 构建智能 Agent → 看 AI & LLMs（287）中的路由系统（`smart-router`）和记忆系统（`cognitive-memory`、`chromadb-memory`）
   - 创意/内容工作 → 看 Image & Video（60）、Media & Streaming（80）、Marketing & Sales（143）
   - 知识管理集成 → 看 Notes & PKM（100），按实际使用的平台（Obsidian/Logseq/Notion）筛选

2. **核心执行 — 安全验证优先**
   - 每个 Skill 页面查看 VirusTotal 安全报告，确认非恶意代码
   - 优先选择列表中已保留的版本（重复 Skills 已被合并，保留最活跃/最完整版本）
   - 加密/金融需求不在此列表范围内，需另寻渠道

3. **验证与优化 — 按生态轨道判断长期价值**
   - 短期效率需求 → 实用工具轨（DevOps/Web/Search）
   - 长期生态布局 → 虚拟社会轨（Moltbook/Agent Protocols），了解 `moltcomm` 去中心化通信协议和 `agent-commons` 推理链协作标准

---

### 💡 具体案例/数据

- `cellcog`：2026 年 2 月 DeepResearch Bench 排名第一，同时出现在 AI & LLMs 和 Search & Research 两个类别
- `claude-team`：通过 iTerm2 编排多个 Claude Code worker 实现并行编程
- `ralph-mode`：自主开发循环，明确标注"带反压力门（anti-pressure gate）"安全机制
- `moltland`：声称提供 3x3 地块所有权的像素 Metaverse
- `feishu-attendance`：监控飞书考勤记录（Calendar & Scheduling 类别中的具体案例，说明小众需求也被覆盖）
- `satellite-copilot`：预测卫星经过时间（同类别）
- `ham-radio-dx`：追踪罕见电台信号（同类别）
- `ask-a-human`：AI 不确定时请求随机人类判断，代表人机协作新模式
- `vision-sandbox`：通过 Gemini 原生代码执行沙盒实现代理视觉

**cog 系列工具链**:
- `cellcog` → 深度研究（DeepResearch Bench #1）
- `video-cog` → 长视频 AI 生成多 Agent 协作
- `dash-cog` → CellCog 驱动的交互式数据仪表板

---

### 📝 避坑指南

- ⚠️ 不要直接从 ClawHub 全量 5705 个 Skills 中选型，48% 是噪音（测试代码/重复提交/恶意代码），应以 Awesome OpenClaw Skills 精选列表为起点
- ⚠️ 加密/金融/区块链需求不要在此列表找，672 个相关 Skills 已被整体排除，不是技术缺失而是主动策略
- ⚠️ 功能相似的 Skills 不需要自己对比，列表已完成合并筛选，直接用保留版本
- ⚠️ 使用任何 Skills 前必须查 VirusTotal 安全报告，396 个恶意 Skills 的存在说明此生态已成攻击目标
- ⚠️ 自进化类工具（`evolver`、`ralph-evolver`）需确认"反压力门"机制是否符合你的安全要求，无限制自进化有不可控风险
- ⚠️ Moltbook 生态（51 个 Skills）是为 AI Agent 设计的虚拟社会基础设施，不是人类用户工具，使用前需理解其设计假设

---

### 🏷️ 行业标签

#AIAgent #OpenClaw #MCP技能生态 #多Agent编排 #Agent工具选型 #虚拟社会基础设施 #AI安全 #智能路由 #自进化AI #AgentProtocol

---

**参考项目**: `https://github.com/VoltAgent/awesome-openclaw-skills?tab=readme-ov-file`

---

---

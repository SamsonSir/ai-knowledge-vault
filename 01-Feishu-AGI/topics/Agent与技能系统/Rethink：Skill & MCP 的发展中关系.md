# Agent与技能系统

## 14. [2026-01-20]

## 📕 文章 1


> 文档 ID: `BnxnwqT7jiTTxikvh4zcSUpEnsb`

**来源**: Rethink：Skill & MCP 的发展中关系 | **时间**: 2026-01-20 | **原文链接**: `https://mp.weixin.qq.com/s/RMfzAttl...`

---

### 📋 核心分析

**战略价值**: MCP 的 Resources/Prompts 接口是连接 Skill 与 MCP 的关键桥梁，两者融合后可实现「知识 + 能力」一体化分发，是 Agent 生态的下一个演进方向。

**核心逻辑**:

- **MCP 协议有三类接口，但 90% 的人只用了一个**：`tools`（工具调用）被广泛使用，`resources`（资源访问）和 `prompts`（提示模板）几乎被完全忽视，而后两者恰恰是融合 Skill 的关键入口。

- **Skill 的本质是「上下文包」，不是脚本**：结构为 `SKILL.md`（核心知识）+ `scripts/`（可选脚本）+ `references/`（参考文档）+ `assets/`（模板资源），核心价值是传递「领域知识、工作流程、工具用法、质量标准、边界条件」。

- **MCP 的本质是「能力扩展协议」**：提供 Tools（可调用操作）、Resources（可读取资源）、Prompts（可复用模板），核心价值是让 Agent 能做原本做不了的事。

- **一句话区分**：Skill 教 Agent「怎么做」（知识传递，静态文档）；MCP 让 Agent「能做什么」（能力扩展，动态服务）。

- **边界模糊的根本原因**：很多 Skill 本质上是在教 Agent 使用特定工具（如 pdf-skill 就是 pdf-mcp 的使用指南），工具提供商天然是对应 Skill 的最佳作者，因此 Tool + Skill 同源分发极为合理。

- **Skill 中的脚本（如 `recalc.py`）本质上就是 MCP Tools**，只是以文件形式分发而非服务形式，封装进 MCP Server 后可获得统一调用接口、环境依赖封装、版本管理三大收益。

- **融合的技术路径已经存在**：通过 MCP 的 `registerResource` 接口，一个 Server 可以同时暴露 Tools 和 Skill 内容，Agent 既能调用 `extract_pdf_text` 执行操作，又能读取 `skill://pdf-guide` 获取使用指南。

- **两种分发范式各有定位**：文件分发（Skill 模式）零门槛、去中心化、离线可用，但碎片化、无自动更新；服务分发（MCP 模式）中心化管理、可自动更新、可计量，但需要开发能力和运维成本。

- **上下文的传递形式不重要，内容才重要**：SKILL.md（静态一次性加载）、MCP Resource（动态按需加载）、MCP Prompt（结构化可参数化）、System Prompt（全局始终生效）四种方式本质等价，Skill 文件格式的价值仅在于降低非开发者的创作门槛。

- **终极演进方向**：每个 MCP Server = Tools + Resources + Skills，Agent 通过统一 MCP 协议同时获取能力和知识，独立 Skill 格式作为轻量级创作入口保留。

---

### 🎯 关键洞察

**为什么 Tool 提供商应该自带 Skill？**

逻辑链：谁最懂 Notion API → Notion 团队 → 他们写的 Skill 质量最高 → Tool + Skill 同源分发是最优解。

标准仓库结构应为：
```
notion-mcp/
├── server.ts         # MCP Server: 提供 Tools
├── SKILL.md          # Skill: 教 Agent 如何用好这些 Tools
└── references/       # 进阶用法文档
```

**为什么 Resources/Prompts 接口是关键？**

当前 MCP 生态几乎只用 Tools，但 Resources 接口天然适合承载 Skill 内容（Markdown 文档、配置模板等），Prompts 接口天然适合承载结构化的任务模板。这两个接口被激活后，MCP Server 就从「工具箱」升级为「工具箱 + 使用手册」。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| MCP 三类接口声明 | `interface MCPCapabilities { tools: Tool[]; resources: Resource[]; prompts: Prompt[]; }` | 完整能力暴露 | 当前生态 resources/prompts 几乎无人用 |
| Skill 目录结构 | `SKILL.md` + `scripts/` + `references/` + `assets/` | Agent 获取完整上下文 | SKILL.md 是唯一必须项 |
| MCP 暴露 Tool | `server.registerTool({ name, description, handler })` | Agent 可调用操作 | handler 需处理异步和错误 |
| MCP 暴露 Skill 为 Resource | `server.registerResource({ uri: "skill://pdf-guide", mimeType: "text/markdown", handler: async () => ({ text: fs.readFileSync("SKILL.md","utf-8") }) })` | Tool + Skill 同一 Server 共存 | uri 用 `skill://` 前缀做语义区分 |
| 文件分发范式 | 写 SKILL.md → 发 GitHub/压缩包 → 消费者放入 `.claude/skills/` | 零门槛分享知识 | 无自动更新，资源文件需手动管理 |
| 服务分发范式 | 写 MCP Server → 发布 npm → 消费者 `npm install` + 配置连接 | 中心化管理、可自动更新 | 需要开发能力，远程 Server 有运维成本 |

---

### 🛠️ 操作流程

**场景：将现有 Skill 升级为 MCP Server（Tool + Skill 融合分发）**

1. **准备阶段**:
   - 确认现有 Skill 目录结构：`SKILL.md` + 可选 `scripts/*.py`
   - 识别 `scripts/` 中哪些脚本可以封装为 MCP Tools（如 `recalc.py` → `recalculate_excel` tool）
   - 确认运行环境依赖（Node.js/Python 版本、第三方库）

2. **核心执行**:
   - 创建 `server.ts`，初始化 `MCPServer` 实例
   - 用 `server.registerTool()` 封装原有脚本逻辑
   - 用 `server.registerResource()` 暴露 `SKILL.md`，uri 格式建议 `skill://{skill-name}-guide`，mimeType 设为 `text/markdown`
   - 用 `server.registerPrompt()` 暴露常用任务模板（可选）
   - 发布到 npm：`npm publish`

3. **验证与优化**:
   - 消费者侧：`npm install {your-mcp-server}`，配置 MCP 连接
   - 验证 Agent 能同时调用 Tool 和读取 Resource
   - 在 `SKILL.md` 中明确声明依赖的其他 MCP Server，方便消费者配置完整环境

---

### 💡 具体案例/数据

**案例 1：pdf-skill 与假想 pdf-mcp 的关系**

现有 pdf-skill 的 `SKILL.md` 内容：
```markdown
# PDF Processing Guide
## Python Libraries
### pypdf - Basic Operations
### pdfplumber - Text and Table Extraction
### reportlab - Create PDFs
## Common Tasks
- Extract Text from Scanned PDFs (OCR)
- Add Watermark
- Password Protection
```
如果存在 `pdf-mcp` Server 提供 `extract_text`、`merge_pdfs`、`add_watermark` 等 Tools，则上述 Skill 本质上就是该 Server 的使用指南，两者应合并为同一仓库分发。

**案例 2：xlsx-skill 中脚本的 MCP 化**
```
xlsx-skill/
├── SKILL.md
└── scripts/
    └── recalc.py     # 当前：需要消费者本地有 Python 环境
```
封装为 MCP Tool 后：消费者无需关心 Python 环境，调用 `recalculate` tool 即可，环境依赖由 Server 端封装。

---

### 📝 避坑指南

- ⚠️ **不要只暴露 Tools**：MCP Server 只有 Tools 等于只给了锤子没给说明书，Agent 在复杂任务中容易用错工具或遗漏最佳实践。
- ⚠️ **Skill 内容质量 > 分发形式**：无论用 SKILL.md 还是 MCP Resource 分发，低质量的上下文内容都无法提升 Agent 表现，形式不能弥补内容的缺失。
- ⚠️ **远程 MCP Server 有运维成本**：选择服务分发范式前需评估是否有能力维护服务可用性，本地 MCP Server（npm install 后本地运行）可规避网络依赖问题。
- ⚠️ **Skill 中要明确声明 MCP 依赖**：如果 Skill 依赖特定 MCP Server，必须在 `SKILL.md` 中显式说明，否则消费者环境不完整会导致 Agent 行为异常。
- ⚠️ **resources/prompts 接口当前生态支持度低**：在 Agent 框架侧验证是否支持读取 MCP Resources，不同框架的实现完整度差异较大。

---

### 🏷️ 行业标签

#MCP #AgentSkill #Claude #AI工程 #上下文工程 #工具分发 #Agent架构

---

---

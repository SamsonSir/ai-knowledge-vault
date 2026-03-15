# Agent与技能系统

## 20. [2026-01-22]

## 📙 文章 4


> 文档 ID: `Anw7wqqtjim6BxkmeZiczkV2n4g`

**来源**: Day 2 教你用：Listenhub API 混搭大模型 API 手搓一个好用的 Skills | **时间**: 2026-01-22 | **原文链接**: 无

---

### 📋 核心分析

**战略价值**: 通过 `.claude/skills/` 目录结构 + SKILL.md 文件，将重复性 Prompt 固化为可自动触发的"专家模块"，配合 Listenhub API 实现音频/播客生成能力的一键复用。

**核心逻辑**:

- **Skills 本质是文件级 Prompt 固化**：不是插件、不是云端配置，就是本地 `.claude/skills/<name>/SKILL.md`，Claude Code 启动时自动加载，对话中按 description 语义匹配自动触发。
- **触发机制依赖 description 字段**：Claude 通过 description 判断"什么时候用这个 Skill"，描述越具体触发越精准。模糊描述（如 "A helper for coding"）= 永远不会被调用。
- **目录结构必须严格遵守**：路径错一层就失效。必须是 `项目根目录/.claude/skills/<技能名>/SKILL.md`，SKILL.md 必须全大写。
- **skill-creator 是官方元 Skill**：用一个 Skill 来生成 Skill，通过 `npx skills add https://github.com/anthropics/skills --skill skill-creator` 安装后，直接在对话中描述需求，它会交互式引导生成完整 SKILL.md。
- **Listenhub Skills 安装命令**：`npx skills add marswaveai/skills`（推荐）或 `bunx add-skill marswaveai/skills`，安装后可调用 Listenhub API 生成音频、图片、播客、解说视频。
- **模块化拆分是质量关键**：一个 Skill 只做一件事。"翻译"、"润色"、"格式化"分三个 Skill，混在一起 Claude 会混淆指令。
- **Skills 可与 MCP 工具链结合**：在 SKILL.md 里写 `请先使用 'file-search' 工具查找相关文档，然后再回答问题`，即可把工具调用逻辑固化进 Skill 流程。
- **Skills 天然支持团队共享**：把 `.claude/skills/` 文件夹提交到 Git 仓库，团队成员 pull 后立即拥有相同技能集，无需任何额外配置。
- **迭代方式**：生成后立即测试，不完善就再次调用 skill-creator 补充说明，支持持续迭代。
- **运行环境要求**：Claude Code 或 OpenCode，或支持文件配置的客户端；需要可正常访问的网络。

---

### 🎯 关键洞察

**为什么 description 是核心**：Claude 在对话中不会主动扫描所有 Skill 内容，它只读 description 来决定是否激

---

---

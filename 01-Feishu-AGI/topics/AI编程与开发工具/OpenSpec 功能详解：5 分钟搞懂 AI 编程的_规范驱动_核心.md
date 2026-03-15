# AI编程与开发工具

## 10. [2026-01-19]

## 📗 文章 2


> 文档 ID: `DPDSwXr2qiDYttkSfsPcxU2pnVg`

**来源**: OpenSpec 功能详解：5 分钟搞懂 AI 编程的"规范驱动"核心 | **时间**: 2026-01-18 | **原文链接**: `https://mp.weixin.qq.com/s/wyUdxh2T...`

---

### 📋 核心分析

**战略价值**: OpenSpec 通过"规范注入"机制，让 AI 在每次对话前先加载项目规范，从而稳定、可复现地驱动 AI 按团队标准执行开发任务。

**核心逻辑**:

- **触发机制是根本**：AI 不触发 OpenSpec 规范，99% 是因为请求中缺少关键词（"提案"、"变更"、"规范"、"计划"等），AI 不会主动加载规范文件，必须显式触发。
- **安装只需两步**：`npm install -g @fission-ai/openspec@latest` 全局安装，然后在项目目录执行 `openspec init`，初始化时选择对应 AI 工具（Claude Code / Cursor / Trae / Qoder / Other Tools）。
- **Claude Code 初始化后自动生成 `.claude/` 目录**，包含三个斜杠命令文件（`apply.md`、`archive.md`、`proposal.md`）和两个根文件（`AGENTS.md`、`CLAUDE.md`），Claude Code 启动时自动读取 `AGENTS.md`，无需手动配置。
- **Trae 老版本需手动配置**：Trae 在 OpenSpec 初始化选项中不直接支持，需选 "Other Tools"，生成 `AGENT.md` + `openspec/` 目录结构，老版本 Trae 不自动读取 `AGENT.md`，必须手动将其内容粘贴到 Trae「项目规则」设置中；2026 年 1 月新版 Trae 已原生支持自动读取 `AGENT.md`。
- **三阶段工作流不可跳步**：Proposal（创建变更提案）→ Apply（实现变更）→ Archive（归档变更），每个阶段对应一个命令文件，AI 按文件中的 Prompt 规范执行。
- **提案触发有明确边界**：新增功能、破坏性变更（API/Schema）、架构调整 → 必须创建提案；Bug 修复（恢复既有行为）、拼写/格式/注释修正、非破坏性依赖升级 → 直接跳过提案。
- **知识分三层存放**：通用开发规范放 `/AGENTS.md`（每次对话自动加载）；OpenSpec 工作流放 `openspec/AGENTS.md`（关键词触发后加载）；业务上下文放 `openspec/project.md`（通过规范索引间接加载）。
- **`openspec/project.md` 是项目知识库**，存放项目目标与背景、核心业务术语、技术栈说明、详细文档索引，但只有触发 OpenSpec 规范后才会被读取，日常对话不会自动加载。
- **规范文件可直接修改**：初始化生成的所有 `.md` 文件均可手动编辑，直接变更规范内容，使其适配企业内部业务流程，无需重新初始化。
- **斜杠命令是最稳定的触发方式**：在支持的工具中，`/openspec:proposal` 直接触发提案流程，比依赖关键词匹配更可靠。

---

### 🎯 关键洞察

**为什么"时灵时不灵"的根本原因**：

OpenSpec 的触发逻辑是关键词匹配，不是语义理解。AI 读取 `AGENTS.md` 后，判断请求是否包含"提案/规范/变更/计划/架构"等词，命中才加载 `openspec/AGENTS.md` 详细规范。如果你说"帮我加个登录功能"，AI 不会触发；如果你说"帮我创建一个新功能的变更提案"，AI 才会触发。

**设计权衡的代价**：`project.md` 中的业务知识不会在日常对话中自动生效，这是为了避免每次对话都加载大量上下文导致性能下降。解法是在 `/AGENTS.md` 中建立业务知识索引，或在对话中明确指定 `先阅读 openspec/project.md 再回答`。

---

### 📦 配置/工具详表

| 工具 | 初始化选项 | 自动加载规范 | 关键目录/文件 | 特殊操作 |
|------|-----------|------------|-------------|---------|
| Claude Code | 直接选择 | ✅ 自动读取 `.claude/AGENTS.md` | `.claude/commands/openspec/`、`AGENTS.md`、`CLAUDE.md` | 无需额外配置 |
| Cursor | 直接选择 | 视版本而定 | 对应 Cursor 规范目录 | 参考工具文档 |
| Trae（新版 2026-01）| 选 Other Tools | ✅ 自动读取 `AGENT.md` | `AGENT.md`、`openspec/` | 升级到最新版 |
| Trae（老版本）| 选 Other Tools | ❌ 不自动读取 | `AGENT.md`、`openspec/` | 手动粘贴到「项目规则」 |
| Other Tools / VSCode | 选 Other Tools | ❌ 需手动配置 | `AGENT.md`、`openspec/` | 手动配置规则入口 |

---

### 🛠️ 操作流程

**1. 准备阶段**

```bash
# 全局安装
npm install -g @fission-ai/openspec@latest

# 进入项目目录并初始化
cd /path/to/your-project
openspec init
# 初始化时选择你使用的 AI 工具
# Trae 用户选 "Other Tools"
```

**2. 核心执行（以 Claude Code 为例）**

```
# 触发提案（方式一：斜杠命令）
/openspec:proposal

# 触发提案（方式二：关键词）
"帮我为新增用户权限功能创建一个变更提案"

# 实现变更
/openspec:apply

# 归档变更
/openspec:archive
```

**3. Trae 老版本手动配置步骤**

1. 打开 Trae → 项目设置 → 找到「项目规则」
2. 打开 `AGENT.md`，复制全部内容
3. 粘贴到「项目规则」输入框
4. 保存，之后每次对话自动加载

**4. 常用 CLI 命令**

```bash
openspec list              # 列出所有变更
openspec list --specs      # 列出所有规范
openspec validate <id>     # 校验变更
openspec archive <id>      # 归档变更
```

**5. 验证与优化**

- 在 `/AGENTS.md` 中补充业务知识索引，确保日常对话也能间接触发业务上下文
- 直接编辑 `openspec/project.md` 填入项目目标、业务术语、技术栈
- 按需修改 `proposal.md`、`apply.md`、`archive.md` 中的 Prompt，适配团队流程

---

### 💡 具体案例/数据

**`AGENTS.md` 核心内容（Claude Code 自动生成）**：

```markdown
<!-- OPENSPEC:START -->
# OpenSpec 说明
这些指令是针对参与本项目的人工智能助手。
当请求中包含以下内容时，请务必打开 `@/openspec/AGENTS.md`：
- 提及规划或提案（如提案、规范、变更、计划等字眼）
- 引入新功能、重大变更、架构调整或重大的性能/安全工作
- 听起来含糊不清，且在编码前需要权威规范
使用 `@/openspec/AGENTS.md` 来学习：
- 如何创建和应用变更提案
- 规范格式和约定
- 项目结构和指南
保留此托管块，以便"openspec update"可以刷新指令。
<!-- OPENSPEC:END -->
```

**提案触发判断表**：

| 场景 | 是否需要提案 |
|------|------------|
| 新增功能或能力 | ✅ 必须 |
| 破坏性变更（API/Schema） | ✅ 必须 |
| 架构或模式调整 | ✅ 必须 |
| Bug 修复（恢复既有行为） | ❌ 跳过 |
| 拼写、格式、注释修正 | ❌ 跳过 |
| 非破坏性依赖升级 | ❌ 跳过 |

---

### 📝 避坑指南

- ⚠️ **Trae 老版本不自动读取 `AGENT.md`**：必须手动粘贴到「项目规则」，否则 OpenSpec 规范完全不生效，AI 不会按规范工作。
- ⚠️ **`project.md` 日常对话不生效**：业务知识只在触发 OpenSpec 规范后才加载，不要把关键业务上下文只放在 `project.md` 里，需在 `/AGENTS.md` 中建立索引。
- ⚠️ **关键词不够精确导致不触发**：说"加个功能"不触发，说"创建变更提案"才触发。最稳定的方式是用斜杠命令 `/openspec:proposal`。
- ⚠️ **不要跳过 Archive 步骤**：已完成的变更不归档会导致 `openspec list` 输出混乱，AI 可能重复处理已完成的提案。
- ⚠️ **初始化生成的 `.md` 文件可以改**：这些文件不是只读的，企业可以直接修改 Prompt 内容来定制规范，不需要等官方更新。

---

### 🏷️ 行业标签

#OpenSpec #规范驱动开发 #AI编程 #ClaudeCode #Trae #提案工作流 #团队协作 #LLM工程化

---

---

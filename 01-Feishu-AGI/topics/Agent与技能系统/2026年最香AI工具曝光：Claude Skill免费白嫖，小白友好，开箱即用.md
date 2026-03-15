# Agent与技能系统

## 6. [2026-01-12]

## 📘 文章 3


> 文档 ID: `ZK5FwqYoTiA72Pk3kt0ciq4anje`

**来源**: 2026年最香AI工具曝光：Claude Skill免费白嫖，小白友好，开箱即用 | **时间**: 2026-01-12 | **原文链接**: `https://mp.weixin.qq.com/s/AQd9RV43...`

---

### 📋 核心分析

**战略价值**: OpenCode + Oh-My-Opencode + Claude Skills 三件套，提供免费、开箱即用的 AI 编程 Agent 环境，无需注册账号、无需信用卡，让普通人以零成本复用顶尖工作流。

**核心逻辑**:

- **OpenCode 是 Claude Code 的免费平替**：官网 `https://opencode.ai/`，支持 Mac/Windows/Linux，有 CLI 和客户端两种形式，推荐 CLI（客户端 Bug 较多）。
- **安装一条命令搞定**：`curl -fsSL https://opencode.ai/install | bash`，安装后输入 `opencode` 回车即进入界面。
- **内置 75+ 模型供应商**：输入 `/model` 查看免费模型（如 GLM-4.7）；输入 `/connect` 可授权接入已订阅的 OpenAI（Codex）或 Google（Gemini）账号；还支持 Mistral、OpenRouter、Groq、本地 Ollama 模型。
- **推荐免费主力模型 GLM-4.7 的理由**：SWE-Bench 得分 73.8%（解决真实 GitHub 开源 Python 问题，第一梯队）；HumanEval Python 编程得分 94.2%；IFEval 指令遵循 88%；GSM8k 多步推理 98%。代码生成、指令遵循、前端审美均强，且对 Agentic Coding 场景做了专项强化。
- **Oh-My-Opencode（OMO）是核心增强框架**：作者耗费 2.4 万美元 Token 打造的 Agent 编程框架，安装方式极简——直接对 OpenCode 说"帮我安装 oh-my-opencode 插件"，GLM-4.7 会自动搜索并执行安装。后续补充订阅可运行 `opencode auth login`。
- **OMO 内置多角色 Agent 编排**：主控 Agent Sisyphus（西西弗斯）由高智商模型（如 Opus 4.5 High）扮演，统筹调度子 Agent：Oracle（架构/调试，GPT 5.2 Medium）、Frontend UI/UX Engineer（前端设计，Gemini 3 Pro）、Librarian（文档/代码库查阅，Claude Sonnet 4.5）、Explore（极速代码库扫描，Grok Code）。
- **OMO 内置三大常用 MCP**：Exa（联网搜索）、Context7（官方文档查询）、Grep.app（GitHub 全库代码搜索）。
- **OMO 实现与 Claude Code 完全兼容**：同样支持 Command、Agent、Skill、MCP、Hook 技术方案，这是在 OpenCode 中玩 Skill 的关键前提。
- **Skill 安装极简**：直接对 OpenCode 说"安装这里的 skills `https://github.com/kepano/obsidian-skills`"，GLM-4.7 自动下载安装；用 `/` 斜杠可显式精准调用已安装 Skill；新安装或新写的 Skill 需 Ctrl+C 退出重进才能生效。
- **Skill 创建建议先装元 Skill**：使用 Anthropic 官方 skill-creator（`https://github.com/anthropics/skills/tree/main/skills/skill-creator`）来生成 Skill，最简单的 Skill 只需一段提示词；复杂 Skill 可包含脚本、MCP 

---

---

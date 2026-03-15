# AI产品与商业化

## 24. [2026-03-05]

## 📕 文章 1


> 文档 ID: `LeoIw1sOmimgy0ksVqDcqxf3nDc`

**来源**: GPT-5.4深夜发布，最适合OpenClaw的天选模型登场了 | **时间**: 2026-03-06 | **原文链接**: `https://mp.weixin.qq.com/s?__biz=Mz...`

---

### 📋 核心分析

**战略价值**: GPT-5.4 首次将 Codex 级代码能力与强世界知识合并进同一主线模型，且可直接走 ChatGPT/Codex 订阅额度，成为 OpenClaw 默认基座模型的最优解。

**核心逻辑**:

- **Agent 基座模型的三要素**：代码能力 + 世界知识 + 多模态理解，三者缺一则 Agent 能力出现明显短板。GPT-5.3-Codex 代码强但世界知识差，说"天书"；Claude Opus 4.6 均衡但 API 极贵且封 OpenClaw 订阅额度；GPT-5.4 是第一个三项都过关的 OpenAI 主线模型。
- **GPT-5.4 = GPT-5.3-Codex 代码力 + 比 GPT-5.2 更强的世界知识 + 更强工具使用能力 + Codex 订阅额度可用**，四项合一，直接锁定 OpenClaw 天选基座。
- **GDPval 83.0%**：测 AI 在真实工作任务（金融、法律等 44 种职业）中的表现。GPT-5.4 Thinking 83.0% > Claude Opus 4.6 78.0% > GPT-5.3-Codex 70.9%。说明 GPT-5.4 能用人话处理真实业务场景，不再是只会写代码的"天书机器"。
- **SWE-Bench Pro 57.7%**：测真实软件工程问题（四种编程语言）。GPT-5.4 Thinking 57.7% vs GPT-5.3-Codex 56.8%，基本持平，代码能力没有退步。
- **OSWorld-Verified 75.0%**：测 AI 像人一样操作电脑（鼠标点击、键盘输入、跨应用切换）。GPT-5.4 Thinking 75.0% > Claude Opus 4.6 72.7%，且操作速度"快的离谱"。
- **ToolAthon 54.6%**：测 AI 使用工具的能力（Agent 核心指标）。GPT-5.4 Thinking 54.6% vs Claude Sonnet 4.6 44.8%，领先近 10 个百分点。
- **上下文窗口从 40 万 token 升至 100 万 token**：对 Agent 执行长任务至关重要，防止"干着干着忘事儿"。注意：超过 27 万 token 后额度按 2 倍计算，但 Codex 给的额度本身很充裕，实际影响有限。
- **原生计算机使用能力**：GPT-5.4 是 OpenAI 第一个内置原生计算机使用能力的主线模型，代码操控（Playwright 等库）+ 视觉操控（截图 → 鼠标/键盘命令）双路并行，可直接原生操控电脑上绝大多数软件。
- **工具搜索（Tool Search）**：模型不再在 prompt 里预载所有工具定义，而是持有轻量工具列表，按需查找并追加定义。OpenAI 内测结果：**在保持相同准确率的前提下，总体 token 使用量减少 47%**，直接降低成本、加快响应、减少上下文污染。
- **OpenAI 明确支持第三方工具（含 OpenClaw）使用 Codex 订阅额度**，是御三家中唯一公开表态不封号、支持第三方调用的厂商，Claude 封了 OpenClaw 的订阅额度（只能走 API，极贵），Google 大批量封号导致反代方案失效。

---

### 🎯 关键洞察

**为什么 GPT-5.3-Codex 不适合做 OpenClaw 默认模型**：
Codex 是编程特化模型，世界知识甚至不如 GPT-5.2，导致它在规划任务时输出"天书"——技术术语堆砌、缺乏业务语境、非程序员根本看不懂。作者实测让 Codex 审查 AI 热点网站项目的文档规范和代码库，输出文档与 Claude Opus 4.6 的输出对比"一目了然"，Codex 完全不说人话。接入 OpenClaw 当默认模型等于"灾难"。

**为什么 Claude 不适合做 OpenClaw 默认模型**：
Claude Opus 4.6 能力均衡，但 Anthropic 封禁了 OpenClaw 使用 Max Plan 订阅额度（只能在 Claude Code 里用），OpenClaw 只能走 API Key，成本极高，小团队/个人不可持续。Google Antigravity 反代方案也因大批量封号而失效。

**GPT-5.4 的"人话"体验**：作者在 Codex 里实测，GPT-5.4 输出风格明显口语化，例如面对爬取 OpenAI 官网视频的任务，模型自己说"这种活最烦"、"省的跟 Cloudflare 互相折寿"——这正是世界知识和语言风格回归正常的直接体现。

**前端审美**：GPT-5.4 在 Codex 里生成的前端有进步，但仍不如 Claude Opus 4.6 和 Gemini。写作风格仍有"爱用排比句"的怪癖。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|---|---|---|---|
| OpenClaw 默认模型 | 切换为 GPT-5.4 | 代码+世界知识双强，说人话 | 发布当晚 OpenClaw 尚未支持，需等更新 |
| Codex 订阅额度调用 | 走登录方式（非 API Key） | 免费使用订阅额度，无需付 API 费 | OpenAI 明确支持，不封号 |
| 上下文窗口 | 最大 100 万 token | 长任务不丢失上下文 | 超 27 万 token 后额度 ×2 计算 |
| 工具搜索（Tool Search） | 模型按需查找工具定义，非预载 | token 用量减少 47%，响应更快 | 需平台/框架支持该特性 |
| playwright-interactive skill | 安装地址：`https://github.com/openai/skills/tree/main/skills/.curated/playwright-interactive` | 代码+视觉双模式调试 Web/Electron 应用 | 需在 Codex 环境中安装 |
| 原生计算机使用 | 截图 → 鼠标/键盘命令；或通过 Playwright 等库代码操控 | 原生操控电脑绝大多数软件 | GPT-5.4 是首个内置此能力的 OpenAI 主线模型 |

---

### 🛠️ 操作流程

1. **准备阶段**: 确认 OpenClaw 已更新至支持 GPT-5.4 的版本（发布当晚尚未支持，需等社区更新，作者预计睡一觉即可）。使用 ChatGPT/Codex 订阅账号登录，无需单独配置 API Key。

2. **核心执行**: 进入 OpenClaw 设置，将默认模型从 Claude Opus 4.6 / Sonnet 4.6 或 GPT-5.3-Codex 切换为 **GPT-5.4**。如需调试 Web/Electron 应用，在 Codex 中安装 `playwright-interactive` skill（地址见上表）。

3. **验证与优化**: 执行一个包含业务规划 + 代码生成的混合任务，验证输出是否"说人话"且代码质量达标。关注上下文长度，若任务超 27 万 token，注意额度消耗翻倍，合理拆分任务。

---

### 💡 具体案例/数据

| 指标 | GPT-5.4 Thinking | Claude Opus 4.6 | GPT-5.3-Codex | Claude Sonnet 4.6 |
|---|---|---|---|---|
| GDPval（真实业务场景） | **83.0%** | 78.0% | 70.9% | — |
| SWE-Bench Pro（软件工程） | **57.7%** | — | 56.8% | — |
| OSWorld-Verified（电脑操作） | **75.0%** | 72.7% | ~75%（持平） | — |
| ToolAthon（工具使用/Agent） | **54.6%** | — | — | 44.8% |
| 上下文窗口 | **100 万 token** | — | 40 万 token | — |
| 工具搜索 token 节省 | **-47%** | — | — | — |

---

### 📝 避坑指南

- ⚠️ **OpenClaw 发布当晚未立即支持 GPT-5.4**，切换前先确认版本已更新，否则模型列表里看不到。
- ⚠️ **上下文超 27 万 token 后额度按 2 倍计算**，长任务要注意拆分，避免额度快速耗尽。
- ⚠️ **GPT-5.4 写作风格仍有"排比句怪癖"**，写作类任务输出质量仍不如 Claude Opus 4.6，需人工润色。
- ⚠️ **前端 UI 审美仍弱于 Claude Opus 4.6 和 Gemini**，纯前端设计任务慎用 GPT-5.4 作为唯一生成模型。
- ⚠️ **Claude 订阅额度（Max Plan）无法在 OpenClaw 中使用**，只能走 API，成本极高，不要误以为订阅了 Claude 就能在 OpenClaw 里免费用。
- ⚠️ **Google Antigravity 反代方案已失效**，大批量封号，不要再尝试此路径。
- ⚠️ **GPT-5.4 Pro 需要 200 刀 Pro 会员**，对大多数用户无必要，普通 Thinking 版本已足够 OpenClaw 使用场景。

---

### 🏷️ 行业标签

#GPT-5.4 #OpenClaw #Agent基座模型 #Codex #上下文工程 #工具搜索 #计算机使用 #Playwright #模型选型

---

---

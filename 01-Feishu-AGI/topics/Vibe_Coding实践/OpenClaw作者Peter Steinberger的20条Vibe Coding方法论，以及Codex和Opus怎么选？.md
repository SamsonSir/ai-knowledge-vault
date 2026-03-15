# Vibe_Coding实践

## 23. [2026-02-17]

## 📙 文章 4


> 文档 ID: `VlEGwnDo6iKsJIk0SajcH0sonvm`

**来源**: OpenClaw作者Peter Steinberger的20条Vibe Coding方法论，以及Codex和Opus怎么选？ | **时间**: 2025-12-28 | **原文链接**: `https://mp.weixin.qq.com/s/QW7L2FXn...`

---

### 📋 核心分析

**战略价值**: Peter Steinberger（OpenClaw/Clawdbot创始人，后加入OpenAI）用亲身实践总结出一套以codex为核心的高速交付工作流，覆盖模型选择、上下文管理、提示词策略、多项目并行、基础设施自动化全链路。

**核心逻辑**:

- **交付速度的瓶颈已从"写代码"转移到"推理时间"**：大多数软件本质是"把数据从表单推到表单"，不需要深度思考，默认从CLI开始构建，因为agent可以直接调用并验证输出，形成闭环。
- **codex vs Opus的本质差异不在基准分，在"读代码习惯"**：codex会在开始前默默读文件10-15分钟，大幅提高修复正确率；Opus更急切，适合小修改，做大功能/重构时经常漏读文件、遗漏细节、交付低效结果。结论：codex花的时间可能是Opus的4倍，但因为不需要"修复那个修复"，整体反而更快。
- **语言/生态选择比代码本身更重要**：Web项目用TypeScript，CLI用Go（类型系统简单、linting快、agent极擅长写），macOS/iOS有UI用Swift。Go是几个月前完全没考虑过的语言，试了之后发现agent写得非常好。
- **Mac/iOS开发者不再需要Xcode**：不使用xcodeproj文件，Swift的构建基础设施已足够，codex知道如何运行iOS应用和处理模拟器，不需要MCP或特殊配置。
- **"计划模式"是早期模型时代的黑客方案，现在已过时**：不再用plan mode，直接和模型对话，让它谷歌搜索、探索代码、一起创建计划，满意后写"build"或"write plan to docs/*.md and build this"。
- **上下文管理：codex一个会话能完成的事是Claude的5倍**：原因是codex内部思考极度压缩以节省token，而Opus非常啰嗦。GPT-5.2之后不再需要勤奋地为新任务重启会话，即使上下文更满性能依然很好，而且模型已加载大量文件时工作更快。
- **提示词越来越短，图片替代文字**：从前用语音输入写长详细提示词，现在经常只打几个字加一张截图，比如拖一张UI截图进去说"fix padding"或"redesign"，多数情况直接解决问题。
- **跨项目引用是节省提示词的利器**：直接写"look at ../vibetunnel and do the same for Sparkle changelogs"，codex有99%概率正确复制并适配到新项目，新项目搭建也用同样方式。
- **文档维护在docs/文件夹，用脚本强制模型读取**：每个项目的docs文件夹维护子系统和功能文档，全局AGENTS文件中用脚本指令强制模型阅读特定主题文档，项目越大越值得做。
- **直接提交到main，不用worktree**：避免在脑中维护项目不同状态的认知负担，线性演进。大型重构留到分心时做（比如写文章时同时跑4个项目的重构，每个1-2小时）。多人团队此方案不适用。
- **bug即时处理，不写issue**：发现bug立刻提示修复，比写下来再切换上下文回去处理快得多。公开项目有bug tracker给开源用户用，但自己发现的bug直接处理。
- **先CLI后UI的铁律**：任何想法先把核心逻辑做成CLI跑通，再构建UI/扩展。例子：先做summarize CLI（把任何内容转markdown丢给模型），核心跑好后一天内构建完整Chrome扩展。

---

### 🎯 关键洞察

**Oracle工具的诞生与退场逻辑**：

当agent卡住时，Peter发现自己反复手动把内容写进markdown再去查询，于是构建了oracle🧿——一个CLI，允许agent运行GPT-5 Pro，上传文件和提示，管理会话以便稍后检索答案。指令写在全局AGENTS.MD文件中，模型卡住时可自动触发oracle。Pro擅长速通约50个网站后深入思考，运行时间从10分钟到超过1小时不等。

GPT-5.2出来后，oracle的使用频率从每天多次降到每周几次——因为5.2本身已经能一发入魂处理大多数现实编码任务。这个演变轨迹本身就是一个信号：**当你发现自己在为模型的局限性打补丁时，等下一个模型版本往往比维护补丁更高效**。

**知识截止日期的实际影响**：GPT-5.2知识截止到8月底，Opus卡在3月中旬，差了约5个月。使用最新工具时这个差距非常关键。

**VibeTunnel重构案例**：早期试图把多路复用器核心从TypeScript重写，尝试过Rust、Go、Zig，老模型consistently失败，需要大量手工工作。用codex后，给一个两句话的提示，跑了5个多小时，经过多次压缩，一次性交付了可用的Zig转换版本。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 首选模型 | `gpt-5.2-codex`，`model_reasoning_effort = "high"` | 覆盖99%场景，速度与质量平衡 | xhigh没有明显优势但慢很多，不值得切换 |
| tool输出token限制 | `tool_output_token_limit = 25000` | 允许模型一次读更多内容 | 默认值偏小，会静默失败，难以排查 |
| 自动压缩阈值 | `model_auto_compact_token_limit = 233000` | 在272-273k上下文窗口附近留出压缩空间 | 公式：273000 - (25000 + 15000) = 233000；压缩后模型重看代码时会发现bug，有审查效果 |
| ghost_commit | `false` | 关闭 | — |
| unified_exec | `true` | 替换tmux和旧runner脚本 | — |
| apply_patch_freeform | `true` | 开启 | — |
| web_search_request | `true` | 开启网络搜索 | 默认未开启，需手动配置 |
| skills | `true` | 开启skills功能 | — |
| shell_snapshot | `true` | 开启 | — |
| 项目信任级别 | `[projects."/Users/steipete/Projects"]` `trust_level = "trusted"` | 项目目录全信任 | — |
| 语言选择 | Web→TypeScript，CLI→Go，macOS/iOS UI→Swift | agent对这三种语言掌握度最高 | Go的简单类型系统让linting极快 |
| 文档结构 | 每个项目`docs/`文件夹 + 全局`AGENTS.MD` | 强制模型读取正确上下文 | 项目越大越值得维护，小项目可跳过 |

---

### 🛠️ 操作流程

**完整配置文件**（`~/.codex/config.toml`）：

```toml
model = "gpt-5.2-codex"
model_reasoning_effort = "high"
tool_output_token_limit = 25000
# 在 272-273k 上下文窗口附近留出原生压缩的空间。
# 公式：273000 - (tool_output_token_limit + 15000)
# 当 tool_output_token_limit=25000 ⇒ 273000 - (25000 + 15000) = 233000
model_auto_compact_token_limit = 233000

[features]
ghost_commit = false
unified_exec = true
apply_patch_freeform = true
web_search_request = true
skills = true
shell_snapshot = true

[projects."/Users/steipete/Projects"]
trust_level = "trusted"
```

1. **启动新项目**:
   - 先建CLI，跑通核心逻辑，再考虑UI
   - 语言选择：Web→TypeScript，CLI→Go，macOS/iOS→Swift
   - 在项目根目录建`docs/`文件夹，在全局`AGENTS.MD`中写入强制读取指令

2. **日常任务执行**:
   - 直接和模型对话，让它搜索、探索代码、共同制定计划
   - 满意后输入`build`或`write plan to docs/*.md and build this`
   - 跨项目引用：直接写`look at ../project-a and do the same for project-b`
   - UI迭代：截图拖进去 + 几个词（"fix padding" / "redesign"）
   - 发现bug：立刻提示修复，不写issue

3. **多项目并行管理**:
   - 同时处理3-8个项目，一个主项目+几个卫星项目
   - 利用codex队列功能积压新想法
   - 大型重构安排在分心时（如写文章、开会时）后台跑
   - 直接提交到main，不用worktree（单人项目适用）
   - 两台Mac通过git同步，需要UI/浏览器自动化的任务移到不打扰主机的那台

4. **上下文管理**:
   - GPT-5.2后不再需要为新任务重启会话
   - 上下文满了也没关系，模型已加载文件时工作更快
   - 注意：codex没有"文件已修改"的系统事件，需要自己保证任务序列化或改动足够分散

---

### 💡 具体案例/数据

- **VibeTunnel Zig重构**：两句话提示，codex跑5小时+，经过多次压缩，一次性交付可用的TypeScript→Zig转换版本。老模型（Rust/Go/Zig均尝试）consistently失败。
- **Oracle使用频率变化**：GPT-5.1时代每天多次触发oracle；GPT-5.2上线后降至每周几次。
- **codex vs Opus速度对比**：codex完成可比任务有时花Opus的4倍时间，但因为不需要"修复那个修复"，整体交付反而更快。
- **知识截止日期差距**：GPT-5.2截止8月底，Opus截止3月中旬，差约5个月，使用最新工具时影响显著。
- **summarize CLI→Chrome扩展**：先做CLI核心（任何内容→markdown→模型总结），核心跑好后一天内完成整个Chrome扩展。本地运行，支持免费/付费模型，本地转录视频/音频，与本地守护进程通信速度极快。

---

### 📝 避坑指南

- ⚠️ `tool_output_token_limit`默认值偏小，会导致模型静默失败（看不到报错），必须手动调高到25000
- ⚠️ `web_search_request`默认未开启，需在config中显式设为`true`
- ⚠️ Opus做大功能/重构时经常不读完整文件，漏掉关键部分，交付低效结果——大任务必须用codex
- ⚠️ 直接提交main的工作流只适合单人项目，多人团队会产生大量冲突
- ⚠️ codex没有"文件已修改"系统事件（不像Claude Code），多会话并行时需自己保证任务不互相踩踏
- ⚠️ 不要过早引入复杂的多agent编排系统——大多数情况下自己才是瓶颈，简单队列足够
- ⚠️ 依赖和框架选择是真正需要人工判断的地方：维护状态、peer依赖健康度、流行度（决定模型世界知识覆盖度）——这里省不了思考时间
- ⚠️ xhigh推理模式没有明显质量提升但速度慢很多，默认用high即可

---

### 🏷️ 行业标签

#VibeCoding #AIAgent #Codex #ClaudeOpus #工作流 #提示词工程 #多项目并行 #上下文管理 #TypeScript #Go #Swift

---

---

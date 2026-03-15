# AI编程与开发工具

## 46. [2026-03-08]

## 📕 文章 1


> 文档 ID: `JZsTwE8pjibdzPktwmkcpu0enqc`

**来源**: Openclaw自己操作Claude code完整开发了TikTok爆款分析系统 | **时间**: 2026-03-08 | **原文链接**: `https://mp.weixin.qq.com/s/Nlu_8FZZ...`

---

### 📋 核心分析

**战略价值**: 用 OpenClaw 充当项目经理、Claude Code 充当工程师，构建一套「我只说需求、AI 全程自主开发」的无人值守全栈开发流水线。

**核心逻辑**:

- OpenClaw 单独用于产品开发是失败的：进程死了不知道、参数传错不报警、卡在交互提示上等一整夜，作者连踩两周坑才得出结论
- 正确分工：OpenClaw 负责项目管理（24h在线、接飞书/Telegram/Discord、持久记忆、多任务调度），Claude Code 负责编程执行（理解整个代码库、自主调试修复、完整工具链）
- 用户只参与两个节点：①确认 PRD 和技术方案，②看最终测试效果截图，中间全程不介入
- 直接用 Claude Code 的三大痛点：①交互式阻塞（改完文件要你确认才继续）；②遇到报错就停等人；③一次只能处理一件事
- OpenClaw 解决这三点的方式：①自己判断大部分情况如何处理，处理不了才飞书通知；②自己读错误日志、自己发修复指令给 Claude Code；③可并行起多个 Claude Code 后台进程（如同时跑后端 API + 前端样式）
- 调用 Claude Code 必须用 PTY 模式，否则 CLI 会挂起或输出乱码，这是 OpenClaw 社区最高频踩坑点
- 核心命令一行解决三个致命问题（进程管理、交互阻塞、结果回传）：`bash pty:true workdir:~/projects/xxx background:true command:"claude --session-id xxx --permission-mode acceptEdits '任务指令'"`
- `--permission-mode acceptEdits` 让 Claude Code 不用每改一个文件都停下来问，`background:true` 让 OpenClaw 可以继续处理其他事，`--session-id` 保持上下文、中断后可 `--resume` 恢复
- 需要单独让 AI 整理一份 Claude Code 实操文档作为 Skill 文件，让 OpenClaw 真正"懂"如何操控 Claude Code
- 整套方案的核心载体是一个 `skills/fullstack-dev/SKILL.md` 文件，定义了从收需求→写PRD→初始化项目→逐功能开发→自动测试→截图报告的完整闭环

---

### 🎯 关键洞察

**为什么 PTY 模式是关键**：Claude Code 的 CLI 是为人类交互设计的，依赖终端的 TTY 特性来渲染输出和接收输入。OpenClaw 调用它时走的是非交互式管道，没有 TTY 就会导致输出缓冲不刷新（乱码）或者进程挂起等待输入（永久阻塞）。加 `pty:true` 模拟一个伪终端，让 Claude Code 以为自己在跟人交互，从而正常运行。

**为什么要写 PRD 再开发**：直接扔需求给 Claude Code 会导致理解偏差，中途返工成本极高。让 OpenClaw 先输出 PRD 给人确认，相当于在最低成本节点做了一次对齐，后续开发方向不会跑偏。

**并行调度的价值**：传统 Claude Code 工作流是串行的，后端写完才能调前端。OpenClaw 可以起多个 Claude Code 进程并行推进，理论上可以把开发时间压缩到接近单个最长任务的时间，而不是所有任务时间之和。

---

### 📦 配置/工具详表

| 模块 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|------|-------------|---------|-----------|
| PTY 调用命令 | `bash pty:true workdir:~/projects/xxx background:true command:"claude --session-id xxx --permission-mode acceptEdits '任务'"` | 后台无阻塞运行 Claude Code | 不加 `pty:true` 必挂起，这是最高频踩坑点 |
| `--permission-mode acceptEdits` | Claude Code 参数 | 自动接受所有文件修改，不停下来问 | 生产环境谨慎，会直接写文件 |
| `--session-id` + `--resume` | Claude Code 参数 | 保持上下文，中断可恢复 | session-id 需自己命名管理 |
| `background:true` | OpenClaw bash 参数 | 任务后台跑，OpenClaw 可继续处理其他事 | 需配合结果回传机制，否则不知道跑完没 |
| Playwright | 测试工具 | 自动端到端测试，截图发飞书 | 需提前安装，TOOLS.md 里声明 |
| FFmpeg | 视频处理工具 | 处理 TikTok 视频拆帧 | 需提前安装，TOOLS.md 里声明 |
| AGENTS.md | 工作空间配置文件 | 告知 OpenClaw 有开发能力，收到需求自动触发 | 必须在末尾追加，不能覆盖原有内容 |
| USER.md | 用户偏好配置 | 声明「技术方案你自己定，别问我技术细节」 | 不写这条，OpenClaw 会不停来问技术问题 |
| SKILL.md | 核心技能文件 | 定义完整开发流程的 5 个 Phase | 路径必须是 `skills/fullstack-dev/SKILL.md` |

---

### 🛠️ 操作流程

**第一步：AGENTS.md 末尾追加**

打开 OpenClaw 工作空间的 `AGENTS.md`，在最后加：

```markdown
## 🔧 Claude Code 开发集成

当用户描述一个想做的产品/网站/工具时，使用 skills/fullstack-dev/SKILL.md 中的流程自主完成开发。

核心规则：
- 你是项目经理，Claude Code 是开发工程师
- 调用 Claude Code 必须用 bash pty:true，否则会挂起
- 用户只需要确认 PRD 和最终验收，中间不要打扰
- 出了技术问题自己解决，需要密码/Key 才问用户
- 开发完用 Playwright 自动测试，截图发给用户
```

**第二步：TOOLS.md 追加开发工具声明**

```markdown
## 开发工具
- Claude Code：已安装，用 OAuth 登录
- 项目目录：~/projects/
- Playwright：用于端到端测试
- FFmpeg：视频处理
```

**第三步：USER.md 加偏好声明**

在你的个人信息后面加一条：

```
- 偏好：我只说产品需求，技术方案你自己定。别问我技术细节。
```

**第四步：创建核心 Skill 文件**

路径：`skills/fullstack-dev/SKILL.md`，内容结构如下（完整版需后台获取）：

```markdown
---
description: "全栈项目开发技能。当用户描述一个想做的产品/网站/工具时自动触发。你负责从需求理解到开发执行、测试验收的全流程。用户只需要描述想法，你自主完成一切。"
---

# Fullstack Development Skill

你是一个资深技术合伙人。用户是产品负责人，他只说想要什么，剩下的全部由你搞定。
你有一个高级开发工程师：Claude Code。你通过命令行指挥它写代码。

## 核心原则
## 完整流程

## Phase 1：需求理解 → PRD
## Phase 2：项目初始化
## Phase 3：逐功能开发
## Phase 4：自动化测试
## Phase 5：交付报告
```

> ⚠️ 完整 SKILL.md 内容（含每个 Phase 的详细指令）需关注公众号「饼干哥哥AGI」后台回复「Claude code」获取

**第五步：发需求触发开发**

在飞书发以下格式：

```
我想做一个 [产品名]。

[3-5 句话描述给谁用、解决什么问题]

核心功能：
1. xxx
2. xxx
3. xxx

做好后测试一遍发我看效果。
```

---

### 💡 具体案例/数据

作者实际构建的产品：TikTok 爆款视频拆解网站

功能清单：
- 用户上传视频 → 自动分析营销策略
- 逐帧拆解每个镜头
- 逆向生成可直接用于 Sora 的提示词
- 语音转结构化脚本

作者发给 OpenClaw 的原始需求（原文完整保留）：
> 我要开发的产品是：tiktok视频拆解网站。功能是，用户上传一个视频后，能逆向出它的提示词、拆成多个视频片段做更细致的分析。主要目的是帮助用户分析爆款视频，并且提炼出来一套玩法后，自己能复刻、模拟生成这类爆款。

从发出这段话到产品可用，作者全程只参与了两次：确认 PRD + 看最终截图。

---

### 📝 避坑指南

- ⚠️ 不加 `pty:true` 是最高频踩坑：Claude Code CLI 会挂起或输出乱码，OpenClaw 社区无数人踩过，一行参数解决
- ⚠️ USER.md 不写「别问我技术细节」：OpenClaw 会不停来飞书问你技术问题，把你当成技术顾问而不是老板
- ⚠️ 不用 `--session-id`：上下文中断后无法恢复，等于从头开始，长任务必须加
- ⚠️ 不加 `background:true`：OpenClaw 会阻塞在这个任务上，无法并行处理其他事
- ⚠️ OpenClaw 单独做产品开发：进程死了不知道、卡在交互提示上等一整夜，作者踩了两周才放弃这条路
- ⚠️ SKILL.md 路径写错：必须是 `skills/fullstack-dev/SKILL.md`，路径不对 OpenClaw 找不到技能文件

---

### 🏷️ 行业标签

#OpenClaw #ClaudeCode #AI自动化开发 #无人值守开发 #AgentOrchestration #TikTok分析工具 #全栈开发 #PTY模式 #项目经理Agent

---

---

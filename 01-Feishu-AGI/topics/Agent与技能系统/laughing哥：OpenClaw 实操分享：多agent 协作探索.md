# Agent与技能系统

## 48. [2026-02-03]

## 📒 文章 7


> 文档 ID: `GX6rwYFc7icPznkysXHcb0jXn7e`

**来源**: laughing哥：OpenClaw 实操分享：多agent 协作探索 | **时间**: 2026-02-03 | **原文链接**: https://mp.weixin.qq.com/s/XfX7l4RL...

---

### 📋 核心分析

**战略价值**: OpenClaw 是当前最热门的开源 AI Agent 框架（GitHub 15万 star），通过系统级配置文件 + skill 技能包 + 多 agent 协作，实现真正意义上的 7x24 小时数字员工。

**核心逻辑**:

- OpenClaw 历经三次改名（Clawdbot → Moltbot → OpenClaw），项目地址：`https://github.com/openclaw/openclaw`，GitHub star 数已达 15万，是当前最活跃的 AI Agent 开源项目
- 部署模型：需自备大模型 API key，配置后通过 Telegram 或飞书与 agent 交互，支持发邮件、做研究等任务
- 系统级配置文件是 agent 行为的核心骨架，共 7 个文件，每次会话按固定顺序读取：`SOUL.md → USER.md → memory/ → MEMORY.md`
- HEARTBEAT.md 是定时任务引擎：文件为空则跳过心跳检查，写入任务则定期执行（如每小时汇报进展、跑数据、发邮件），只要宿主机 24 小时开机，agent 就 24 小时运转
- skill 技能包机制是 OpenClaw 的核心扩展点：预装 skill 不够用时，可用内置的 `skill_creator` 自行编写新 skill，理论上可无限扩展 agent 能力边界
- 多 profile 多开模式：新建 profile 会在新端口号上跑一套独立服务，Telegram / 飞书账户彼此隔离，适合给不同用户（如家庭成员）各自配置独立 bot
- 同一 profile 下可运行多个 agent（如认干小王 + 可爱悠悠同住一台无头 Mac，同 profile 不同 agent），多 agent 可拉入同一群组协作分工
- 错误处理策略一：agent 不回消息时，通过 SSH 接管宿主机，让另一个 Claude 实例直接诊断并修复（agent 互相兜底）
- 错误处理策略二：agent 具备自我修复能力，可自行查找配置问题（如飞书 bot 长链接连不上、新端口服务未启动），依次排查文件并修改，无需人工介入
- token 消耗是唯一实质性成本，作者开通智谱套餐后，3个 agent 协作运行，半夜低峰期消耗约 3000万 token，日常任务成本可控

---

### 🎯 关键洞察

**为什么 OpenClaw 比普通大模型产品更有价值**：

普通大模型（豆包、ChatGPT）是"问答机器"，你问它才动。OpenClaw 的核心差异在于**主动性**和**持久性**：
- HEARTBEAT 机制让 agent 脱离人工触发，自主按计划执行任务
- 系统级文件（SOUL/USER/IDENTITY）让 agent 拥有持久记忆和人格，跨会话保持上下文
- skill 机制让 agent 能力可编程扩展，而非受限于模型本身的训练边界

**多 agent 协作的实际价值**：三个 agent 在同一群组内，理论上可并行分工（一个跑数据、一个写报告、一个对外沟通），且互相可以作为对方的"运维工程师"——当一个 agent 故障时，另一个 agent 通过 SSH 权限直接介入修复。

---

### 📦 配置/工具详表

| 文件 | 用途 | 关键内容 | 注意事项 |
|------|------|---------|---------|
| AGENTS.md | 工作区宪法 | 必读文件列表、记忆管理规则、安全边界、群聊行为准则、Heartbeat 使用指南 | 每次会话启动时强制读取 |
| SOUL.md | agent 性格定义 | 核心价值观（真诚/有主见/主动）、边界规则、语气风格 | 修改前需告知用户，属于 evolving 文件 |
| USER.md | 用户档案 | 姓名、称呼、时区、偏好、项目、兴趣、厌恶项 | 随时间累积上下文，越用越准 |
| TOOLS.md | 环境备忘录 | 摄像头名称/位置、SSH 主机信息、TTS 语音偏好、环境特定配置 | 本地环境信息手动维护 |
| IDENTITY.md | 身份卡 | 名字、物种类型（AI/机器人/精灵）、Vibe 风格、Emoji 签名、头像路径/URL/data URI | 多 agent 场景下每个 agent 独立配置 |
| HEARTBEAT.md | 定时任务清单 | 空白=跳过；写入任务=定期执行（邮件/日历/天气/数据汇报等） | 宿主机必须保持开机状态 |
| BOOTSTRAP.md | 初始化引导脚本 | 首次运行时执行的引导流程 | 用完即删，不可重复执行 |

---

### 🛠️ 操作流程

1. **准备阶段**:
   - 部署 OpenClaw（项目地址：`https://github.com/openclaw/openclaw`）
   - 准备大模型 API key（支持 Claude、GLM、Qwen 等）
   - 配置通讯渠道：Telegram bot token 或飞书 bot 长链接
   - 可选：准备无头 Mac 或服务器作为 24 小时宿主机，并开启 SSH 访问权限

2. **核心执行**:
   - 按需编辑 7 个系统级配置文件，重点配置 `SOUL.md`（性格）、`USER.md`（用户信息）、`HEARTBEAT.md`（定时任务）
   - 在 `HEARTBEAT.md` 中写入定时任务（如：每小时汇报进展、每天早上发天气、定时跑数据）
   - 通过 `skill_creator` 为 agent 添加所需 skill，不确定用什么 skill 直接问 agent 本身
   - 多开场景：新建 profile → 自动分配新端口 → 独立配置 Telegram/飞书账户
   - 多 agent 场景：同一 profile 下创建多个 agent，拉入同一群组实现协作

3. **验证与优化**:
   - 观察 agent 是否在 typing（有 typing 状态 = 正在执行任务）
   - agent 不回消息时：SSH 连接宿主机 → 让另一个 Claude 实例诊断 → 自动修复
   - 飞书 bot 长链接连不上时：让同机器上的 agent 自行排查配置文件并修复
   - 定期检查 token 用量，评估任务编排密度是否合理

---

### 💡 具体案例/数据

- **定时任务实战**：周末凌晨 3 点多，agent（无情的干token机器）自动执行 HEARTBEAT 定时任务，每小时发送一次进展汇报，全程无人值守
- **多 agent 架构**：作者当前运行 3 个 agent：
  - 「无情的干token机器」：跑在独立服务器上
  - 「认干小王」：跑在无头 Mac 上，profile A
  - 「可爱悠悠」：跑在无头 Mac 上，同 profile A（龙凤胎 agent，共享环境但独立身份）
  - 三者同在一个 Telegram 群组，除作者外全是机器人
- **自我修复案例**：新建 profile 配置飞书 bot，长链接连不上、新端口服务未启动，同机器上的 agent 自行依次排查原因、修改配置文件，最终修复，全程无需人工介入
- **token 消耗参考**：3 个 agent 协作运行，半夜低峰期累计消耗约 3000万 token

---

### 📝 避坑指南

- ⚠️ 飞书 bot 多开时，新 profile 的长链接连不上大概率是端口服务未正常启动，让同机器 agent 自查比手动排查更高效
- ⚠️ agent 不回消息不一定是模型问题，可能是进程异常，SSH 接管宿主机后让另一个 Claude 实例诊断是最快的恢复路径
- ⚠️ BOOTSTRAP.md 用完即删，重复执行会导致初始化逻辑重跑
- ⚠️ SOUL.md 属于 evolving 文件，修改前需告知用户，否则 agent 性格会静默变更
- ⚠️ 上下文污染问题：长期运行的 agent 上下文会积累噪音，需定期清空（作者提到「无情的干token机器」上下文有点污染，需清空）
- ⚠️ 24 小时运行依赖宿主机持续开机，无头 Mac 或服务器是更稳定的选择，笔记本合盖会中断任务

---

### 🏷️ 行业标签

#OpenClaw #AI-Agent #多Agent协作 #数字员工 #开源项目 #自动化 #Heartbeat定时任务 #Skill技能包 #无头Mac #飞书Bot

---

---

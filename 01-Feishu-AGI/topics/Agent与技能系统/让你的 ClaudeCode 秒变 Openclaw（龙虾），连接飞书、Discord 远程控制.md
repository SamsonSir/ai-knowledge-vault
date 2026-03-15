# Agent与技能系统

## 99. [2026-03-05]

## 📒 文章 7


> 文档 ID: `BbFZw6IaOiAwBZk6GAlcVfLgnBg`

**来源**: 让你的 ClaudeCode 秒变 Openclaw（龙虾），连接飞书、Discord 远程控制 | **时间**: 2026-03-05 | **原文链接**: `https://mp.weixin.qq.com/s/fjGd3mBJ...`

---

### 📋 核心分析

**战略价值**: 作者歸藏用 16 天、40 个版本、220 次提交，将 Claude Code 桌面端 Codepilot 扩展为支持飞书/Discord/Telegram 远程控制的 Agent 平台，并将 IM 连接能力拆分为两个开源项目供社区复用。

**核心逻辑**:

- **Codepilot 是什么**: Claude Code 的桌面端客户端，非官方，MacOS + Windows 全平台，定位比 OpenClaw 更安全、更易用，适合小白入门。发布地址：`https://github.com/op7418/CodePilot/releases/tag/v0.26.0`
- **Codepilot 当前功能集**: 飞书等 IM 远程连接、可视化配置 Code plan 套餐、设计 Agent + 素材库、多 Agent 并发分屏、Token 使用检测看板、一键安装 Claude Code。
- **拆分逻辑**: IM 连接能力从 Codepilot 中独立开源，分为两个项目——面向普通用户的 `Claude-to-IM-skill`，以及面向开发者的 `Claude-to-IM` 库。
- **Claude-to-IM-skill 核心能力**: 支持 Telegram、Discord、飞书三平台任意组合启用；交互式向导引导配置（首次启动 Claude 会逐步指引你点哪里）；工具调用需在聊天中通过内联按钮明确批准（允许/拒绝/本次会话允许）；流式实时预览（Telegram 和 Discord 支持）；会话在守护进程重启后持久化；token 以 chmod 600 存储，日志自动脱敏。
- **安装极简**: 一条命令搞定，无需写代码：`npx skills add op7418/Claude-to-IM-skill`，安装后运行 `/claude-to-im setup` 完成配置。
- **Claude-to-IM 库的核心差异点**: 面向基于 Agent SDK 开发的产品，提供可复用的多平台适配器，所有宿主依赖通过 4 个 DI 接口抽象，不绑定数据库驱动、不绑定 LLM 客户端、不绑定框架，可直接集成进自己的产品。
- **安全与可靠性机制（Claude-to-IM 库）**: 令牌桶速率限制每个聊天 20 条/分钟、用户授权白名单、完整审计日志、输入验证、指数退避重试、消息去重、按平台限制自动分块。
- **Markdown 渲染适配**: Telegram 用 HTML、Discord 用 Discord 风格 Markdown、飞书用富文本卡片，各平台原生格式化。
- **连接协议差异**: Telegram 用长轮询、Discord 用 Gateway WebSocket、飞书用 WSClient，三种不同接入方式已封装好。

---

### 📦 配置/工具详表

| 项目 | 目标用户 | 安装/接入方式 | 支持平台 | 关键特性 | 仓库地址 |
|------|---------|------------|---------|---------|---------|
| Claude-to-IM-skill | 普通用户/小白 | `npx skills add op7418/Claude-to-IM-skill` | Telegram、Discord、飞书 | 交互式向导配置、无需写代码 | `https://github.com/op7418/Claude-to-IM-skill` |
| Claude-to-IM | 开发者/产品集成 | 作为库引入，参考文档 | Telegram、Discord、飞书 | DI 抽象、宿主无关、速率限制、审计日志 | `https://github.com/op7418/Claude-to-IM` |
| Codepilot | 所有用户 | 下载 Release 包 | MacOS、Windows | 全功能 Claude Code 桌面端 | `https://github.com/op7418/CodePilot/releases/tag/v0.26.0` |

---

### 🛠️ 操作流程（Claude-to-IM-skill 快速上手）

1. **安装 Skill**
   ```bash
   npx skills add op7418/Claude-to-IM-skill
   ```

2. **启动配置向导**
   在 Claude Code 中运行：
   ```
   /claude-to-im setup
   ```
   Claude 会逐步引导你获取并填入各平台 token（含详细点击路径说明）。

3. **选择启用的平台**
   Telegram、Discord、飞书可任意组合，按需启用。

4. **权限审批**
   工具调用时，IM 聊天中会出现内联按钮，手动点击「允许 / 拒绝 / 本次会话允许」。

5. **远程交互**
   配置完成后，在外部通过对应 IM 直接与 Claude Code 对话，流式输出实时可见。

---

### 🛠️ 操作流程（Claude-to-IM 开发者集成）

1. **引入库**，参考官方文档：`https://github.com/op7418/Claude-to-IM`
2. **实现 4 个 DI 接口**，注入自己的数据库驱动、LLM 客户端、框架依赖。
3. **选择平台适配器**：Telegram（长轮询）/ Discord（Gateway WebSocket）/ 飞书（WSClient）。
4. **配置速率限制**：默认每聊天 20 条/分钟，可按需调整。
5. **配置用户授权白名单**，启用完整审计日志。

---

### 📝 避坑指南

- ⚠️ Claude-to-IM-skill 的流式预览仅 Telegram 和 Discord 支持，飞书暂不支持实时流式输出。
- ⚠️ token 存储权限为 chmod 600，部署时确认文件系统权限正确，否则密钥保护失效。
- ⚠️ Claude-to-IM 库宿主无关设计依赖正确实现 4 个 DI 接口，接口未实现完整会导致运行时报错。
- ⚠️ 速率限制为令牌桶机制，每个聊天 20 条/分钟，高频自动化场景需注意触发限流。

---

### 🏷️ 行业标签

#ClaudeCode #AgentSDK #飞书集成 #Discord #Telegram #VibeCoding #开源工具 #远程控制 #IM集成

---

---

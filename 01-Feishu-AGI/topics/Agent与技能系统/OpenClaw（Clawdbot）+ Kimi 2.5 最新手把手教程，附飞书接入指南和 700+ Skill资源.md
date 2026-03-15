# Agent与技能系统

## 41. [2026-01-31]

## 📘 文章 3


> 文档 ID: `H9wRwvNW9ikaDIkOIpJc1bl2n5d`

**来源**: OpenClaw（Clawdbot）+ Kimi 2.5 最新手把手教程，附飞书接入指南和 700+ Skill资源 | **时间**: 2026-01-31 | **原文链接**: `https://mp.weixin.qq.com/s/8DwabUPP...`

---

### 📋 核心分析

**战略价值**: 用 Kimi 2.5（开源模型，Design Arena 击败 Gemini 3 Pro 和 Claude）替代 Claude Opus 4.5 接入 OpenClaw，实现低成本高质量的 AI Agent 本地化部署，并通过飞书等 IM 工具实现日常指令下发。

**核心逻辑**:

- **Kimi 2.5 能力验证**：在 Design Arena 设计榜打败 Gemini 3 Pro 和 Claude，属于开源模型；一句话直出精美 TodoList 网页；能独立完成复杂多步骤 Skill（调用 Listenhub 生成音频+字幕时间轴 → 基于字幕生成图片提示词 → 调用即梦生图 → 调用 Manim 生成透明文本动效 → 生成片头片尾 → ffmpeg 拼接完整视频），此前只有 Claude Opus 4.5 能稳定完成该流程。
- **工具命名混乱警告**：Clawdbot 一周内三次改名（Clawdbot → Moltbot → OpenClaw），当前正式名称为 **OpenClaw**，搜索教程时注意版本对应。
- **安装入口唯一**：Mac/Linux 终端一行命令安装，Windows 推荐用 Warp 终端；安装脚本地址 `https://openclaw.ai/install.sh`。
- **Onboarding 关键选择**：Model/auth Provider 必须选 **Kimi Code API Key**（对应 Kimi 会员套餐），粘贴 API Key 后设为默认模型。
- **Hook 三件套必选**：① 启动时注入 Markdown 文件（类 README 内容注入）；② 操作日志记录（记录本次会话命令与上下文）；③ 新会话保存当前会话上下文摘要（无缝衔接历史）。
- **飞书接入核心坑**：事件配置和回调配置的订阅方式必须选**长链接**，否则无法建立连接；配置完 appId/appSecret 后必须执行 `openclaw gateway restart`，否则飞书端事件回调会报错。
- **飞书权限清单完整性**：必须开通 6 项权限 + 4 个事件订阅，缺一不可（详见配置表）。
- **IM 生态横向对比**：飞书对国人最友好；TG 配置最简单；Discord 配置最复杂但 Markdown 展示格式最佳；另支持 WhatsApp、iMessage。
- **Skill 冷启动方案**：OpenClaw 自动加载 Claude 全局安装的 Skill；不会写 Skill 可直接用 `https://github.com/VoltAgent/awesome-openclaw-skills`（已收录 700+ Skill）。
- **多模型管理**：支持添加备用模型和按会话线程指定不同模型，具体用法可直接在 OpenClaw 内提问。

---

### 🎯 关键洞察

**为什么 Kimi 2.5 值得接入 OpenClaw**：

原因 → Kimi 2.5 是开源模型，在 Design Arena 设计榜击败闭源的 Gemini 3 Pro 和 Claude，前端生成质量达到顶级水准，且 API 通过 Kimi 会员套餐即可获取，成本远低于 Claude Opus 4.5。

动作 → 用 Kimi Code API Key 替换默认模型，接入 OpenClaw 执行复杂多步骤 Skill。

结果 → 原本只有 Claude Opus 4.5 能稳定跑通的视频生成 Skill（Listenhub + 即梦 + Manim + ffmpeg 全链路），Kimi 2.5 同样能完成，出乎意料。

---

### 📦 配置/工具详表

#### 飞书权限配置

| 权限/事件 | 类型 | 是否必需 | 备注 |
|----------|------|---------|------|
| `contact:user.base:readonly` | 权限 | 必需 | 基础用户信息 |
| `im:message` | 权限 | 必需 | 消息读写 |
| `im:message.p2p_msg:readonly` | 权限 | 必需 | 需先开通 bot 能力 |
| `im:message.group_at_msg:readonly` | 权限 | 必需 | 需先开通 bot 能力 |
| `im:message:send_as_bot` | 权限 | 必需 | bot 发消息 |
| `im:resource` | 权限 | 必需 | 上传图片或文件资源 |
| `im.message.receive_v1` | 事件 | 必需 | 接收消息核心事件 |
| `im.message.message_read_v1` | 事件 | 建议 | 消息已读回执 |
| `im.chat.member.bot.added_v1` | 事件 | 建议 | bot 被拉入群 |
| `im.chat.member.bot.deleted_v1` | 事件 | 建议 | bot 被移出群 |

#### 常用命令速查

| 功能 | 命令 |
|------|------|
| 启动 TUI | `openclaw tui` |
| 重启网关 | `openclaw gateway restart` |
| 开启新对话 | `/new` |
| 添加备用模型 | `openclaw models fallbacks add [模型公司代号/模型名称]` |
| 设置默认模型 | `openclaw models set [模型公司代号/模型名称]` |
| 安装飞书插件 | `openclaw plugins install @m1heng-clawd/feishu` |

---

### 🛠️ 操作流程

**1. 准备阶段：获取 Kimi API Key**

- 开通 Kimi 会员套餐：`https://www.kimi.com/membership/pricing`
- 进入控制台创建 API Key：`https://www.kimi.com/code/console`
- ⚠️ API Key 只显示一次，立即复制保存到安全位置

**2. 安装 OpenClaw**

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

- 进入 Onboarding 后：左右方向键选 Yes → Onboarding mode 选 **QuickStart**
- Model/auth Provider 选 **Kimi Code API Key**
- 粘贴 API Key → 选第一个设为默认模型
- Skill 配置：上下箭头移动，空格选中，回车确认
- Hook 三个全选：Markdown 注入 + 操作日志 + 会话摘要
- 界面选择：TUI（命令行）或 Web UI，两者都会安装，不互斥

**3. 飞书接入（完整流程）**

```bash
# Step 1: 安装飞书插件
openclaw plugins install @m1heng-clawd/feishu

# Step 2: 配置凭证（替换为你的实际值）
openclaw config set channels.feishu.appId "你的App ID"
openclaw config set channels.feishu.appSecret "你的App Secret"
openclaw config set channels.feishu.enabled true

# Step 3: 重启网关（必须执行，否则飞书回调报错）
openclaw gateway restart
```

- 飞书开放平台：`https://open.feishu.cn/app?lang=zh-CN`
- 创建企业自建应用 → 添加应用能力 → 找到「机器人」点击添加
- 在「凭证与基础信息」复制 App ID 和 App Secret
- 在「权限管理」开通上表中全部 6 项权限
- 事件配置和回调配置：订阅方式均选**长链接**
- 添加 4 个事件（`im.message.receive_v1` 为必需）
- 在「版本管理与发布」创建版本并发布
- 打开飞书搜索「OpenClaw」即可找到机器人

**4. 多模型管理示例**

```bash
# 添加备用模型（示例）
openclaw models fallbacks add openai-codex/gpt-5.2-codex

# 设置默认模型为 Kimi
openclaw models set kimi-code/kimi-for-coding
```

---

### 💡 具体案例/数据

- **复杂 Skill 全链路测试**（原作者自写 Skill）：
  1. 调用 Listenhub 生成音频 + 字幕时间轴
  2. 基于字幕生成图片提示词
  3. 调用即梦 API 生图
  4. 调用 Manim 生成透明文本动效
  5. 根据 IP 头像生成片头和片尾
  6. ffmpeg 拼接生成完整视频
  - 结论：此前只有 Claude Opus 4.5 能稳定跑通，Kimi 2.5 同样完成，超出预期。

- **Skill 资源库**：`https://github.com/VoltAgent/awesome-openclaw-skills`，已收录 700+ Skill，可直接复用。

- **飞书插件来源**：`https://github.com/m1heng/clawdbot-feishu`

- **Discord 配置参考**：`https://x.com/AppSaildotDEV/status/2016384987596206383`

- **常见坑汇总参考**：`https://x.com/lyc_zh/status/2016984907226939820`

---

### 📝 避坑指南

- ⚠️ **API Key 只显示一次**：创建后立即复制，关闭页面后无法再查看。
- ⚠️ **飞书订阅方式必须选长链接**：事件配置和回调配置两处都要选，选错会导致连接建立失败。
- ⚠️ **配置飞书凭证后必须重启网关**：`openclaw gateway restart` 不执行，飞书端事件回调必报错。
- ⚠️ **bot 能力必须先开通**：`im:message.p2p_msg:readonly` 和 `im:message.group_at_msg:readonly` 依赖 bot 能力，需先在「添加应用能力」中添加机器人。
- ⚠️ **工具名称混乱**：搜索教程时注意 Clawdbot / Moltbot / OpenClaw 是同一工具的不同历史名称，当前正式名为 OpenClaw。
- ⚠️ **已有网关需重启**：如果电脑之前安装过旧版本，Onboarding 时建议选重启网关，避免端口冲突。
- ⚠️ **让 AI 帮配置飞书有边界**：插件安装和 config set 可以让 AI 执行，但飞书开放平台的权限开通、事件订阅、版本发布必须手动操作。

---

### 🏷️ 行业标签

#OpenClaw #Kimi2.5 #AIAgent #飞书机器人 #本地化部署 #Skill工程 #多模型管理 #前端生成

---

---

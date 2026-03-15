# Agent与技能系统

## 31. [2026-01-27]

## 📘 文章 3


> 文档 ID: `QQqTwBCfEirecCkSPiWcPceanfe`

**来源**: 开源AI助手 ClawdBot 火爆全网，已狂飙50K Star！附喂饭级安装使用教程 | **时间**: 2026-01-27 | **原文链接**: `https://mp.weixin.qq.com/s/nAC-Z-Bz...`

---

### 📋 核心分析

**战略价值**: ClawdBot 是一个开源、自托管的"主动型"个人AI助手，部署在服务器上后通过 Telegram 等聊天软件与你交互，能7×24小时自主执行任务、主动推送信息，是从"人找AI"到"AI找人"的范式转变。

**核心逻辑**:

- **范式转变**：传统AI（ChatGPT/Claude）是"人找AI"——打开网页提问；ClawdBot 是"AI找人"——它主动给你发消息、主动干活，你不在线它也在跑。
- **运行架构**：ClawdBot 是一个持续运行在服务器（或本地旧电脑）上的进程，通过 Telegram Bot / iMessage / WhatsApp 等聊天渠道与用户交互，不需要专用客户端。
- **爆发速度**：GitHub 项目地址 `https://github.com/clawdbot/clawdbot`，20天内 Star 从几百暴涨至 40K+，单日最高涨幅 30K Star，属于现象级开源项目。
- **硬件误区澄清**：Mac Mini 销量跟涨是误区，ClawdBot 对硬件要求极低，2核4G/8G 内存的云服务器（或家里旧笔记本）完全够用，无需高性能机器。
- **三大核心优势**：① 有记忆（持久上下文，昨天说不吃香菜，下周订餐还记得）；② 主动推送（授权后可主动告知航班延误、股票跌破预警价等）；③ 数据自托管（数据在自己服务器，隐私可控）。
- **工具集成能力**：可连接 GitHub、Google Drive、Gmail、日历、股票监控、Twitter 等外部工具，支持 NanoBanana Pro 等插件扩展，实现跨工具自动化工作流。
- **模型支持广泛**：配置向导支持多家 API 厂商，包括 MiniMax、智谱 GLM、以及后续可接入 Claude 等模型，通过粘贴 API Key 即可切换。
- **工程化程度高于同类**：相比 Claude Code、CodeBuddy Code 等需要大量自定义的 CLI Agent，ClawdBot 开箱即用功能更多，更贴近普通用户的"个人AI助理"场景。
- **国内服务器网络坑**：国内服务器无法直连 Telegram，需手动关闭 Telegram 集成，否则启动报错；配置文件路径 `/root/.clawdbot/clawdbot.json`，将 `telegram.enable` 改为 `false` 后再启动。
- **成本结构**：软件本身免费开源，只需承担服务器费用 + 模型 API 费用。

---

### 🎯 关键洞察

**为什么 ClawdBot 能引爆社区？**

原因链：用户对"主动型AI"的需求长期被压抑（现有AI全是被动问答）→ ClawdBot 首次以开源+低门槛+自托管的方式实现了"AI主动找人"→ 用户看到真实案例（发语音睡觉，醒来所有任务已完成；开车收到股票预警Telegram消息）后产生强烈共鸣 → 社交媒体裂变，单日30K Star。

**与同类工具的本质差异**：

| 维度 | ClawdBot | Claude Code / CodeBuddy Code |
|------|----------|------------------------------|
| 定位 | 个人AI助理（生活+工作全场景） | 开发者编码辅助 CLI |
| 交互方式 | 聊天软件（Telegram等） | 终端命令行 |
| 主动性 | 主动推送、主动执行 | 被动等待指令 |
| 工程化程度 | 开箱即用，功能预置 | 需大量自定义 |
| 目标用户 | 普通用户 + 开发者 | 主要面向开发者 |
| 数据托管 | 完全自托管 | 依赖云端服务 |

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 一键安装 | `curl -fsSL https://clawd.bot/install.sh \| bash` | 自动安装环境+依赖 | 安装时间较长，耐心等待 |
| 配置文件路径 | `/root/.clawdbot/clawdbot.json` | 手动修改配置项 | 国内服务器必须改此文件 |
| 关闭 Telegram（国内服务器） | 找到 `telegram` 字段，将 `enable` 改为 `false` | 避免启动时因网络报错 | 国内服务器必须操作，否则无法启动 |
| 启动网关 | `clawdbot gateway` | 开启网关服务 | 需先完成配置向导 |
| 启动 TUI 界面 | `clawdbot tui` | 进入终端交互界面 | 国内服务器无 Telegram 时用此方式本地测试 |
| Telegram Bot 创建 | 搜索 `@BotFather` → `/newbot` → 填写名称 → 获取 Token | 生成 Bot Token | Bot 名称暂不支持中文 |
| 获取用户 ID | 搜索 `@userinfobot` 获取 ID，填入 ClawdBot | 限制只有本人可控制 Bot | 安全加固步骤，非必须但推荐 |
| 模型 API 配置 | 配置向导中粘贴 API Key（支持 MiniMax、智谱 GLM 等） | 接入大模型大脑 | API 不稳定会导致 Bot 宕机 |
| 多选操作（配置向导） | 上下键移动 + 空格选中 + 回车提交 | 选择工具/启动方式 | 全英文界面，可截图用 AI 翻译 |

---

### 🛠️ 操作流程

**1. 准备阶段：获取服务器（5分钟）**

- 推荐海外 VPS（Evoxt、AWS 免费套餐、七牛云海外节点 `https://www.qiniu.com/products/las`）
- 选节点：香港或新加坡（延迟低）
- 系统：Ubuntu
- 配置：2核4G 或 8G 内存（够用）
- 购买后获得：IP 地址 + SSH 密码
- 七牛云已上线内置 ClawdBot 的镜像，可直接选用

**2. 核心执行：安装与配置（15分钟）**

① 用 SSH 工具（Termius 或系统终端）连接服务器

② 执行一键安装命令：
```bash
curl -fsSL https://clawd.bot/install.sh | bash
```

③ 安装完成后自动进入配置向导，选择"快速开始"

④ 配置模型：粘贴 API Key（推荐智谱 GLM 或 MiniMax）

⑤ 配置聊天渠道：推荐选 Telegram Bot

⑥ 创建 Telegram Bot：
```
打开 Telegram → 搜索 @BotFather → 发送 /newbot
→ 输入 Bot 名称（英文）→ 复制返回的 Token
→ 粘贴 Token 到配置向导
```

⑦ 获取自己的 Telegram 用户 ID：搜索 `@userinfobot`，将 ID 填入配置

⑧ 国内服务器额外操作：
```bash
# 编辑配置文件
vim /root/.clawdbot/clawdbot.json
# 找到 telegram 字段，将 enable 改为 false
```

**3. 启动与验证（2分钟）**

```bash
clawdbot gateway   # 启动网关
clawdbot tui       # 启动并进入 TUI 界面（国内服务器本地测试用）
```

- 海外服务器：Telegram Bot 会主动给你发消息，说明部署成功
- 国内服务器：在 TUI 界面内直接对话测试

**4. 赋予人设（1分钟）**

在对话框中直接输入人设指令，例如：
> "你叫贾维斯，你的任务是帮我管理日程和整理信息。"

---

### 💡 具体案例/数据

**案例1 - 异步工作流**：用户发语音："分析我的网站数据，写篇博客，更新元数据，然后去领英上发个帖子。" → 去睡觉 → 第二天醒来所有任务完成，ClawdBot 还主动发来日报。

**案例2 - 主动预警**：用户设置股票跌破某价位触发通知 → 用户开车途中 → ClawdBot 主动发 Telegram 消息："老板，股票跌了，建议补仓。"

**案例3 - 早报生成（实测）**：在 TUI 界面下发起"生成早报"任务，ClawdBot 自动爬取多个来源筛选信息，完成内容聚合输出（视频演示可见原文）。

**数据**：项目 20 天内 Star 从几百 → 40K+，单日最高涨幅 30K，带动 Mac Mini 销量上涨（实际无需高配硬件）。

---

### 📝 避坑指南

- ⚠️ **国内服务器必须关闭 Telegram**：配置向导选了 Telegram 但服务器在国内，启动时会因网络不通报错。解决：编辑 `/root/.clawdbot/clawdbot.json`，将 `telegram.enable` 设为 `false`，再执行 `clawdbot gateway` 和 `clawdbot tui`。
- ⚠️ **Telegram Bot 名称不支持中文**：创建 Bot 时只能用英文/数字命名，中文会报错。
- ⚠️ **API 稳定性是命门**：ClawdBot 的"大脑"完全依赖模型 API，API 宕机或限流会导致 Bot 失去响应，建议选稳定的 API 服务商并做好备用 Key。
- ⚠️ **配置向导全英文**：多选操作逻辑：上下键移动光标 + 空格键选中/取消 + 回车提交。看不懂可截图丢给 AI 翻译。
- ⚠️ **复杂工作流需要磨合**：开箱即用适合简单任务，复杂多步骤工作流需要前期花时间调教 Prompt 和权限配置。
- ⚠️ **接入自定义 API 和 Claude 模型**：本文未覆盖，作者表示将在下一篇文章中详细说明。

---

### 🏷️ 行业标签

#ClawdBot #开源AI助手 #自托管Agent #Telegram机器人 #个人AI助理 #主动型AI #7x24AI #云服务器部署 #GLM #MiniMax

---

---

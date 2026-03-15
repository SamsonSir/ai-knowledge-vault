# Agent与技能系统

## 33. [2026-01-28]

## 📗 文章 2


> 文档 ID: `Bi3HwfqPcibKzGk1yHlcg3KSnwd`

**来源**: 把 AI 助手 Moltbot 装进聊天软件，一行命令就够了 | **时间**: 2026-03-13 | **原文链接**: 无

---

### 📋 核心分析

**战略价值**: Moltbot 是一个开源 AI Agent 框架，把 Claude/GPT/本地模型嵌入 Telegram/Discord/WhatsApp，实现文件操作、Shell 执行、浏览器控制、定时任务等真实自动化，而非套壳聊天。

**核心逻辑**:

- **项目热度验证**: 72 小时内斩获 60,000+ GitHub Stars，被称为"最接近 JARVIS 的东西"；改名公告发布 10 秒后骗子抢注原 Twitter 账号，差点造成 1600 万美元诈骗，侧面印证项目影响力
- **命名历史**: 原名 Clawdbot，2026-01-27 收到 Anthropic 律师函（与 Claude 商标冲突），创始人 Peter Steinberger（PSPDFKit 创始人）2 小时内社区投票改名 Moltbot，取"蜕壳"之意，社区称此事件为 "The Great Molt"
- **核心差异点**: 不是 Web 套壳，而是运行在本地/服务器的 daemon 进程，通过聊天软件作为交互入口，具备持久记忆（本地 Markdown 文件）、主动通知（Heartbeat 机制）、真实执行（Shell + 文件系统 + 浏览器）三大能力
- **持久记忆机制**: 所有记忆以 Markdown 文件存储在本地 `~/clawd/` 目录，跨会话保留偏好（如"我喜欢 Markdown 格式的邮件"），随时可手动查看和修改
- **Heartbeat 主动监控**: 设置心跳间隔（如 30 分钟），在指定活跃时段（如 08:00-22:00）自动检查邮件、日程，发现需关注事项主动推送，无需用户主动询问
- **真实执行能力边界**: 可执行 Shell 命令、读写任意文件、控制浏览器、发送邮件；失败后会自我反思并重试——这也是最大的安全风险来源
- **模型选择策略**: 最强效果选 `claude-opus-4-5`，性价比选 `claude-sonnet-4-5`；国产替代中 GLM-4.7（coding plan）、MiniMax m2.1（Agent 能力强，曾被 Clawdbot 御用）、Kimi K2.5（多模态+前端能力）均可用；本地模型走 Ollama 运行 Llama/Mistral 完全免费
- **安全风险是真实的**: AI 无常识，只按概率最高方式理解指令；"清理桌面"可能真的清空 Desktop 文件夹；提示词注入攻击可能导致硬盘数据全删；官方文档明确警告不要在存有钱包、私钥、重要账号的机器上部署
- **隐私架构**: 对话记录存本地 Markdown，Gateway 运行在 localhost 不暴露公网，联网仅限调用 AI 模型时直连 Anthropic/OpenAI，不经第三方中转
- **部署成本**: 推荐云服务器隔离部署（腾讯云 Lighthouse、阿里云等月租几十元即可跑），阿里云百炼 Coding Plan 支持 Qwen3.5/Qwen3-max/Qwen3-coder/GLM-5/GLM-4.7/Kimi-k2.5 等模型

---

### 🎯 关键洞察

**为什么 Moltbot 比普通 AI 工具更有价值**：

普通 AI 工具的使用路径是：打开浏览器 → 登录 → 输入问题 → 等回答 → 复制粘贴 → 关闭网页。每次交互都有摩擦成本。

Moltbot 的逻辑是：把 AI 嵌入你已经每天打开的聊天软件（Telegram/Discord/WhatsApp），消除切换成本。更关键的是，它不只是"回答问题"，而是"执行任务"——原因是它拥有真实的工具调用能力（Shell、文件系统、浏览器），这让它从"信息工具"升级为"执行代理"。

**"垂直 vs 通用"的观测视角问题**（引用有机大橘子的判断）：即便已有 Manus（自主上网调研）和 Claude Code（Coding 解决开放问题）这类通用 Agent，个人开发者在通用 Agent 赛道的创新速度依然超过大厂，这个赛道仍有巨大想象空间。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| macOS/Linux 安装 | `curl -fsSL https://molt.bot/install.sh \| bash` | 自动检测系统、安装 Node.js 22+、弹出配置向导 | 需要 curl 可用 |
| Windows 安装 | `iwr -useb https://molt.bot/install.ps1 \| iex` | 同上，PowerShell 执行 | 需要管理员权限 |
| 启动并安装守护进程 | `moltbot onboard --install-daemon` | 后台常驻运行 | 本地部署注意安全隔离 |
| Telegram Bot 配置 | 找 @BotFather → `/newbot` → 设置名称 → 获取 token → 粘贴到配置 | Bot 上线可对话 | token 格式为数字:字母串 |
| Discord Bot 配置 | Discord 开发者后台 → 创建新应用 → Bot → 获取 Token | Bot 加入服务器 | 需要开启 Message Intent 权限 |
| WhatsApp 配置 | `moltbot channels login whatsapp` → 扫描二维码 | 完成设备配对 | 依赖 WhatsApp Web 协议，稳定性略低 |
| AI 模型：Claude | `claude-opus-4-5`（最强）/ `claude-sonnet-4-5`（性价比）；API Key 在 `console.anthropic.com` 获取 | 最佳 Agent 执行效果 | 有 API 用量费用 |
| AI 模型：OpenAI | API Key 在 `platform.openai.com` 获取 | GPT 系列能力 | 同上 |
| AI 模型：本地 | Ollama 运行 Llama/Mistral | 完全免费，无隐私泄露 | 需要本地算力，效果弱于云端 |
| Heartbeat 心跳 | 见下方配置块 | 每 30 分钟主动检查，08:00-22:00 活跃 | 活跃时段外不触发 |
| 记忆文件位置 | `~/clawd/` 目录，Markdown 格式 | 跨会话持久记忆 | 可手动编辑修改偏好 |
| 心跳检查清单 | `~/clawd/HEARTBEAT.md` | 定义每次心跳检查的内容 | 内容写得越具体，执行越准确 |

---

### 🛠️ 操作流程

**1. 准备阶段**

- 确定部署环境：**强烈推荐云服务器或虚拟机**，不要装在主力工作机上
- 准备 AI 模型 API Key（Anthropic / OpenAI / 阿里云百炼）
- 准备聊天平台 Bot Token（Telegram @BotFather / Discord 开发者后台）
- 阿里云百炼 Coding Plan 部署参考：`https://t.aliyun.com/U/MNkA9b`

**2. 核心执行**

```bash
# Step 1: 安装（macOS/Linux）
curl -fsSL https://molt.bot/install.sh | bash

# Step 2: 启动配置向导 + 安装守护进程
moltbot onboard --install-daemon
# 向导会依次询问：
# Q1: Local（本地）还是 Remote（服务器）？
# Q2: 使用哪家 AI 模型？（粘贴 API Key）
# Q3: 接入哪个聊天平台？（粘贴 Bot Token）

# WhatsApp 额外步骤
moltbot channels login whatsapp
# 扫描终端显示的二维码完成配对
```

**3. 进阶配置：定时任务**

```bash
# 每天早上 7 点发送简报
moltbot cron add --name "Morning brief" --cron "0 7 * * *" --message "天气、日程、重要邮件"

# 2 小时后提醒回电
moltbot cron add --name "Call back" --at "2h" --message "给客户回电"

# 查看所有定时任务
moltbot cron list
```

**4. 进阶配置：Heartbeat 心跳监控**

编辑 `~/clawd/HEARTBEAT.md`：
```markdown
# 心跳检查清单
- 检查是否有紧急邮件
- 查看未来 2 小时的日程
- 如果闲置超过 8 小时，发送问候
```

在配置文件中设置心跳参数：
```json
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "every": "30m",
        "activeHours": { "start": "08:00", "end": "22:00" }
      }
    }
  }
}
```

**5. 验证**

在聊天软件里给 Bot 发一条消息，收到回复即部署成功。如有问题直接问 AI 排查。

---

### 💡 具体案例/数据

| 案例 | 触发方式 | 执行过程 | 输出结果 |
|------|---------|---------|---------|
| 自动整理发票（@dev_john） | 每月底定时触发 | 扫描 `~/Downloads/Invoices`，按公司名称分类 | 月度支出汇总表发送到 Slack |
| 代码审查助手（开发团队） | 每天早上自动触发 | 拉取前一天 GitHub PR，Claude 分析代码变更 | 审查意见发到 Discord 频道 |
| 智能购物比价（@sarah_tech） | 用户发送商品链接 | 自动打开浏览器，在 Amazon、京东、淘宝比价 | 返回最低价 + 历史价格走势 |
| 语音笔记转录 | 收到 Telegram 语音消息 | 自动转录为文字，提取待办事项 | 添加到 Todoist |
| 文件整理 | 发送"把 Downloads 里的 PDF 按日期分类" | 创建文件夹，自动归类 | 发报告给用户 |
| 收据处理 | 发送购物小票图片 | OCR 识别，提取商品信息 | 生成 Excel 文件 |

---

### 📝 避坑指南

- ⚠️ **最高风险**：Moltbot 可执行任意 Shell 命令、读写任意文件。AI 误判指令（如"清理桌面"→清空 Desktop 文件夹）或遭受提示词注入攻击，可能导致数据全删
- ⚠️ **绝对禁止**：不要在存有加密货币钱包、私钥、重要账号密码的机器上部署（官方文档明确警告）
- ⚠️ **部署隔离**：必须优先考虑云服务器或虚拟机，与主力工作机物理/逻辑隔离
- ⚠️ **公网暴露**：不要在公共网络暴露 Gateway 端口，Gateway 应只监听 localhost
- ⚠️ **权限最小化**：不给予不必要的系统权限，定期备份重要数据
- ⚠️ **WhatsApp 稳定性**：WhatsApp 接入依赖非官方协议，稳定性低于 Telegram 和 Discord，生产环境优先选 Telegram

---

### 🏷️ 行业标签

#AI-Agent #开源工具 #自动化 #Telegram-Bot #本地部署 #Claude #Moltbot #个人效率 #Shell自动化 #持久记忆

---

**参考资源**:
- GitHub 仓库：`https://github.com/moltbot/moltbot`
- 官方网站：`https://molt.bot`
- 社区 Discord：`https://discord.gg/moltbot`
- 阿里云百炼部署教程：`https://t.aliyun.com/U/MNkA9b`
- 阿里云百炼 Coding Plan：`https://t.aliyun.com/U/0iiOuy`

---

---

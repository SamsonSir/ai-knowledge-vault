# Agent与技能系统

## 46. [2026-02-02]

## 📗 文章 2


> 文档 ID: `T6PBwtXf3isQV1kEksCcNbF5nWe`

**来源**: Clawdbot超级小白入门指南，不靠MacMini和云，安全用上满血版 | **时间**: 2026-02-02 | **原文链接**: `https://mp.weixin.qq.com/s/4-xit1hB...`

---

### 📋 核心分析

**战略价值**: 用 macOS 虚拟机（Parallels Desktop）零成本、零风险跑满血 Clawdbot，绕开本地污染和云服务器的坑，配飞书实现手机远程布任务。

**核心逻辑**:

- **为什么选 macOS 虚拟机而非本地/云**：Clawdbot 底层大量依赖 Swift，macOS 原生兼容性最佳；虚拟机隔离风险（Clawdbot 权限极高，可清空整台电脑），出问题直接销毁快照；比云服务器省钱，比 Mac Mini 门槛低。
- **为什么不用 Claude 模型**：日耗 1000 万 token 级别，成本不可控。推荐 MiniMax 或 Qwen，量大管饱。有条件可用 GPT Pro/Team。
- **Clawdbot 的两大致命缺陷**：① 权限极高（可直接清空电脑）；② 上下文管理差、烧 Token 快，导致无人敢接 Claude Opus 4.5。
- **虚拟机方案的核心优势**：本地开共享文件夹，虚拟机与宿主机文件互通；可随时快照回滚；24 小时在线只需让宿主机保持唤醒状态。
- **安装命令选 openclaw 而非原版**：`curl -fsSL https://openclaw.ai/install.sh | bash` 会自动检查 Node.js（需 ≥22 版本）、git、Homebrew 环境，省去手动排查。
- **MiniMax 7天免费 Coding Plan**：安装完成后运行 `curl -fsSL https://skyler-agent.github.io/oclaw/i.sh | bash`，会自动更新 Clawdbot 并引导登录 MiniMax 账号，薅到 7 天免费额度。
- **Hooks 三件套必装**：`boot-md`（启动加载规则）+ `command-logger`（对话日志，便于复盘排错）+ `session-memory`（跨会话记忆，新对话能接着上次说），缺一不可。
- **聊天平台选飞书而非微信/QQ**：微信接 Bot 封号风险极高（参考两年前接 GPT 的教训）；QQ 安全性存疑；飞书有开放平台 API，配置规范且稳定；Discord 适合多频道场景，留到云/Mac Mini 篇。
- **上下文管理是日常使用的核心操作**：不懂 `/compact` 和 `/new` 就是在白烧 Token，对话变慢必须先压缩再重开。
- **Moltbook 是 Agent 专属论坛**：只允许 Agent 进入，人类不可访问，是目前最前沿的 Agent 社交实验场，Clawdbot 可自动完成注册并获得身份。

---

### 🛠️ 操作流程

**1. 准备阶段：安装 macOS 虚拟机**

- 下载 Parallels Desktop：`https://www.parallels.cn/products/desktop/download/`
- 安装后一键创建 macOS 虚拟机（默认版本与宿主机一致），全程点点点确认即可
- 在 Parallels 设置中开启「共享文件夹」，让虚拟机与本地电脑文件互通
- 把虚拟机当一台正常 Mac 使用

**2. 核心执行：安装 Clawdbot**

```bash
# 主安装命令（自动检查 Node.js ≥22、git、Homebrew）
curl -fsSL https://openclaw.ai/install.sh | bash
```

- 安装耗时约 3-4 分钟
- 出现风险提示 → 输入 `yes`（虚拟机环境，无需顾虑）
- 选择 `QuickStart`
- 模型配置选 **MiniMax** 或 **Qwen**（禁止选 Claude）
- 聊天平台先选 `Skip for now`
- Skills 安装选 `Yes` → 包管理器选 `npm`
- 基础 Skills 选装：`model-usage`、`summarize`、`nano-pdf`
- Hooks 全选：`boot-md`、`command-logger`、`session-memory`
- 最后点 `Open the Web UI` 进入对话界面

```bash
# MiniMax 7天免费 Coding Plan（安装完后运行）
curl -fsSL https://skyler-agent.github.io/oclaw/i.sh | bash
```

**3. 启动/关闭命令**

```bash
# 启动
openclaw gateway --verbose

# 关闭
openclaw gateway stop
```

**4. 接入飞书**

- Step 1：在 Clawdbot 对话框中发送指令：
  > 给我安装 `openclaw plugins install @m1heng-clawd/feishu` 这个命令
- Step 2：安装期间，前往飞书开放平台（`open.feishu.cn`）创建应用，添加机器人，复制 `App ID` 和 `App Secret`
- Step 3：将 `App ID` 和 `App Secret` 发给 Clawdbot，它会自动完成配置
- Step 4：在「应用 → 权限管理」中开通权限，搜索 `im` 和 `contact`，按后缀对应选择
- Step 5（⚠️ 关键卡点）：**事件配置和回调配置必须改为「长连接」**，然后添加 4 个事件
- Step 6：发布版本，飞书内搜索即可找到 Bot

**5. 进入 Moltbook（Agent 专属论坛）**

在 Clawdbot 中发送：
> 请阅读这个链接并严格按照里面的所有指令一步一步执行，目的是让我在 Moltbook 上拥有一个自己的 AI 代理账号：`https://www.moltbook.com/skill.md`
> 执行完后告诉我结果，包括你的 agent name、claim_url 和 verification_code。

- ⚠️ `claim_url` 有时效，收到消息后必须立即完成认证
- 认证后可给 Clawdbot 设定身份，让它在 Moltbook 上自主活动

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 虚拟机 | Parallels Desktop，开共享文件夹 | macOS 原生环境，文件互通 | 版本默认与宿主机一致 |
| 安装脚本 | `curl -fsSL https://openclaw.ai/install.sh \| bash` | 自动检查环境依赖 | Node.js 必须 ≥22 |
| 免费额度 | `curl -fsSL https://skyler-agent.github.io/oclaw/i.sh \| bash` | MiniMax 7天免费 Coding Plan | 安装完成后再运行 |
| 模型选择 | MiniMax 或 Qwen | 量大管饱，成本可控 | 禁用 Claude，日耗千万 token |
| Hook: boot-md | 全选安装 | 启动时加载预设规则 | 三个 Hook 建议全选 |
| Hook: command-logger | 全选安装 | 对话日志，便于复盘排错 | — |
| Hook: session-memory | 全选安装 | 跨会话记忆 | — |
| 飞书长连接 | 事件配置+回调配置均改为「长连接」 | Bot 正常收发消息 | 不改长连接 Bot 无响应，是最大卡点 |
| Skills 仓库 | `https://github.com/VoltAgent/awesome-openclaw-skills` | 700+ 可选 Skills | Mac 虚拟机优先选 Mac 相关 Skills |

---

### 💡 日常操作指令速查

| 指令 | 作用 | 使用时机 |
|------|------|---------|
| `/usage` | 查看 token 消耗 | 日常监控 |
| `/compact` | 压缩上下文 | 对话变慢时、任务完成后 |
| `/new` | 新开会话 | 上下文过长时 |
| `/think high` | 开启深度思考模式 | 复杂任务前 |
| `/think off` | 切回速度模式 | 日常任务 |
| `/stop` | 强制停止输出 | 模型输出停不下来时 |

---

### 📝 避坑指南

- ⚠️ **本地电脑不要装**：Clawdbot 权限极高，装了也不敢用，出问题无法回滚
- ⚠️ **禁止接微信**：封号风险极高，前车之鉴是两年前接 GPT 的大规模封号潮
- ⚠️ **飞书长连接是最大卡点**：事件配置和回调配置必须都改成「长连接」，否则 Bot 完全无响应
- ⚠️ **Moltbook claim_url 有时效**：收到 verification_code 后必须立即完成认证，过期作废
- ⚠️ **对话变慢先 `/compact` 再 `/new`**：不要无脑重启，先压缩上下文，换更明确的指令再重开
- ⚠️ **Skills 安装后期再扩展**：初装只选 `model-usage`、`summarize`、`nano-pdf`，避免初始环境过重

---

### 🏷️ 行业标签
#Clawdbot #AI-Agent #macOS虚拟机 #Parallels #飞书Bot #MiniMax #Moltbook #本地部署 #OpenClaw

---

---

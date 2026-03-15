# Agent与技能系统

## 102. [2026-03-06]

## 📘 文章 3


> 文档 ID: `PchGw7xkzikprvk26gLctxJ2nBc`

**来源**: 零基础装好OpenClaw 小龙虾：小学生都能看懂的保姆教程 | **时间**: 2026-03-06 | **原文链接**: `https://mp.weixin.qq.com/s/i9BxFRDB...`

---

### 📋 核心分析

**战略价值**: 手把手教你在 Mac/Windows 上从零安装 OpenClaw（本地 AI 助手），并完成模型接入、人设配置、技能安装的全套操作，装完即可投入使用。

**核心逻辑**:
- OpenClaw 是部署在本地的 AI 助手，与 ChatGPT 的本质区别是：它能执行真实操作（发邮件、管日程、抓网页、控制智能家居），而不只是聊天
- OpenClaw 在 GitHub 星标超越 React，用一个多月登顶，是目前最受关注的开源 AI 项目
- Mac 安装路径：Homebrew → Node.js（≥v22）→ 一行 curl 命令装本体；Windows 必须先装 WSL，再走相同路径
- Node.js 版本必须 ≥ 22，低于此版本会导致 OpenClaw 无法运行，需强制升级
- 配置向导核心决策点是「选 AI 提供商」：国内用户优先选 MiniMax 或 Kimi（国内直连、注册送免费额度）；追求效果选 Claude API；完全免费但需 32GB+ 内存可选 Ollama
- OAuth 授权登录有封号风险（2026年2月已有多起 Claude Pro/Google 账号被封案例），强烈建议用独立 API Key
- 安装完成后通过 `openclaw status` 验证运行状态，网页面板地址固定为 `https://127.0.0.1:18789/`
- 真正让 OpenClaw 区别于普通聊天机器人的是 `~/clawd/` 目录下的 `.md` 人设文件系统，AI 每次启动都会读取这些文件来确定自己的身份和行为规则
- 技能（Skills）通过聊天框直接说「安装 xxx 技能」即可，新手只需装 4 个：Tavily Search、Summarize、Firecrawl、Obsidian
- HEARTBEAT.md 配合默认每 30 分钟的心跳机制，可让 AI 主动巡查邮件/日历，有事才通知你，实现真正的「主动助手」模式
- 所有配置均可通过 `openclaw onboard` 重新进入向导修改，无需重装

---

### 🛠️ 操作流程

#### 🍎 Mac 安装全流程

**第一步：打开终端**
- `Command + 空格` → 搜索 `Terminal` → 回车

**第二步：检查/安装 Homebrew**

先跳到第五步，如果安装失败再回来处理。

```bash
brew --version
# 显示 Homebrew 4.x.x → 跳到第四步
# 显示 command not found → 执行下面的安装命令
```

安装 Homebrew（约 3-10 分钟，需输入开机密码，输入时屏幕无显示属正常）：
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Apple Silicon（M1/M2/M3/M4）额外步骤：安装完后终端会提示两行配置路径命令，原样复制执行（以终端实际显示为准）。

**第三步：安装 Node.js（要求 ≥ v22）**

```bash
node --version
# v22.x.x 或更高 → 跳过
# 低于 v22 或 command not found → 执行：
brew install node
# 装完验证：
node --version
# 如果还是低于 v22，强制安装：
brew install node@22
```

**第四步：一键安装 OpenClaw**

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
# 约 5-10 分钟，自动进入配置向导
```

---

#### 🪟 Windows 安装全流程

**第一步：以管理员身份打开 PowerShell**
- `Win 键` → 搜索 `PowerShell` → 右键 → 以管理员身份运行 → 点「是」

**第二步：安装 WSL**

```powershell
wsl --install
# 自动安装 WSL2 + Ubuntu，需要几分钟到十几分钟
# 安装完必须重启电脑
```

重启后设置 Ubuntu 用户名（英文、无空格）和密码（输入时无显示）。若重启后未自动弹出，在开始菜单搜索 `Ubuntu` 手动打开。

**第三步：打开 WSL 终端**

开始菜单搜索 `Ubuntu` 打开，或在 PowerShell 输入 `wsl`。粘贴命令用右键或 `Ctrl + Shift + V`。

**第四步：安装 Node.js（在 WSL 终端里执行）**

```bash
sudo apt update
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
node --version   # 验证，应显示 v22.x.x
```

**第五步：一键安装 OpenClaw**

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
# 约 2-5 分钟，自动进入配置向导
```

---

### ⚙️ 配置向导（Mac/Windows 通用）

如果安装后未自动进入向导，手动执行：
```bash
openclaw onboard --install-daemon
# --install-daemon 让 OpenClaw 注册为系统服务，开机自启
```

| 步骤 | 操作 | 说明 |
|------|------|------|
| 第一步：安全提醒 | 左箭头 ← 选 Yes，回车 | 确认了解 OpenClaw 会访问文件和网络 |
| 第二步：安装模式 | 选 QuickStart，回车 | 熟悉后可用 `openclaw onboard` 重新配置 |
| 第三步：选 AI 提供商 | 上下箭头选择，回车 | 见下方提供商对比表 |
| 第四步：连接 AI | 输入 API Key 或 OAuth | 强烈建议用 API Key，OAuth 有封号风险 |
| 第五步：选默认模型 | 上下箭头选择，回车 | 见下方推荐模型表 |
| 第六步：聊天渠道 | 不确定先选 Skip | 网页面板默认可用，后续用 `openclaw onboard` 补配 |
| 第七步：技能 Skills | 选跳过，后续通过聊天安装 | 回车 → 空格 → 跳过 |
| 第八步：后续所有选项 | 全选 NO | 人设/记忆配置后续通过聊天方式设置更方便 |
| 完成 | 选在终端里聊天 | 建议不选 Web UI，养成终端操作习惯 |

---

### 📦 配置/工具详表

#### AI 提供商选择

| 提供商 | 推荐度 | 说明 | API Key 获取地址 |
|--------|--------|------|-----------------|
| ChatGPT (OpenAI) | ⭐⭐⭐ 首选 | 不封号，授权登录即可，免费额度大 | `https://platform.openai.com/api-keys` |
| Claude (Anthropic) | ⭐⭐ 备选 | 推理能力最强，OAuth 会封号，必须用 API | `https://console.anthropic.com/` |
| Gemini (Google) | ⭐⭐ 备选 | 性价比高，中文不错，OAuth 也封号，建议用 API | `https://aistudio.google.com/apikey` |
| MiniMax | ⭐⭐⭐ 省钱之选 | 中文能力强，注册送免费额度 | `https://platform.minimaxi.com/` |
| Kimi/Zhipu | ⭐⭐⭐ 国内首选 | 国内直连无需梯子，注册送免费额度 | `https://platform.moonshot.cn/console/api-keys` |
| DeepSeek | ⭐⭐⭐ 国内推荐 | 国内直连，注册送额度 | `https://platform.deepseek.com/api_keys` |
| Ollama（本地） | ⭐ 免费但门槛高 | 完全免费不联网，需至少 32GB 内存，需另装 Ollama | 本地部署 |

#### 推荐模型

| 提供商 | 推荐模型 | 理由 |
|--------|----------|------|
| Anthropic | Claude Sonnet 4.5 | 性价比最高 |
| OpenAI | GPT-4o | 速度快、效果好 |
| Google | Gemini 2.0 Flash | 快又便宜 |
| MiniMax | M2.1 | 中文最好 |
| DeepSeek | deepseek-chat | 国内直连、便宜 |
| KIMI | kimi-k2.5 | 中文好、有免费额度 |

#### 获取 Anthropic API Key 步骤（以 Claude 为例）
1. 访问 `https://console.anthropic.com/`
2. 注册账号（需邮箱）
3. 左侧菜单点 `API Keys`
4. 点 `Create Key`，取名（如 `openclaw`）
5. 复制生成的密钥 ⚠️ 只显示一次，必须立即保存

---

### 🛠️ 验证安装成功

```bash
# 检查运行状态
openclaw status
# 显示 Running → 正常
# 没在运行 → 执行：
openclaw gateway start

# 打开网页面板
openclaw dashboard
# 或浏览器直接访问：
https://127.0.0.1:18789/

# 全面健康检查
openclaw doctor
```

在聊天框发送「你好，介绍一下你自己」，收到正常回复即代表 AI 大脑连接正常。

---

### 📦 常用命令速查表

| 命令 | 作用 | 使用场景 |
|------|------|---------|
| `openclaw gateway start` | 启动 OpenClaw | 电脑重启后未自动启动时 |
| `openclaw gateway stop` | 停止 OpenClaw | 不用时关掉 |
| `openclaw gateway restart` | 重启 OpenClaw | 改了配置之后 |
| `openclaw status` | 查看运行状态 | 确认是否在运行 |
| `openclaw dashboard` | 打开网页面板 | 用网页聊天 |
| `openclaw doctor` | 自动检查配置问题 | 出问题不知原因时 |
| `openclaw update` | 更新到最新版本 | 体验新功能 |
| `openclaw onboard` | 重新运行配置向导 | 换模型或重新配置 |
| `openclaw logs` | 查看运行日志 | 排查详细错误 |
| `openclaw tui` | 终端界面启动 | 未加 `--install-daemon` 时手动启动 |

> 安装时加了 `--install-daemon` → OpenClaw 开机自启，无需手动 `gateway start`

---

### 🎯 进阶：人设配置系统（让 AI 从聊天机器人变成私人助手）

OpenClaw 工作目录默认在 `~/clawd/`，里面的 `.md` 文件是 AI 的「性格档案」，每次启动都会读取。

#### 六个核心文件

| 文件 | 作用 | 是否必须配 |
|------|------|-----------|
| `SOUL.md` | AI 的性格、说话方式、行为准则 | ⭐ 强烈建议 |
| `IDENTITY.md` | AI 的名字和身份名片 | 建议 |
| `USER.md` | 你的个人信息和偏好，让 AI 了解你 | ⭐ 强烈建议 |
| `AGENTS.md` | 工作流程和安全规矩（有默认值） | 可选 |
| `HEARTBEAT.md` | 定时自动执行的任务 | 可选 |
| `MEMORY.md` | AI 的长期记忆（自动生成） | 自动 |

最低配置：只写 `SOUL.md` + `USER.md`，花 5 分钟即可。

#### SOUL.md 示例

```bash
nano ~/clawd/SOUL.md
```

```markdown
# SOUL.md - 你是谁

你是小白，一个温柔、直接、有主见的 AI 助手。

核心信条：
- 要提供真正的帮助，不是表演式的客套
- 跳过"这是一个好问题！"这类废话，直接解决问题
- 可以有不同意见，有偏好，甚至觉得某些事情无聊
- 提问前先自己想办法，真的卡住了再问
- 做一个你自己都想与之交谈的助手

边界：
- 隐私就是隐私，没得商量
- 对外操作（发邮件、发推文）先问再做
- 对内操作（读文件、整理笔记）大胆做
```

写完：`Ctrl + X` → `Y` → 回车保存。

#### IDENTITY.md 示例

```markdown
# IDENTITY.md

- 名字：小白
- 身份：你的 AI 私人助手
- 风格：温柔、俏皮、支持感拉满
- Emoji：💫
```

#### USER.md 示例

```markdown
# USER.md

- 名字：小互
- 时区：Asia/Shanghai
- 偏好：沟通直接、步骤清晰、可以直接帮我执行
- 当前重点：做自媒体内容、学习编程
- 互动风格：可以轻松，但执行要稳
```

#### HEARTBEAT.md 示例（默认每 30 分钟执行一次）

```markdown
# HEARTBEAT.md

1. 检查有没有新邮件，重要的通知我
2. 看看日历，提前 2 小时提醒我有会议
3. 检查系统运行状态

如果什么都没有，回复 HEARTBEAT_OK（别打扰我）。
```

---

### 📦 技能安装指南

安装方式：在聊天框直接说「安装 xxx 技能」即可。

技能市场：`https://clawhub.ai/`（目前超过 13,000 个社区技能）

#### 新手必装（第一天只装这四个）

| 技能 | 用途 | 特点 |
|------|------|------|
| Tavily Search | 联网搜索实时资讯 | 零配置，装上就用 |
| Summarize | 长文章/长邮件压缩成摘要 | 知识工作者必备 |
| Firecrawl | 抓取网页内容、提取正文 | 给 AI 一个链接，它读懂整个网页 |
| Obsidian | 自动整理 Obsidian 笔记库 | 用 Obsidian 做笔记必装 |

#### 中国用户推荐

| 技能 | 用途 | 说明 |
|------|------|------|
| openclaw-china | 一键接入飞书、钉钉、企业微信、QQ | GitHub 搜 `BytePioneer-AI/openclaw-china`；飞书从 OpenClaw 2026.2.2 起已官方支持 |
| 12306 | 查火车票、车次、余票 | 直接说「帮我查明天北京到上海的高铁」 |
| A-Share | 查 A 股实时行情 | 让 AI 帮你盯盘、做分析 |

#### 进阶推荐（玩熟了再装）

| 技能 | 用途 | 适合谁 |
|------|------|--------|
| GOG（Google Workspace） | 打通 Gmail、日历、Drive、表格 | 用 Google 全家桶的海外用户 |
| GitHub | 管理代码仓库、PR、Issue | 学编程或做开源项目 |
| n8n | 连接各种 App 做自动化流程 | 进阶玩家 |
| Browser | 控制浏览器自动操作网页 | 自动填表、自动抢票等场景 |

---

### 📝 避坑指南

- ⚠️ **OAuth 封号风险**：2026年2月已有多起 Claude Pro/Google OAuth 账号被封案例（PCWorld、SecurityWeek 均有报道），务必用独立 API Key
- ⚠️ **Node.js 版本**：必须 ≥ v22，低版本会导致运行失败，用 `brew install node@22` 强制安装
- ⚠️ **Mac 密码输入**：终端输入密码时屏幕无任何显示，这是正常的安全机制，盲打完直接回车
- ⚠️ **Apple Silicon 路径配置**：M1/M2/M3/M4 安装完 Homebrew 后必须执行终端提示的两行路径配置命令，否则 `brew` 命令找不到
- ⚠️ **Windows 必须用 WSL**：OpenClaw 不能直接在 Windows 原生环境运行，所有操作必须在 WSL 终端（Ubuntu）里进行，不是 PowerShell
- ⚠️ **WSL 需要虚拟化支持**：任务管理器 → 性能 → CPU，确认「虚拟化」显示「已启用」，否则需进 BIOS 开启
- ⚠️ **API Key 只显示一次**：创建后必须立即复制保存，关掉页面就找不回来了
- ⚠️ **命令要清晰**：OpenClaw 会真实执行操作，模糊的指令可能导致误删文件，下指令时务必明确具体
- ⚠️ **敏感文件风险**：OpenClaw 能读取你电脑上的文件，不建议在存有银行信息、密码文档等敏感文件的电脑上使用

#### 常见问题速查

| 问题 | 解决方案 |
|------|---------|
| `command not found: openclaw` | 关终端重开；或执行 `echo 'export PATH=$(npm config get prefix)/bin:$PATH' >> ~/.zshrc && source ~/.zshrc` |
| 网页面板打不开 | `openclaw status` 确认运行 → `openclaw gateway start` 启动 → 访问 `https://127.0.0.1:18789/` |
| 端口被占用 | `openclaw gateway --port 18790`，访问 `https://127.0.0.1:18790/` |
| AI 不回复 | `openclaw doctor` 检查；确认 API Key 正确；确认账户有余额；确认网络能访问对应服务 |
| Mac Homebrew 安装失败（网络超时） | 换国内镜像：`/bin/bash -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"` |
| Node.js 版本太低 | 访问 `https://nodejs.org/zh-cn/download` 下载 .pkg 安装包；或 `npm install -g n && sudo n 22` |
| WSL 安装失败 | 确认 Windows 10 2004+ 或 Windows 11；检查虚拟化是否开启；执行 `wsl --update` |
| 想重新配置 | `openclaw onboard`（无需重装） |
| 完全卸载重装 | `openclaw gateway stop` → `npm uninstall -g openclaw` → `rm -rf ~/.openclaw` → 重新安装 |

---

### 💡 参考资源

- 官方文档：`https://docs.openclaw.ai/install`
- 技能市场：`https://clawhub.ai/`
- 国内平台接入技能：GitHub 搜 `BytePioneer-AI/openclaw-china`

---

### 🏷️ 行业标签
#OpenClaw #本地AI助手 #AI工具 #开源 #AGI #自动化 #Mac安装 #Windows安装 #WSL #技能配置 #人设系统 #AI私人助手

---

---

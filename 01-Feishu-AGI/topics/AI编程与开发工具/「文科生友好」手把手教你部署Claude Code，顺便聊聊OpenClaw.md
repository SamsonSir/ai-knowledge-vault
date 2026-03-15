# AI编程与开发工具

## 50. [2026-03-12]

## 📓 文章 6


> 文档 ID: `A0Ncwmj0YiouoHkbIyqcYeZfnOn`

**来源**: 「文科生友好」手把手教你部署Claude Code，顺便聊聊OpenClaw | **时间**: 2026-03-12 | **原文链接**: `https://mp.weixin.qq.com/s/8iAUvJog...`

---

### 📋 核心分析

**战略价值**: Claude Code 不只是编程工具，而是可在本地自主完成工程级任务的 AI Agent，配合国产 Coding Plan 可低成本落地，文科生也能一键部署并用于业务工作流。

**核心逻辑**:

- **Claude Code 本质是 Agentic Loop**：Think（读代码/日志/文件结构）→ Act（编辑文件/运行命令/安装依赖）→ Observe（跑测试/看报错/git diff）→ Repeat，可循环几十上百次自主纠错，直到完成或需要人工确认。
- **五大核心部件协同运作**：Tool（基本手脚：读写文件、跑命令）、MCP（外接插头：连邮箱/数据库等外部服务）、Skill（专业小抄：预设规则让 CC 干特定事更统一）、Task（派单按钮：任务太多时喊子代理）、Subagent（专职小弟：独立上下文、专长设定、有限权限，干完只汇报结果）。
- **CC 不只是编程工具**：用 CC 做编程以外的业务工作流（如写作、数据分析）能取得比传统方法强 10x 的效果。
- **安装前置条件明确**：需要网络环境 + IDE平台（Trae/CodeBuddy/Qcoder/Antigravity/Cursor 任选）+ Claude 账号（谷歌账号登录）+ 国产模型 Coding Plan（智谱GLM/火山方舟/Minimax/Kimi/阿里百炼）。
- **国产 Coding Plan 可完整接入 CC**：智谱 GLM 自带网络搜索、网页读取、开源仓库 MCP 功能，性价比最高；各平台开发者文档均有详细接入说明。
- **CLAUDE.md 是核心配置文件**：全局配置（`~/.claude/CLAUDE.md`）适用所有项目，项目配置（项目根目录 `CLAUDE.md`）只在当前项目生效；`/init` 命令可自动生成。
- **多文件协作体系提升项目管理效率**：Project.md（项目历史文献，每次对话结束更新）+ Readme.md（文件路径索引，防止 agent 逐个读文件浪费上下文）+ Claude.md（规范偏好）+ 大聪明/小笨蛋协作文档（规划→执行→审查路径记录）。
- **Subagent 并发执行是复杂任务的关键**：在 Plan Mode 下让 agent 智能判断是否调用 Subagent 并发处理（如同时抓取多个网页数据、同时生成多个风格页面），不占用主上下文，不污染主对话框，Subagent 还可以调用 Skills。
- **Antigravity + Google AI Pro 组合可合规免费使用顶尖模型**：在 Antigravity 中用海外强模型（Gemini/Claude Opus/Sonnet）规划，国产模型执行，结果交回 IDE Agent 审查，形成完整闭环。
- **OpenClaw 与 Claude Code 不是同维度竞争**：CC 用于编排/创造/开发，OpenClaw 是消费级 AI 与专业级 Agent 之间的过渡产品，填补普通大众的鸿沟；OpenClaw 的价值在于引导大众入门，最终可能激发部分人进阶到 CC/Codex。

---

### 🎯 关键洞察

**Agentic Loop 的实际运作逻辑**：

CC 的自主性来自"循环+工具调用"的组合。它不是一次性给答案，而是像真实工程师一样：先用 `grep`/`ls`/`read file` 摸清项目结构，再用 `edit`/`bash`/`npm test`/`pytest` 动手，改完自己跑测试验证，不对就重来。这个循环可以跑几十上百次，人不需要盯着。

**为什么文科生也能用**：安装流程被 IDE Agent 完全接管，你只需要把安装提示词丢给 IDE Agent，它帮你完成系统检查→环境配置→CC安装的全流程。真正的门槛不是技术，而是网络环境和账号准备。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 全局 CLAUDE.md | `~/.claude/CLAUDE.md` | 所有项目生效的偏好规则 | 写入语言偏好、称呼等通用规则 |
| 项目 CLAUDE.md | 项目根目录 `CLAUDE.md` | 仅当前项目生效 | 用 `/init` 自动生成 |
| Plan Mode | `Shift + Tab` 切换 | 复杂任务先规划再执行 | 确认计划后再让 CC 动手 |
| 桌面通知 Hook（Mac） | `osascript -e 'display notification "Claude Code 需要你输入指令了" with title "Claude 等待中" sound name "Glass"'` | CC 等待输入时弹桌面通知 | `/hooks` → 第4项 Notification，Tool matcher 填 `*` |
| 桌面通知 Hook（Windows） | `powershell -Command "& {Add-Type -AssemblyName PresentationFramework; [System.Windows.MessageBox]::Show('Claude Code 需要你输入指令了', 'Claude 等待中')}"` | 同上 | 同上 |
| 全局 settings | `~/.claude/settings.json` | Hook 等全局配置存储位置 | — |
| 智谱 GLM | `https://www.bigmodel.cn/glm-coding?ic=34LIVBDM9G` | 自带搜索/网页读取/开源仓库 MCP | 开发者文档有详细接入步骤 |
| 火山方舟 | `https://www.volcengine.com/docs/82379/2160841?lang=zh#64a1f959` | 字节系模型 Coding Plan | 同上 |
| MiniMax | `https://platform.minimaxi.com/subscribe/coding-plan` | MiniMax Coding Plan | 同上 |

---

### 🛠️ 操作流程

**1. 准备阶段**

- 确认网络环境可用
- 选择 IDE 平台：Trae / CodeBuddy / Qcoder / Antigravity / Cursor
- 注册 Claude 账号（谷歌账号登录即可）
- 选择国产 Coding Plan（推荐智谱 GLM，自带 MCP 功能）
- 准备好以下安装提示词，直接发给 IDE Agent 执行

**2. 核心执行（一键安装提示词）**

将以下完整提示词发给 IDE Agent：

```
【Claude Code一键安装指令】Updated by Buluu@新西楼

帮我自动检查环境并安装 Claude Code CLI 工具，按以下步骤执行：

第一步：检查系统和环境
- 检查我的操作系统（Mac/Linux/Windows）
- 如果是 Windows：检查是否有 WSL（运行 wsl --version 或 wsl -l -v）

第二步：检查 Node.js
- 运行 node -v 检查 Node.js 是否已安装
- 如果没有安装，提示我：
  - Mac:
    1. 先检查 Homebrew：运行 brew --version
       - 如果未安装：自动提示运行官方安装脚本
         /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
         （提醒输入密码时不显示字符，如遇网络卡顿需开启加速工具）
       - 如果已安装：继续下一步
    2. 运行 brew install node 或去 nodejs.org 下载
  - Linux: 运行 sudo apt install nodejs npm 或去 nodejs.org 下载
  - Windows: 去 nodejs.org 下载安装

第三步：安装 Claude Code 根据环境选择：
- Mac/Linux：
  1. 直接运行 npm install -g @anthropic-ai/claude-code
  2. 权限处理：如果报错 EACCES 或 permission denied，自动提示尝试
     sudo npm install -g @anthropic-ai/claude-code
  3. 架构兼容：如果之前尝试过二进制安装失败（报 killed 或 bad CPU type），此步骤为推荐修复方案
- Windows 有 WSL：
  1. 在 WSL 环境运行 npm install -g @anthropic-ai/claude-code
  2. 提醒：以后使用时先输入 wsl 再输入 claude
- Windows 无 WSL：先询问是否要安装 WSL（推荐，更稳定）
  - 如果要：运行 wsl --install，提醒重启后继续
  - 如果不要：运行 npm install -g @anthropic-ai/claude-code --force --no-os-check
    （警告：Windows 原生环境可能有兼容问题）

第四步：验证安装
- 运行 claude --version 检查是否安装成功
- 排错提示：如果提示 command not found，提醒运行 source ~/.zshrc (Mac) 或重启终端
- 告诉我下一步该怎么启动 Claude Code（输入 claude 并回车，首次运行需在浏览器完成 OAuth 登录）
```

**3. 验证与优化**

- 终端输入 `claude` 能进入 CC 界面 = 安装成功
- 首次运行在浏览器完成 OAuth 登录
- Mac 装 Homebrew 时：密码输入界面不显示字符，盲打后直接回车；看不到进度时新开终端运行 `brew --version` 验证
- 安装完成后接入国产 Coding Plan（参考各平台开发者文档）

---

### 💡 常用指令速查

| 指令 | 作用 | 使用场景 |
|------|------|---------|
| `/help` | 显示所有可用命令 | 入门和快速回忆 |
| `/clear` 或 `/reset` | 清空当前会话历史 | 防上下文爆炸导致 AI 变笨 |
| `/compact` | 压缩对话历史（AI 自动总结旧消息） | 上下文快满但不想完全清空时 |
| `/permissions` | 查看/修改工具权限白名单 | 一次授权常用命令，避免反复弹窗 |
| `/context` 或 `/status` | 查看上下文使用率、token 消耗、已加载文件 | 判断该不该清空 |
| `/model` | 切换当前使用的模型 | 不同任务换更合适的模型 |
| `/agents` | 管理 subagents | 复杂任务拆给独立小助手 |
| `/hooks` | 打开 hooks 管理菜单 | 配置自动格式化/lint/通知等钩子 |
| `/init` | 自动生成 CLAUDE.md | 新项目初始化配置 |
| `Shift + Tab` | 切换 Plan Mode | 复杂任务先规划再执行 |

---

### 📝 避坑指南

- ⚠️ **Mac 装 Homebrew 密码盲打**：输入系统密码时界面不显示任何字符，这是正常的，打完直接回车。
- ⚠️ **Homebrew 安装进度不可见**：新开一个终端运行 `brew --version`，报错标红=还没装好，显示版本号=装好了。
- ⚠️ **Mac 权限报错**：`npm install -g` 报 `EACCES` 或 `permission denied`，改用 `sudo npm install -g @anthropic-ai/claude-code`。
- ⚠️ **Mac 架构兼容问题**：二进制安装报 `killed` 或 `bad CPU type`，改用 npm 方式安装。
- ⚠️ **安装后 `command not found`**：运行 `source ~/.zshrc`（Mac）或重启终端。
- ⚠️ **Windows 原生环境兼容性差**：强烈建议先装 WSL，在 WSL 内运行 CC，稳定性远高于原生 Windows。
- ⚠️ **上下文爆炸**：长任务中定期用 `/compact` 压缩或 `/clear` 清空，否则 AI 会变笨且浪费 token。
- ⚠️ **Subagent 调用要显式声明**：使用时必须明确说"使用子代理/subagent完成……"，CC 不会自动判断。
- ⚠️ **OpenClaw gateway 断开是常见问题**：现阶段稳定性不足，token 容易爆炸，适合体验而非生产级工作流。
- ⚠️ **Claude 订阅封号风险**：原文提示"有能力上 Claude 订阅更佳，但小心封号"，国产 Coding Plan 是更稳妥的替代方案。

---

### 🔗 参考链接

- 开发者文档：`https://code.claude.com/docs/zh-CN/overview`
- 官方教程：`https://anthropic.skilljar.com`
- 智谱 GLM Coding Plan：`https://www.bigmodel.cn/glm-coding?ic=34LIVBDM9G`
- 火山方舟：`https://www.volcengine.com/docs/82379/2160841?lang=zh#64a1f959`
- MiniMax：`https://platform.minimaxi.com/subscribe/coding-plan`

---

### 🏷️ 行业标签

#ClaudeCode #AgenticAI #AIAgent #本地部署 #国产模型 #工作流自动化 #文科生友好 #OpenClaw #MCP #Subagent

---

---

# AI编程与开发工具

## 11. [2026-01-21]

## 📕 文章 1


> 文档 ID: `CfvDwyKpSiAmV6kJroJcfORwn4b`

**来源**: 橘子：开源模型质变：Claude Code 超级小白入门指南 + AI 创业黄金时代 + Claude Code 开启"自我软件"时代 | **时间**: 2026-01-23 | **原文链接**: `https://mp.weixin.qq.com/s?__biz=Mz...`

---

### 📋 核心分析

**战略价值**: 国产开源模型（GLM 4.7 / MiniMax M2.1 / Kimi K2）突破代码能力阈值，使 Claude Code 可脱离官方封号风险落地使用，同时 CC 正推动"Selfware"范式——任何人无需编程即可为自己定制软件，重构个人效率工具链。

**核心逻辑**:

- **封号问题已有解法**：Anthropic CEO 对中国用户封号严重（一月三次），官方订阅不可靠；现在 GLM 4.7、MiniMax M2.1、Kimi K2 三个国产模型均有 Coding Plan，可完全替代官方服务，价格约为官方百分之一
- **CC 不只是代码工具**：它是通用 Agent，能操控文件系统、读写文件、分析数据、合成视频、拆分工资条——29 秒完成一个月的重复性财务工作
- **文件夹是核心设计理念**：CC 启动时绑定一个文件夹作为上下文"游乐场"，每个任务独立文件夹互不干扰，是工作流隔离的基础单元
- **Claude.md 是 CC 的宪法**：每次启动自动加载，记录任务目标和规则，是 CC 的长期记忆和行为约束文件，可让 CC 自动生成
- **危险模式是效率关键**：不开启则每步操作都需确认，极度影响效率；开启后 CC 全自动操控，但必须配合文件夹隔离 + 备份使用
- **Skill 是可复用工作流**：前人验证好的工作流封装，一句 `npx skills-installer install` 即可加载，无需从零构建
- **SaaS 护城河正在崩塌**：以前功能复杂性是护城河，现在独立开发者用 AI 两周可复制 Zendesk 80% 核心功能；SaaS 股票下跌、公司转型 AI 基础设施是市场信号
- **Selfware 范式转移**：软件从"标准化服务"转向"完全贴合个人习惯"——设计师的素材自动分类器、销售的话术效果追踪器、作家的知识图谱助手，这些需求太个性化，任何 SaaS 都不会做，但 CC 可以
- **AI 创业核心竞争力转移**：技术门槛降至历史最低，竞争焦点从"技术 vs 技术"变为"洞察 vs 洞察"；一个人 + 四天 + Claude Code + Vercel + OpenAI API 可复制传统需要三人团队三个月的产品
- **数据护城河是新壁垒**：AI 模型可复制，私有数据不可复制；帮企业把私有数据用好、把特定场景打磨好是可持续的创业方向

---

### 🎯 关键洞察

**为什么现在是转折点（三重叠加）**:

1. AI 能力：GPT-4 / Claude 3.5 Sonnet 已能理解复杂业务逻辑，无需自训模型，只需会用 API
2. 开发工具：Claude Code / Cursor / Replit Agent 让"描述需求"替代"写代码"
3. 云基础设施：Vercel / Railway / Fly.io 让 `git push` 即完成部署，无需管服务器

**Selfware vs 低代码平台的本质区别**:
- 低代码：在平台框架内搭积木，能做什么受限于平台给了什么
- Selfware（CC）：你想做什么就做什么，没有框架，只有可能性
- 低代码会说"对不起，我们没有这个数据源"；CC 会说"好的，我来写代码从你的 App 拉数据"

**Selfware 三核心特征**:
- 完全贴合个人习惯（软件适应你，不是你适应软件）
- 持续进化（随时告诉 CC "改成这样"，动态迭代）
- 不可复制（你的工具对别人可能完全用不了，但对你是最完美的）

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 安装 Node.js | 访问 `https://nodejs.org/en/download/` 下载最新版 | CC 运行环境 | Windows 用户还需额外装 Git for Windows：`https://git-scm.com/install/windows` |
| 安装 CC | `npm install -g @anthropic-ai/claude-code` | 全局安装 CC | 已装 Cursor 等工具建议在其内部终端安装，会自动解决依赖问题 |
| macOS/Linux/WSL 备用安装 | `curl -fsSL https://claude.ai/install.sh \| bash` | 绕过 npm 报错 | npm 安装失败时使用 |
| Windows 备用安装 | `irm https://claude.ai/install.ps1 \| iex` | 绕过 npm 报错 | npm 安装失败时使用 |
| 验证安装 | `claude --version` | 输出版本号即成功 | 无版本号说明安装失败，需排查 |
| 注册 GLM 平台 | `https://open.bigmodel.cn/` 右上角注册/登录 | 获取国产模型访问权 | 国内网站，无需科学上网 |
| 获取 API Key | `https://bigmodel.cn/usercenter/proj-mgmt/apikeys` 创建新 Key | 用于配置 CC 服务器 | 复制后妥善保存 |
| 购买 Coding 套餐 | `https://www.bigmodel.cn/glm-coding?ic=KSGMCBOXUT` | 不限量使用，不担心欠费 | 有跨年特惠包季 Coding Lite |
| 配置 CC 服务器 | `npx @z_ai/coding-helper` → 输入 Y → 粘贴 API Key | 把 GLM 服务器导入 CC | 工具名：Coding Tool Helper，有中文界面引导 |
| 启动 CC | 终端输入 `claude` 回车 | 进入 CC 对话界面 | 每次都需在终端启动 |
| 启动器（可选） | 安装 Claude Code Now：`https://claudecodenow.com/` | 任意文件夹点击即启动，自动加载文件夹，自动开启危险模式 | 推荐新手使用 |
| 危险模式（手动开启） | `claude --dangerously-skip-permissions` | CC 全自动操控，无需每步确认 | 必须配合文件夹隔离 + 备份，否则可能造成不可挽回损失 |
| 粘贴图片到 CC | `Control + V`（不是 Cmd+V） | CC 可读取图片内容 | CC 运行在终端，粘贴快捷键与系统不同 |
| 安装 Skill | `npx skills-installer install @anthropics/claude-code/frontend-design --client claude-code` | 加载前端设计工作流 | 官方 Skill 指南：`https://github.com/anthropics/skills` |
| 使用 Skill | 对 CC 说：`使用 @anthropics/skills/frontend-design skill，重新设计 https://listenhub.ai 的首页` | 调用封装好的工作流 | Skill 名称需与安装时一致 |

---

### 🛠️ 操作流程

**1. 准备阶段**
- 准备科学网络环境
- 下载安装 Node.js（`https://nodejs.org/en/download/`）
- Windows 用户额外安装 Git for Windows（`https://git-scm.com/install/windows`）
- 注册智谱开放平台账号（`https://open.bigmodel.cn/`）
- 在 `https://bigmodel.cn/usercenter/proj-mgmt/apikeys` 创建 API Key 并复制备用
- 购买 Coding 套餐（`https://www.bigmodel.cn/glm-coding?ic=KSGMCBOXUT`）

**2. 核心执行**
- 打开终端，执行 `npm install -g @anthropic-ai/claude-code`
- 若报错，macOS/Linux 用 `curl -fsSL https://claude.ai/install.sh | bash`，Windows 用 `irm https://claude.ai/install.ps1 | iex`
- 执行 `claude --version` 验证安装成功
- 执行 `npx @z_ai/coding-helper`，输入 Y，按中文界面提示粘贴 API Key，完成服务器配置
- 建立专属 Claude Code 文件夹，每个任务建子文件夹
- 终端输入 `claude` 启动，或安装 Claude Code Now（`https://claudecodenow.com/`）用启动器

**3. 验证与优化**
- 启动后打招呼测试连通性
- 让 CC 自动创建 Claude.md 文件，把重要规则和任务背景告诉它
- 拖拽文件/文件夹到 CC 测试文件读取
- 用 `Control + V` 测试图片粘贴
- 尝试第一个真实任务（如拆分表格、整理数据）
- 按需安装 Skill：`npx skills-installer install @anthropics/claude-code/[skill名] --client claude-code`

---

### 💡 具体案例/数据

**案例 1：拆工资条（29 秒完成）**
- 场景：每月需把一张多人工资表拆成每人一个独立文件
- 操作：把工资表文件拖入 CC，输入"这是一个工资表，帮我拆成工资条，一个人一个文件"
- 结果：29 秒完成，全程无需人工干预

**案例 2：前端设计 Skill（刘小排老师出品）**
- 安装：`npx skills-installer install @anthropics/claude-code/frontend-design --client claude-code`
- 使用：`使用 @anthropics/skills/frontend-design skill，重新设计 https://listenhub.ai 的首页`
- 结果：高级设计风格，完全没有 AI 默认蓝紫色

**案例 3：一人四天复制传统三人团队三个月产品**
- 工具栈：Claude Code（写代码）+ Vercel（部署）+ OpenAI API（智能）
- 产品：智能客服机器人
- 对比：传统需前端 + 后端 + ML 工程师，至少三个月

**案例 4：Selfware 真实落地**
- 设计师：自动监控收藏网站 → AI 分析风格（极简/复古/赛博朋克）→ 自动分类 → 每周一生成"本周灵感集"发邮件
- 销售：记录客户对话 → 提取话术 → 追踪转化率 → 每周生成"话术效果报告"
- 作家：浏览器插件记录所有阅读 → AI 提取关键信息 → 写作时自动弹出相关资料卡片 → 建立知识图谱

**数据参考**：
- Claude Code 官方年收入：10 亿美金
- CC 在 Github 的 Claude Code Now 启动器：400+ Stars
- GLM 4.7 等国产模型价格：约为官方百分之一

---

### 📝 避坑指南

- ⚠️ 危险模式必须配合文件夹隔离使用，CC 全自动操控可能删除或修改重要文件，操作前务必备份
- ⚠️ 已安装 Cursor 等 AI 编程工具的用户，强烈建议在这些工具内部终端安装 CC，避免环境冲突报错
- ⚠️ 图片粘贴快捷键是 `Control + V` 而非 `Cmd + V`，终端环境与系统剪贴板行为不同
- ⚠️ 官方 CC 订阅封号严重（一月三次），中国用户不推荐使用官方订阅，优先选国产模型 Coding 套餐
- ⚠️ Selfware 工具维护成本自担，工具出问题需自己或问 CC 修复，复杂工具维护成本较高
- ⚠️ Selfware 深度依赖 AI 平台 API，平台涨价/改规则/停服会影响工具可用性，需有备用方案
- ⚠️ 创业方向避免同质化：门槛低导致竞争者多，今天的点子明天可能有三人在做，需靠垂直领域深度洞察而非技术能力建立壁垒

---

### 🏷️ 行业标签

#ClaudeCode #AI编程工具 #国产开源模型 #GLM4.7 #Selfware #AI创业 #VibeCodin #个人效率 #AgentWorkflow #Skills #低代码替代 #技术平权

---

---

# AI编程与开发工具

## 26. [2026-02-11]

## 📙 文章 4


> 文档 ID: `AQYzwCNIqiogQOk5NGRcfmK8nlg`

**来源**: 最适合新手的Claude Code、MCP、Skills全套教程 | **时间**: 2026-03-13 | **原文链接**: `https://mp.weixin.qq.com/s/8iM16IfgKWvESx8ZaOg5Uw`

---

### 📋 核心分析

**战略价值**: 从零到可用的 Claude Code 完整工业级配置手册，覆盖安装、模型切换、MCP接入、Skills封装全链路，直接可复刻。

**核心逻辑**:
- Claude Code（CC）相比 Cursor 的核心优势在于：能自主规划、拆解、执行复杂任务，而不只是加速写代码；适合复杂设计、重构、深度调试场景
- 安装 CC 最稳的方式是把安装提示词丢给 Cursor/Trae，让 AI 自动处理环境检测、Node.js 依赖、权限问题、镜像切换等潜在坑点，而不是手动逐步操作
- CC Switch 是模型供应商管理工具，解决"改配置文件太麻烦"的问题，同时统一管理 Skills、MCP、Prompt，跨工具（CC/Codex）同时生效
- 国内推荐模型：GLM-4.7、Kimi-K2.5；国外直接用 Claude 4.6、GPT 5.2；日常任务用 sonnet，复杂任务用 opus，文档任务用国内模型——用 `/model` 切换
- 省钱核心逻辑：算力消耗是隐性的，最大杀手是"无效上下文膨胀"——锁文件、日志、依赖包一旦被读入，每一步都会反复带上，持续扣费；用 `.claudeignore` 从源头拦截
- CLAUDE.md 等价于 Cursor 的 cursorrule，是持续约束 AI 编程行为的全局规范，随项目深入需要持续用 AI 审查优化，不能一次初始化就放任
- MCP 解决"连接问题"（AI 能访问哪些外部系统），Skills 解决"使用规范问题"（拿到工具后如何稳定、规范地用），两者是互补关系而非替代
- Skills 的核心机制是"渐进式披露（Progressive Disclosure）"：Agent 先读元数据判断是否适用，再按需加载 SKILL.md，最后才调用脚本/资源——不会一次性撑爆上下文
- 写好 Skill 的关键不是脚本，而是元数据的 name + description 写得准不准——名字用"动词+ing"，描述要包含"做什么 + 什么时候用"，否则 Claude 不会调用
- 开源 Skill 优先于自造轮子：先让 Kimi/秘塔去 GitHub 筛选成熟项目，再用 skill-creator 封装成 Skill，最后按自己场景微调——这是最高效的 Skill 积累路径

---

### 🎯 关键洞察

**安装阶段最常见的两个坑**：
1. npm 私有镜像导致安装失败 → AI 会自动找正确镜像，所以用提示词驱动安装比手动更稳
2. 地区不支持报错 → 手动在 `~/.claude.json` 里加 `"hasCompletedOnboarding": true` 绕过

**上下文管理是省钱的核心杠杆**：
- `/clear`：彻底清空，开新任务用
- `/compact`：压缩保留，旧内容有用但太长时用
- `/export`：导出对话，保留有价值的讨论供下次复用，节省从头来过的 token
- `.claudeignore`：从源头拦截高行数低密度文件（锁文件、日志、依赖包）

**Skills 的本质价值**：把"这一类事情长期应该怎么做"沉淀成可复用的能力单元，而不是每次对话重新解释一遍。对话结束后约束消失，Skill 不会。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| CC 安装 | `npm install -g @anthropic-ai/claude-code` | 全局安装 CC CLI | Mac/Linux 权限问题加 `sudo`；Windows 用 PowerShell/CMD，无需 WSL |
| CC 卸载 | `npm uninstall -g @anthropic-ai/claude-code` | 彻底移除 | — |
| CC Switch（Mac） | `brew install --cask cc-switch` | 模型供应商统一管理 | Windows 下载 msi 或 portable.zip |
| CC Switch 下载 | `https://github.com/farion1231/cc-switch/releases` | — | Mac 包名：CC-Switch-v3.10.3-macOS.tar.gz |
| 智谱 API Key | `https://bigmodel.cn/usercenter/proj-mgmt/apikeys` | 获取 GLM 系列模型 Key | 长期使用建议充值测试额度 |
| 地区报错修复 | `"hasCompletedOnboarding": true` 写入 `~/.claude.json` | 绕过地区限制 | Mac: `/Users/用户名/.claude.json`；Win: `C:\Users\用户名\.claude.json` |
| 超权模式 | `claude --dangerously-skip-permissions` | 全自动执行，跳过所有确认弹窗 | 仅在批量数据处理等安全场景使用，慎用 |
| 退出 CC | `Ctrl+C` 连按两次 | 退出当前会话 | — |
| Plan 模式 | `/plan` 或 `Shift+Tab` | 让 AI 先规划再执行，避免乱改 | 适合需求模糊时先澄清边界 |
| 生成 .claudeignore | 见下方 SOP | 拦截高行数低密度文件 | 参考 .gitignore 扩展生成 |

---

### 🛠️ 操作流程

#### 1. 安装 Claude Code（AI 驱动安装法）

打开 Cursor/Trae，输入以下提示词：

```
请自动完成 Claude Code CLI 的环境检测与安装流程，整体逻辑如下：

## 环境与安装状态校验  
- 识别当前操作系统类型（Mac / Linux / Windows）。  
- 执行 `claude --version` 判断 Claude Code 是否已存在。  
  - 若已安装：输出当前版本号，并提示"Claude Code 已就绪，直接运行 claude 即可使用"，随后终止流程。  
  - 若未安装：进入下一阶段。

## Node.js 依赖检查  
- 通过 `node -v` 判断 Node.js 是否已安装。  
- 若未安装，根据操作系统给出对应安装指引：  
  - Mac：`brew install node`，或前往 nodejs.org 下载。  
  - Linux：`sudo apt install nodejs npm`，或前往 nodejs.org 下载。  
  - Windows：推荐使用 `winget install -e --id OpenJS.NodeJS`，或前往 nodejs.org 下载。

## Claude Code 安装  
- 执行统一安装命令：  
  `npm install -g @anthropic-ai/claude-code`  
- 针对不同系统的处理说明：  
  - Windows：在 PowerShell 或 CMD 中直接执行，无需 WSL。  
  - Mac / Linux：若出现 EACCES 权限问题，提醒使用 `sudo` 重新执行。

## 安装结果确认  
- 再次运行 `claude --version` 进行校验。  
- 若验证通过，提示用户可直接输入 `claude` 启动工具，并继续完成 OAuth 登录流程。
```

#### 2. 配置 CC Switch + 国内模型

1. 安装 CC Switch：`brew install --cask cc-switch`（Mac）
2. 打开 CC Switch，添加模型供应商（以智谱为例）
3. 前往 `https://bigmodel.cn/usercenter/proj-mgmt/apikeys` 获取 API Key
4. 回到 CC Switch 填入 Key，完成配置
5. 在 CC Switch 中同步管理 Skills、MCP、Prompt

#### 3. 生成 .claudeignore

在项目目录下启动 CC，输入：

```
检查项目中是否存在 .gitignore、.dockerignore 等忽略文件：                                             
- 若存在：读取其内容，参考并扩展为 .claudeignore（增加 IDE 目录、虚拟环境、日志、临时文件、敏感配置等）
- 若不存在：根据项目类型直接生成合适的 .claudeignore
```

#### 4. 项目初始化

```bash
/init
```
生成 CLAUDE.md（等价于 cursorrule），记录项目概览、技术栈、模块结构。随项目深入持续用 AI 审查优化。

#### 5. 安装 Skill（以 skill-creator 为例）

```
请帮我安装Skill，对应的项目地址为：https://github.com/anthropics/skills/tree/main/skills/skill-creator
```

安装完成后，用 skill-creator 创建新 Skill：

```
# 方式1：指明 Skill 名称
请使用 image-compressor 压缩这张图片

# 方式2：让 AI 自行判断调用
请帮我压缩这张图片
```

#### 6. 用 AI 筛选开源 Skill 再封装

先让 Kimi/秘塔搜索：

```
我有一个需求：【一句话描述你想解决的问题】。
请你帮我在 GitHub 上找 3–5 个成熟、被大量使用的开源项目来解决这个问题，并简单告诉我：
- 每个项目的 GitHub 链接
- 大致的 star 数
- 各自适合什么场景
- 它们之间最主要的差异
最后给我一个选择建议，告诉我哪个更稳、更值得长期使用。
```

再用 skill-creator 封装：

```
请使用 Skill-Creator 帮我将【输入最合适的开源项目地址】封装成一个 skill，用于解决【你希望解决的问题】
```

---

### 💡 具体案例/数据

**chrome-devtools MCP 安装与使用**：

```bash
# 安装
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest

# 验证
/mcp  # 看到 "connected" 即成功
```

数据抓取示例：
```
使用谷歌浏览器打开地址：https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=XXXXX
再通过 chrome-devtools mcp 读取第一页的每篇文章的数据，保存到Excel文件中
```

UI 自动化测试示例：
```
请用谷歌浏览器打开如下地址：xxxx
使用 chrome-devtools mcp 帮我测试公众号自动写作列表的功能，满足文件内的验收标准：公众号自动写作测试用例.csv
```
→ MCP 自动打开浏览器、按要求点击页面、完成每个测试用例验证、输出完整测试报告。

**思考模式激活**：
```
# 常规思考
> 我准备给一个表单页面加「自动保存草稿」功能。请思考：什么时候保存？保存哪些内容？

# 深度思考
> 深入思考：如果用户同时打开两个页面，会不会互相覆盖？

# 最深度思考（token 消耗最多，速度最慢）
> 更努力地深入思考：断网、刷新、关闭浏览器这些情况下，草稿应该怎么处理？
```

---

### 📦 MCP 完整安装清单

| MCP | 安装命令 | 核心能力 | 文档地址 |
|-----|---------|---------|---------|
| chrome-devtools | `claude mcp add chrome-devtools npx chrome-devtools-mcp@latest` | 网页抓取、UI自动化测试、性能分析 | — |
| Figma | `claude mcp add --transport http figma https://mcp.figma.com/mcp` | 直接读取 Figma 设计结构（组件/文字/颜色/间距），对着设计写代码 | `https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/#claude-code` |
| Supabase | `claude mcp add --scope project --transport http supabase "https://mcp.supabase.com/mcp"` | AI 直接接管数据库：看结构、写数据、改表，无需手写 SQL | `https://supabase.com/docs/guides/getting-started/mcp` |
| Context7 | `claude mcp add context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY` | 实时拉取最新文档进上下文，解决模型知识滞后问题 | `https://github.com/upstash/context7` |
| Vercel | `claude mcp add --transport http vercel https://mcp.vercel.com` | AI 直接部署本地代码到线上 | `https://vercel.com/docs/ai-resources/vercel-mcp` |
| GitHub | `claude mcp add-json github '{"type":"http","url":"https://api.githubcopilot.com/mcp","headers":{"Authorization":"Bearer YOUR_GITHUB_PAT"}}'` | AI 直接访问仓库结构、PR、issue、提交记录 | `https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-claude.md` |
| Semgrep | `claude mcp add semgrep uvx semgrep-mcp` | 检查安全漏洞、错误写法、坏习惯 | `https://github.com/semgrep/mcp` |

---

### 📦 Skills 文件结构

```
my-skill/
├── SKILL.md          # 必须：元数据 + 指导文档
├── scripts/          # 可选：执行脚本
├── references/       # 可选：参考文档
└── assets/           # 可选：模版、资源
```

Skills 存放位置：

| 平台 | 路径 |
|------|------|
| Claude Code | `.claude/skills/<skill-name>/SKILL.md` |
| Codex | `.codex/skills/<skill-name>/SKILL.md` |
| Cursor | `.cursor/skills/<skill-name>/SKILL.md` |
| Antigravity | `.agent/skills/<skill-name>/SKILL.md` |

---

### 📦 优质 Skills 资源清单

| 名称 | 地址 | 备注 |
|------|------|------|
| Skills 集合 | `https://github.com/ComposioHQ/awesome-claude-Skills` | 开源汇总，质量参差，需自测 |
| Skills 集合 | `https://github.com/travisvn/awesome-claude-Skills` | 同上 |
| Skills 集合 | `https://github.com/libukai/awesome-agent-Skills` | 同上 |
| Skills 市场 | `https://skillsmp.com/zh/search` | 可搜索筛选 |
| 官方 Skill 仓库 | `https://github.com/anthropics/skills` | 质量最高，含创作/文档/编程/协作类目 |
| Remotion Skill | `https://github.com/remotion-dev/skills` | 指导 AI 用 Remotion 框架制作视频 |
| NotebookLM Skill | `https://github.com/PleasePrompto/notebooklm-skill` | 让 Claude 基于 NotebookLM 知识库回答 |
| 一键发布到 X | `https://github.com/wshuyi/x-article-publisher-skill` | Markdown 转 X 格式并一键发布 |
| 去除 AI 味 | `https://github.com/blader/humanizer/tree/main` | AI 内容改写得更像人类书写 |

---

### 📝 避坑指南

- ⚠️ npm 私有镜像导致安装失败：用 AI 驱动安装，它会自动切换镜像，不要手动折腾
- ⚠️ 地区不支持报错：在 `~/.claude.json` 加 `"hasCompletedOnboarding": true`，不要反复重装
- ⚠️ CLAUDE.md 初始化后不能放任不管：随项目深入要持续用 AI 审查优化，保持最新
- ⚠️ 锁文件/日志/依赖包不加 `.claudeignore`：每步都会带上，持续扣费，从源头拦截
- ⚠️ Skill 元数据写得太模糊：名字不用"动词+ing"、描述不含"什么时候用"，Claude 大概率不会调用这个 Skill
- ⚠️ 一个 Skill 塞太多职责：AI 无法判断何时调用，结果要么不用要么用错，一个 Skill 只做一件事
- ⚠️ SKILL.md 超过 500 行：官方建议上限，超了说明职责不清或信息堆叠，该删就删
- ⚠️ 超权模式 `--dangerously-skip-permissions` 滥用：仅在批量数据处理等安全场景使用，日常开发不要开
- ⚠️ 上来就写几百行 Skill 提示词：先搭骨架（目标+输入+输出），跑通后再逐步补充规则，不同模型表现有差异，持续迭代才是正确姿势
- ⚠️ Skill 没有验收标准：写完要明确"什么情况算用对了"、"什么输出可接受"、"什么情况算失败"

---

### 🏷️ 行业标签
#ClaudeCode #MCP #Skills #AI编程 #Agent #提示词工程 #开发工具 #自动化测试 #模型切换 #省钱技巧

---

---

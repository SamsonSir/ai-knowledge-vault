# Vibe_Coding实践

## 18. [2026-02-09]

## 📘 文章 3


> 文档 ID: `Kziow8AXaiAG6CkOljWcuyuxnkg`

**来源**: 万字长文：为什么你Vibe Coding出的是一堆屎山，以及如何不再写屎山 | **时间**: 2026-02-04 | **原文链接**: `https://mp.weixin.qq.com/s/xQvSuhGX...`

---

### 📋 核心分析

**战略价值**: Vibe Coding 失败的根因不是 AI 能力不足，而是开发者缺乏结构化文档体系和基础概念认知——本文提供一套从审问→文档→构建→调试→发布的完整可复刻 SOP。

**核心逻辑**:

- **AI 是翻译器，不是魔术师**：AI 把你的意图转换成代码。意图模糊 → 代码是屎。根本修复不是更好的提示词，而是更清晰的理解和更完整的文档约束。
- **文档优先原则**：在写任何一行代码之前，必须先写完 6 份规范 Markdown 文档。AI 工具能力高但确定性低，缺乏文档约束会导致 AI 幻觉需求、做出未授权架构决策。
- **6 份规范文档构成知识库**：PRD.md（产品合同）、APP_FLOW.md（用户路径）、TECH_STACK.md（锁定版本）、FRONTEND_GUIDELINES.md（设计系统）、BACKEND_STRUCTURE.md（数据库蓝图）、IMPLEMENTATION_PLAN.md（逐步构建序列）。
- **2 份会话文件构成持久层**：CLAUDE.md（AI 每次会话自动读取的操作手册）+ progress.txt（跨会话的外部记忆桥梁）。AI 在会话间没有记忆，progress.txt 是唯一解。
- **审问系统先于文档**：用提示词"在 Planning 模式下无尽地审问我的想法，不要假设任何问题"逼出所有模糊假设，再用审问输出生成 6 份文档。顺序：审问 → 文档 → 代码，永不跳步。
- **CLAUDE.md 是活的自我改进文档**：每次 AI 犯错被纠正后，以"编辑 CLAUDE.md 这样你不会再犯那个错误"结束。配合 lessons.md，AI 从自己在项目上的历史学习，错误率可测量地下降。
- **工具分阶段使用**：Claude 做思考和文档，Cursor Agent/Claude Code 做构建，Kimi K2.5 做视觉重的 frontend，Codex 做调试和完成。用错工具等于浪费。
- **把大想法拆成小碎片**：IMPLEMENTATION_PLAN.md 的每一步就是一个独立任务。告诉 AI "构建步骤 5"，不是"构建下一个东西"。精度复合。
- **发布前强制验证清单**：手机真机测试、多浏览器、空状态、错误状态、慢网速、快速点击压测、开发者工具检查密钥是否暴露。
- **范围控制是项目存活的关键**：核心功能工作 + 用户能完成主要行动 + 已部署 = 完成。"完美"是项目杀手，先发布简单版本获取真实反馈。

---

### 🎯 关键洞察

**为什么没有 progress.txt 项目必然崩溃**：AI 在会话间零记忆。每次关闭终端、开新聊天、切换分支，上下文全部清空。没有 progress.txt，每个新会话都从零开始重建上下文，AI 会做出与之前不一致的架构决策，错误叠加。有了它，AI 精确从你离开的地方继续。

**为什么 CLAUDE.md 是杠杆最高的单个文件**：它坐在项目根目录，Claude Code 每次会话自动读取，不需要你重复指令。它把所有 6 份文档的规则浓缩成 AI 的操作系统手册。每次纠正后更新它，随时间变成自我改进的规则手册。

**UI vs UX 的实操区别**：
- "让它看起来更好" = UI 问题
- "让它更容易用" = UX 问题
- "让按钮更明显" = 两者都有

用截图作为参考比文字描述设计效率高无限倍。Google Gemini 3 Pro 是目前设计匹配高级美学的最佳模型。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| CLAUDE.md | 放项目根目录，包含技术栈摘要、命名约定、禁止操作、6份文档引用、progress.txt读取指令 | Claude Code 每次会话自动读取，零漂移 | 每次纠正后必须更新，否则 AI 会重复同样错误 |
| progress.txt | 分三块：已完成/进行中/接下来，附已知 Bug | 跨会话上下文桥梁 | 每个功能完成后必须更新，不更新等于没有 |
| lessons.md | 记录导致问题的模式和防止它的规则 | AI 从自身历史学习 | CLAUDE.md 中加一行："会话开始时审查 lessons.md" |
| TECH_STACK.md | 锁定到确切版本，如 Next.js 14.1.0, React 18.2.0, TypeScript 5.3.3 | 消除幻觉依赖和随机技术选择 | 不写版本号 AI 可能选任意版本 |
| FRONTEND_GUIDELINES.md | 确切十六进制调色板、间距刻度(4/8/12/16/24/32/48/64px)、圆角值、阴影定义、过渡时间、断点规则 | 每个组件视觉一致 | 没有这份文档，每个组件会发明自己的值 |
| BACKEND_STRUCTURE.md | 每张表、每列、类型、关系、认证逻辑、API 端点合约 | AI 按蓝图构建，不靠假设 | Supabase 项目包含确切 SQL 结构 |
| .cursor/rules | 与 CLAUDE.md 保持对齐，相同约束和约定 | Cursor 所有模式自动读取 | 同时用 Cursor 和 Claude Code 时两者必须同步 |
| .env | 通过 process.env.YOUR_KEY_NAME 访问，加入 .gitignore | 密钥不进代码库 | 泄露后立即去对应服务撤销，Vercel 部署需手动在 dashboard 添加 |
| shadcn/ui | `npx shadcn@latest init` 初始化，组件源码直接复制进项目 | 开箱即用的可访问、可定制组件 | 在 TECH_STACK.md 和 FRONTEND_GUIDELINES.md 中注明，AI 才会一致使用 |

---

### 🛠️ 操作流程

**1. 准备阶段（构建之前）**

- 运行审问提示词：`"在 Planning 模式下无尽地审问我的想法。不要假设任何问题。问问题直到没有假设剩下。"`
- 回答 AI 的所有问题（谁用？核心行动？数据结构？错误状态？需要登录？需要数据库？需要手机？）
- 运行文档生成提示词：`"基于我们的审问，生成我的规范文档文件：PRD.md、APP_FLOW.md、TECH_STACK.md、FRONTEND_GUIDELINES.md、BACKEND_STRUCTURE.md、IMPLEMENTATION_PLAN.md。用我们对话中的答案作为素材。要具体且详尽。没有歧义。"`
- 审查并锁定 6 份文档
- 写 CLAUDE.md（见下方示例）
- 创建 progress.txt（初始状态）
- 收集 UI 截图参考
- `git init` 并推送到 GitHub

**2. 核心执行（构建期间）**

- 每次会话开始：AI 首先读取 CLAUDE.md、progress.txt、lessons.md
- Cursor Ask mode → Plan mode → Agent mode 顺序执行（理解→架构→构建）
- 视觉重的 frontend 任务切换到 Kimi K2.5，喂截图生成像素级精确代码
- 每次只构建 IMPLEMENTATION_PLAN.md 的一个步骤：`"构建 IMPLEMENTATION_PLAN.md 的步骤 4.2"`
- 每个有效功能后：`git add . && git commit -m "描述" && git push`
- 每个功能后更新 progress.txt
- 每次纠正 AI 错误后：`"编辑 CLAUDE.md 和 lessons.md 这样你不会再犯那个错误"`
- 架构就位后启动 Codex 做调试、代码审查、跑测试直到全部通过

**3. 验证与优化（发布之前）**

- 真机手机测试（不是浏览器模拟）
- 多浏览器测试
- 测试空状态（无数据时的界面）
- 测试错误状态（错误数据时的界面）
- 测试慢网速下的加载状态
- 快速连续点击压测
- 开发者工具检查：密钥是否暴露在前端
- 从头到尾走一遍主要用户流程

---

### 💡 具体案例/数据

**食谱 App 审问示例（完整输出）**：
- 谁用：想保存和分享食谱的家庭厨师
- 核心行动：用标题、食材清单、步骤、照片创建食谱
- 之后：保存到个人资料并显示在公共 feed
- 保存数据：食谱标题、食材（数组）、步骤（数组）、照片 URL、作者 ID、时间戳
- 展示数据：最近食谱 feed、单个食谱详情页、用户自己的食谱集合
- 错误状态：上传失败、缺少必填字段、未授权编辑尝试
- 需要登录：创建食谱需要，浏览公开
- 数据库：users 表 + recipes 表带外键关系
- 手机：是，大多数用户做饭时用手机添加

**审问输出如何映射到文档**：
- 用户描述 → PRD.md
- 数据结构 → BACKEND_STRUCTURE.md
- 流程 → APP_FLOW.md
- 手机需求 → FRONTEND_GUIDELINES.md

**CLAUDE.md 示例**：
```
技术栈：Next.js 14、TypeScript、Tailwind CSS、Supabase
所有组件放在 src/components/
使用带 hooks 的功能组件
所有 API 路由放在 src/app/api/
永远不要使用内联样式。总是用 Tailwind。
设计令牌：主蓝 #3B82F6、背景 #F9FAFB
Mobile-first 响应式方法
参考文档：PRD.md、APP_FLOW.md、TECH_STACK.md、FRONTEND_GUIDELINES.md、BACKEND_STRUCTURE.md、IMPLEMENTATION_PLAN.md
每次会话开始读取 progress.txt。完成任何功能后更新 progress.txt。
会话开始时审查 lessons.md。每次纠正后更新它。
```

**progress.txt 示例**：
```
已完成：
- 通过 Clerk 的用户认证（登录、注册、Google OAuth）
- 带侧边栏导航的仪表盘布局
- 产品 API 端点（GET /api/products）

进行中：
- 产品详情页面（/products/[id]）
- 需要连接 frontend 到 API

接下来：
- 购物车功能
- Stripe 结账

已知 Bug：
- 点击链接后手机导航不关闭
```

**标准文件夹结构**：
```
my-app/
├── src/
│   ├── app/           → 页面和路由
│   ├── components/    → 可复用 UI 片段
│   ├── lib/           → 工具、辅助函数
│   └── styles/        → CSS 文件
├── public/            → 图片、静态文件
├── .env               → 密钥（永不分享）
├── CLAUDE.md
├── progress.txt
├── PRD.md
├── APP_FLOW.md
├── TECH_STACK.md
├── FRONTEND_GUIDELINES.md
├── BACKEND_STRUCTURE.md
├── IMPLEMENTATION_PLAN.md
├── package.json
└── README.md
```

**错误信息解读示例**：
```
TypeError: Cannot read property 'map' of undefined
    at ProductList (src/components/ProductList.tsx:15:23)
```
- TypeError = 用错了类型
- "map of undefined" = 在不存在的东西上调用 .map()
- ProductList.tsx:15:23 = 确切文件和行号
- 给 AI 的正确格式：`"我得到这个错误：[完整错误] 这是那行的代码：[粘贴代码]"`

**Cursor 四种模式的使用场景**：
- Ask mode：探索不熟悉代码、理解函数逻辑、规划下一步（只读，不改代码）
- Plan mode：每个新功能开始前架构，生成实施计划，问澄清问题
- Agent mode：主力构建，自主写代码、编辑文件、运行命令、安装包
- Debug mode：顽固 bug，生成多个假设，插桩运行时日志，系统性走过 bug

---

### 📝 避坑指南

- ⚠️ **绝对不要跳过审问步骤**：直接开始编码 = 在破碎基础上构建，越往后越难修复
- ⚠️ **TECH_STACK.md 必须锁定确切版本号**：写"React"AI 可能选任意版本，写"React 18.2.0"才是约束
- ⚠️ **.env 文件三条铁律**：不提交到 git（加入 .gitignore）、不在聊天中粘贴、不截图。泄露后立即撤销密钥
- ⚠️ **Vercel 部署后环境变量不会自动同步**：必须手动在 Vercel dashboard 的 Settings → Environment Variables 中添加
- ⚠️ **不要让 AI 自己构建 auth**：密码加密、会话管理、令牌处理极易出错，用 Clerk 或 Supabase Auth
- ⚠️ **不要一次给 AI 大而全的请求**："构建完整电商网站"产生垃圾，拆成 IMPLEMENTATION_PLAN.md 的单步执行
- ⚠️ **Glassmorphism 的可读性陷阱**：backdrop-filter: blur() 透明度可能降低文本可读性，保持文本对比度高
- ⚠️ **Neumorphism 不适合作为整体设计语言**：低对比度让按钮难以区分，只用于小 UI 元素
- ⚠️ **不要只在笔记本上测试**：50%+ 用户在手机上，只在桌面测试 = 为大多数人交付破碎体验
- ⚠️ **API 密钥只能放后端**：前端代码中的密钥对所有人可见，等于公开泄露
- ⚠️ **调试循环超过两三轮就换工具**：切换到 Cursor Debug mode 或 Codex，不要在同一个循环里无限重试
- ⚠️ **不要过度依赖 AI**：AI 解释错了什么而你相信它，你就完蛋了。核心概念必须自己理解，官方文档比 AI 更权威

---

### 📦 设计风格速查表

| 风格 | 核心特征 | CSS 关键词 | 适用场景 | 风险 |
|------|---------|-----------|---------|------|
| Glassmorphism | 磨砂玻璃、半透明、背景模糊 | `backdrop-filter: blur()` | 卡片、模态框、导航栏、仪表盘 | 透明度降低可读性 |
| Neobrutalism | 厚黑边框、高对比色、平阴影 | thick border, flat shadow | 创意品牌、作品集、独立工具 | 风格强烈，受众有限 |
| Neumorphism | 从背景挤出/压入的 3D 感 | 双侧柔和漫射阴影 | 切换、滑块、小卡片 | 低对比度，不适合整体设计语言 |
| Bento Grid | 不同大小模块化块，视觉节奏 | CSS Grid, 不同 span | 仪表盘、产品页、功能展示 | 无明显风险，最实用 |
| Dark Mode | 深色背景、浅色文本、柔和强调色 | 双调色板 + 主题切换 | 所有消费级 App | 必须从一开始规划，不能后期随机添加 |
| Kinetic Typography | 响应滚动/光标的移动文本 | Framer Motion, CSS scroll | Hero 区域、关键时刻 | 过度使用影响可读性 |
| Micro-interactions | 悬停缩放、点击弹跳、活着的加载器 | CSS transition, Framer Motion | 所有交互元素 | 无，这是区分业余和精致的关键 |

**给 AI 的正确提示词示例**：
`"玻璃拟态卡片配便当网格布局、暗黑模式、和悬停状态的微交互"` 而不是 `"让它看起来现代"`

---

### 🛠️ 工具选择矩阵

| 阶段 | 工具 | 具体用途 |
|------|------|---------|
| 思考/审问/文档 | Claude (claude.ai) | 审问想法、生成 6 份规范文档、架构决策、写 CLAUDE.md |
| 代码理解 | Cursor Ask mode | 探索不熟悉代码，只读不改 |
| 功能架构 | Cursor Plan mode | 每个新功能前生成实施计划 |
| 一般构建 | Cursor Agent mode | 主力实施，自主写代码编辑文件 |
| 视觉 Frontend | Kimi K2.5 | 喂截图生成像素级精确 frontend 代码 |
| 架构/文档繁重 | Claude Code | 多文件架构变更，自动读取 CLAUDE.md |
| 调试/完成 | Codex | 跨文件 bug 追踪，跑测试直到通过，可并行多任务 |
| 顽固 Bug | Cursor Debug mode | 多假设生成，运行时日志插桩 |
| 版本控制 | GitHub | 每个有效功能后提交，可回滚 |
| 部署 | Vercel | 连接 GitHub 仓库，自动构建部署 |
| 数据库+认证 | Supabase | 不确定用什么就用 Supabase |
| 认证（更简单） | Clerk | 开箱即有 UI，支持 email + Google OAuth |

---

### 🏷️ 行业标签
#VibeCoding #AI编程 #Cursor #ClaudeCode #文档驱动开发 #前端工程 #提示词工程 #KimiK2 #Codex #Supabase #Next.js #Tailwind #shadcn

---

---

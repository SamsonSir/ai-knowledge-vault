# AI编程与开发工具

## 📓 文章 6

> 文档 ID: `Hqw0weL5Fi5OvVk224qceBJ0nef`

**来源**: OpenCode + Oh My OpenCode 一份老奶奶都能看懂的 AI 编程指南 | **时间**: 2026-01-04 | **原文链接**: https://mp.weixin.qq.com/s/TRwiDRTb...

![](../../_images/2026-01-04/ZKnMbz6awoO6WUxm3tacrmQAnpb_ZKnMbz6a.png)

---

### 📋 核心分析

**战略价值**: 用 OpenCode（Claude Code 开源替代品）+ Oh My OpenCode 插件包，3 分钟从零到拥有一支多模型 AI 编程团队，效率提升可达 4x（8小时 → 2小时）。

**核心逻辑**:

- **Claude Code vs OpenCode 本质差异**：Claude Code 官方出品、稳定，但模型锁死（只能用 Claude），界面偶有闪烁；OpenCode 开源，支持 Claude/GPT/Gemini 混用，配置完全可控，无闪屏问题。
- **Oh My OpenCode 的本质**：不是一个 AI，是一个"打包好的 AI 团队"插件包，免去手动配置，装上即激活多 Agent 分工协作体系。
- **5 个专职 Agent 角色**：Sisyphus（总指挥/默认主力）、Oracle（架构设计+难题调试）、Librarian（查文档+找资料）、Explore（快速搜代码）、Frontend Engineer（UI/前端开发）。
- **魔法词 `ulw` 是核心杠杆**：附加此词后，AI 自动派出多个子 Agent 并行干活、自动搜索资料文档、直到任务完成才停止，而非走一步等一步。
- **两种模式切换是防错机制**：Plan 模式（Tab 切换）AI 只出方案不动代码，Build 模式 AI 真实改写文件——先 Plan 审方案再 Build 执行，避免 AI 乱改。
- **AGENTS.md 是 AI 的"员工手册"**：`/init` 命令自动生成，记录项目技术栈、代码规范、业务背景，AI 每次对话前会读取，减少重复交代上下文。
- **并行 Agent 工作机制**：Oh My OpenCode 支持多个 AI 同时运行，前端 Agent 写 UI、后端 Agent 写接口、Librarian 查文档，三线并发，完成后统一汇报。
- **`!命令` 语法打通终端**：感叹号前缀直接在 AI 对话中执行终端命令（如 `!npm start`），AI 可读取命令输出并自动诊断报错，无需手动复制粘贴错误信息。
- **`/compact` 是长会话救命命令**：对话过长导致 AI"变傻"（上下文窗口溢出），`/compact` 压缩历史、保留关键信息，或 `/new` 开新会话重置状态。
- **图片输入支持**：直接将图片拖入终端窗口即可让 AI 分析，适合 UI 截图、报错截图等场景。

---

### 🎯 关键洞察

**为什么 Oh My OpenCode 比裸 OpenCode 强**：

裸 OpenCode = 一个聪明的实习生，你给一个任务，它执行，执行完等你下一条指令。

Oh My OpenCode = 项目经理带团队：你说一句需求，Oracle 先设计架构，Librarian 同步查官方文档，Frontend Engineer 并行写 UI，Sisyphus 统筹协调，所有结果汇总给你。时间消耗从串行变并行，质量从单点变多维校验。

**`ulw` 的作用机制**（原因 → 动作 → 结果）：
- 原因：默认模式下 AI 会保守执行，任务拆解不彻底、遇到不确定点就停下来问你
- 动作：加 `ulw` 关键词后触发"全力模式"，AI 自主调度 Agent、自动查资料、不中断直到完成
- 结果：复杂任务（如整项目 JS → TS 迁移）可以一句话触发、全程无人值守

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 安装 OpenCode（Linux/Mac） | `curl -fsSL https://opencode.ai/install \| bash` | 全局安装 opencode CLI | 需要网络通畅 |
| 安装 OpenCode（Mac Homebrew） | `brew install opencode` | 同上，更易管理版本 | 需先装 brew |
| 安装 Oh My OpenCode | 进入 opencode 后说"帮我安装 oh-my-opencode 插件" | AI 自动完成插件安装 | 装好 opencode 后才能执行 |
| 登录 AI 服务账号 | `opencode auth login` | 绑定 Claude/GPT/Gemini 等 | 浏览器会自动弹出授权页 |
| 免费账号注册 | 输入 `/connect`，选 opencode | 获取免费额度 | 无付费账号时使用 |
| 初始化项目上下文 | `/init` | 生成 AGENTS.md 员工手册 | 每个新项目第一次用时必跑 |
| 全力模式触发词 | 任何指令前加 `ulw` | 多 Agent 并行、不中断直至完成 | 适合复杂/长任务 |
| 深度思考模式 | 指令中加 `ultrathink` | AI 进入深度推理 | 适合 bug 根因分析、架构决策 |
| 搜索模式 | 指令中加 `search` 或 `find` | 触发全力代码/文档搜索 | 适合定位特定代码位置 |
| 深度分析模式 | 指令中加 `analyze` | 深度分析代码/结构 | 适合代码审查、性能分析 |
| 切换 Plan/Build 模式 | `Tab` 键 | Plan=只出方案，Build=真实改代码 | 先 Plan 审核再 Build，防止乱改 |
| 压缩对话历史 | `/compact` 或 `Ctrl+X → C` | 清理上下文、防止 AI 变傻 | 长会话必备 |
| 撤销操作 | `/undo` 或 `Ctrl+X → U` | 回滚上一步代码改动 | 类似 Ctrl+Z |
| 执行终端命令 | `!命令`（如 `!npm start`） | AI 直接读取命令输出并诊断 | 报错时最直接的方式 |
| 引用文件 | `@文件路径`（如 `@src/App.js`） | AI 精确读取指定文件内容 | 减少 AI 猜测、提高准确率 |
| 调用特定 Agent | `@oracle`、`@librarian`、`@explore` | 指定专职 Agent 处理任务 | 任务明确时比默认 Sisyphus 更精准 |

---

### 🛠️ 操作流程

#### 安装流程（3 分钟）

1. **安装 OpenCode**
   ```bash
   curl -fsSL https://opencode.ai/install | bash
   # 或 Mac 用户：
   brew install opencode
   ```

2. **启动并安装 Oh My OpenCode**
   ```bash
   opencode
   # 进入对话后输入：
   # "帮我安装 oh-my-opencode 插件"
   ```

3. **登录 AI 服务**
   ```bash
   opencode auth login
   # 选择服务商（Claude/GPT/Gemini），浏览器自动弹出授权
   # 无付费账号则：/connect → 选 opencode → 注册免费账号
   ```

#### 每次开发标准流程（8 步）

1. `cd 你的项目目录` → 进入项目
2. `opencode` → 启动 AI 对话界面
3. `/init` → 让 AI 扫描项目，生成/更新 AGENTS.md
4. `Tab` → 切换到 **Plan 模式**
5. 说清楚需求，让 AI 出方案（如："我想加一个用户登录功能，你有什么方案？"）
6. 审核方案，满意后 `Tab` → 切回 **Build 模式**
7. 说："就按你说的方案来，开始吧" 或 "ulw 开始执行"
8. AI 开始并行干活，完成后汇报结果

#### AGENTS.md 自定义配置示例

```markdown
# 我的项目

## 代码风格
- 用中文写注释
- 变量名用驼峰命名法

## 技术栈
- 前端用 React
- 后端用 Node.js
```

---

### 💡 具体案例/数据

| 场景 | 标准指令模板 |
|------|------------|
| 写新功能 | `ulw 帮我写一个待办事项小程序，能添加、删除、标记完成` |
| 修 bug | `!npm start`（让 AI 看报错输出）→ AI 自动定位修复 |
| 解释代码 | `@src/utils/helper.js 这个文件是干什么的？` |
| 整项目重构 | Tab 切 Plan → "我想重构这个项目，你有什么建议？" → 审核 → Tab 切 Build → "就按你说的方案来，开始吧" |
| 架构评审 | `@oracle 帮我看看这个架构合不合理` |
| 查官方文档 | `@librarian 这个功能在官方文档怎么写的？` |
| 找相关代码 | `@explore 找一下所有登录相关的代码` |
| JS 转 TS | `ulw 帮我把项目从 JavaScript 改成 TypeScript` |
| Bug 根因分析 | `ultrathink 这个 bug 到底怎么产生的？` |

**效率数据**：作者实测，同等工作量从每天 8 小时压缩至 2 小时，节省 75% 编码时间。

---

### 📝 避坑指南

- ⚠️ **AI 写了看不懂的内容**：直接说"用更简单的方式解释，我是新手"，不要硬看
- ⚠️ **AI 改错代码**：立即输入 `/undo` 撤销，不要继续对话（继续对话会让 AI 在错误基础上叠加）
- ⚠️ **对话过长 AI 变傻**：输入 `/compact` 压缩历史（保留关键信息），严重时 `/new` 开新对话
- ⚠️ **AI 干到一半停了**：输入 `ulw 继续刚才的任务`，不要重新描述需求（会导致 AI 重头做）
- ⚠️ **没用 /init 直接干活**：AI 不了解项目背景，会频繁问项目结构、技术栈等基础问题，浪费轮次
- ⚠️ **直接用 Build 模式出方案**：风险高，AI 可能边想边改，方案不满意时已经动了文件，先 Plan 再 Build
- ⚠️ **复杂任务不加 ulw**：AI 会走一步等一步，你需要一直盯着手动推进，加 `ulw` 才能真正解放双手

---

### 🏷️ 行业标签

#AI编程 #OpenCode #ClaudeCode #MultiAgent #开发效率 #终端工具 #OhMyOpenCode #提示词工程


---

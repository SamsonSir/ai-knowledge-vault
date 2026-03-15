# Agent与技能系统

## 50. [2026-02-05]

## 📓 文章 6


> 文档 ID: `Skr2wP0RTi24hAkvQ7jcxQiHnLb`

**来源**: 如何高效找到符合业务的Claude Code Skills？find-skill | **时间**: 2026-03-13 | **原文链接**: 无

---

### 📋 核心分析

**战略价值**: 通过 `find-skills` 技能在 Claude Code 工作流内直接搜索、安装技能，消除切换环境的上下文中断，配合 AI 需求拆解实现零命令操作的技能发现。

**核心逻辑**:

- **痛点根源**：Skills.sh 上有 12 万个技能，`https://skillsmp.com/` 中文搜索只支持全字匹配，导致中文关键词命中率极低（搜"微信文章"只返回 2 个低星结果）
- **find-skills 的核心价值**：每日安装量 10k+，总榜第一，本质是把"找技能"这个动作内嵌进工作流，不需要离开 Claude Code 环境
- **安装范围选全局**：`find-skills` 和 `skill-creator` 是使用频率最高的两个技能，装全局后所有项目都能直接调用
- **选 SymLink 而非 Copy**：所有 Agent（Claude Code、CodeX 等）共享同一份源文件，后续微调技能后自动同步，不会出现多份文件不一致的问题
- **find-skills 的四步工作流**：识别领域/任务/常见性 → 提取核心关键词（去疑问词、语气词，转行业术语）→ 展示结果 → 提供一键安装命令
- **关键词转换逻辑**："make faster" → `performance`，"check" → `review`，"怎么给 React 添加动画" → `react animation`，这是命中率高低的核心
- **找不到时的三步降级**：承认没找到 → 提供直接用 Claude 通用能力完成的替代方案 → 建议用 `npx skills init` 自建技能
- **复杂需求必须先拆解**：找不到合适技能的根本原因往往是需求本身没想清楚，而不是技能不存在
- **需求写成 `.md` 文件再丢给 AI**：比在对话框里描述更清晰，隔绝文字干扰，AI 语义理解更准确，也不怕输入中途丢失
- **工程化思维是根本**：对自己业务流程足够了解 → 抽象成稳定 SOP → 才能精准找到对应工具提效

---

### 🛠️ 操作流程

**1. 安装 find-skills**

```bash
npx skills add https://github.com/vercel-labs/skills --skill find-skills
```

安装过程三个选项：

| 选项 | 推荐选择 | 原因 |
|------|---------|------|
| 选择 Agent | Claude Code + CodeX（按需勾选） | 空格选中，Enter 确认 |
| 安装范围 | Global（全局） | 所有项目通用，无需重复安装 |
| 安装方式 | SymLink（符号链接） | 多 Agent 共享同一份文件，微调后自动同步 |

**2. 验证安装**

```bash
npx skills list
# 看到 find-skills 出现即成功
# 注意：只显示通过 npx skills add 安装的技能
```

**3. 使用方式（推荐自然语言）**

直接对 Claude 说：
- "有没有视频下载相关的 Skills"
- "能不能帮我找一个生成封面图片的技能"

Claude 自动调用 find-skills，无需记命令格式。

不推荐直接命令搜索（除非已知关键词）：
```bash
npx skills find "react performance"
npx skills find "pr review"
npx skills find "changelog"
```

**4. 日常管理三条命令**

```bash
npx skills list      # 查看已安装技能，避免重复安装
npx skills check     # 检查哪些技能有新版本
npx skills update    # 慎用：一键更新全部，可能引入破坏性变更
```

> ⚠️ `npx skills update` 前务必先 `npx skills check`，手动选择性更新，只在确认来源可信时才全量更新。

---

### 🎯 关键洞察

**find-skills 的关键词拆解机制**（直接影响命中率）：

原问题 → 拆解逻辑 → 实际搜索词：

| 原始问题 | 拆解动作 | 最终搜索词 |
|---------|---------|----------|
| "how do I make my React app faster?" | 去疑问词，faster→performance | `react performance` |
| "怎么给 React 添加动画效果" | 提取核心名词，中英文同搜 | `react animation` |
| "帮我 check 一下 PR" | check→review | `pr review` |

---

### 📦 配置/工具详表

| 模块 | 关键命令/配置 | 预期效果 | 注意事项 |
|------|------------|---------|---------|
| 安装技能 | `npx skills add <owner/repo@skill> -g -y` | 全局静默安装 | `-g` 全局，`-y` 跳过确认 |
| 搜索结果展示格式 | `owner/repo@skill-name` + 安装命令 + 详情链接 | 直接可复制安装 | 详情链接格式：`https://skills.sh/<owner>/<repo>/<skill>` |
| 自建技能 | `npx skills init my-xyz-skill` | 生成 SKILL.md 模板 | 找不到匹配技能时的降级方案 |

---

### 💡 具体案例：复杂需求拆解 + 技能搜索

**场景**："自动从多个网站抓取内容，整理成表格，用 AI 分析趋势"

**第一步：给 Claude 的拆解提示词**

```
我有个需求：[描述你的需求]

请帮我拆解一下：
1. 这个需求包含哪几个子任务？
2. 每个子任务需要什么能力？
3. 哪些能力可能有现成的技能？
4. 我应该用什么关键词去搜索？
```

**Claude 返回的拆解结果**：

| 子任务 | 需要能力 | 可能的技能 | 搜索关键词 |
|-------|---------|----------|----------|
| 网页内容抓取 | HTTP请求、HTML解析、反爬虫 | web scraping、crawler、puppeteer | `"web scraping"` `"crawler"` |
| 内容整理成表格 | 数据结构化、表格生成 | data processing、excel generation | `"excel"` `"csv"` `"data processing"` |
| AI分析趋势 | 数据分析、可视化、AI推理 | data analysis、chart generation | `"data analysis"` `"visualization"` |

**第二步：给 Claude 的搜索提示词**

```
根据上面的拆解，请帮我找到以下技能：
1. 网页抓取相关的技能
2. Excel表格生成相关的技能
3. 数据分析相关的技能

如果找不到合适的，请告诉我是否需要创建自定义技能。
```

**找不到时 Claude 的降级回应示例**：
```
✓ 网页抓取：找到 playwright-scraper
✓ Excel生成：找到 excel-generator
✗ 数据分析：没有找到完全匹配的技能

建议方案：
1. 用 Claude 的通用数据分析能力（推荐，快速启动）
2. 创建自定义技能（如果需要重复使用）

需要我帮你创建 data-analyzer 技能吗？
我可以基于你的需求生成一个 SKILL.md 文件。
```

**万能技能搜索提示词模板**（直接复制使用）：

```
我有个需求：[详细描述你的需求.md]

请帮我：
1. 拆解这个需求包含哪些子任务
2. 每个子任务需要什么能力
3. 搜索相关的 Skills 技能
4. 如果找到了，推荐最合适的并说明理由
5. 如果没找到，告诉我是否需要创建自定义技能

最后给出完整的解决方案和安装建议。
```

> 💡 技巧：把需求写成 `.md` 文件，用 `[详细描述你的需求.md]` 引用，而不是直接在对话框里粘贴大段文字。AI 语义理解更准，你也不怕输入中途丢失。

---

### 📝 避坑指南

- ⚠️ `npx skills list` 只显示通过 `npx skills add` 安装的技能，其他方式安装的不会出现
- ⚠️ `npx skills update` 可能引入破坏性变更，正在依赖某技能特定行为时更新后可能出问题，务必先 `check` 再选择性更新
- ⚠️ `https://skillsmp.com/` 中文搜索只支持全字匹配，不适合中文用户直接使用，优先用自然语言让 Claude 调用 find-skills
- ⚠️ 找不到技能不代表技能不存在，先检查需求是否拆解清楚，关键词是否转换成了行业术语

---

### 🏷️ 行业标签

#ClaudeCode #Skills #AI工作流 #开发效率 #提示词工程 #工程化思维

---

---

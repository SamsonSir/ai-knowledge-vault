# Agent与技能系统

## 21. [2026-01-23]

## 📗 文章 2


> 文档 ID: `C1Tmw98BUi6pJJk0cTTcCMhpnPe`

**来源**: 我们花了两天时间，终于造出了能自我进化的Skills管理器 | **时间**: 2026-01-23 | **原文链接**: `https://mp.weixin.qq.com/s/hCN9UV_R...`

---

### 📋 核心分析

**战略价值**: 通过三件套 Skill 工具，实现 Claude Skills 库的全自动增删改查 + 版本追踪 + 经验沉淀，让 Skills 从静态文档变成自我进化的活体知识库。

**核心逻辑**:

- **痛点根源**：官方 skill-creator 生成的 SKILL.md 不含 `github_url` 和 `github_hash`，导致后续无法关联回 GitHub 仓库、无法对比版本，强行扫描匹配失败率极高。
- **身份系统是地基**：`github-to-skills` 在打包时强制注入两个元数据字段 `github_url`（来源仓库地址）和 `github_hash`（当前 commit hash），相当于给每个 Skill 颁发身份证，没有这个 ID，后续自动化管理全部无从谈起。
- **版本监控机制**：`skill-manager` 请求 GitHub API，用本地 SKILL.md 头部的 `github_hash` 与远程仓库最新 commit hash 对比，输出状态为「过期」或「最新」，一眼定位哪些 Skill 需要更新。
- **冲突问题的核心矛盾**：GitHub 更新拉取会覆盖 SKILL.md，而用户在使用过程中积累的 Bug 修复经验也写在 SKILL.md 里，两者同时操作同一文件必然冲突、互相覆盖。
- **解耦方案——evolution.json**：将用户经验与 GitHub 版本内容分离存储。GitHub 更新只动 SKILL.md 主文件；用户经验单独存入 `evolution.json`（类比游戏存档）。每次 SKILL.md 被新版本覆盖后，`evolution.json` 中的经验自动重新注入回 SKILL.md，两条线互不干扰。
- **经验沉淀机制**：`skill-evolution-manager` 在对话过程中默默记录 Skill 哪里出错、哪里需要改进，对话结束后将这些经验写入 `evolution.json`，再同步进 SKILL.md，下次运行同一 Skill 时自动绕过已知坑，实现「一坑不踩两次」。
- **两类 Skill 共存设计**：`github-to-skills` 与官方 `skill-creator` 并存，原因是并非所有 Skill 都来自 GitHub，自定义工作流和个人经验类 Skill 不需要注入 GitHub 元数据，两者各司其职。
- **飞轮效应**：四个 Skill 协同（`github-to-skills` + `skill-manager` + `skill-evolution-manager` + 官方 `skill-creator`），覆盖 Skills 的增（创建）、删（删除）、改（迭代）、查（列表/版本监控）全生命周期，形成自我强化的管理闭环。
- **实际使用节奏**：每次打开 OpenCode 先执行「检查所有 Skills 状态」，获得版本报告后按需执行「开始升级」，全程几十秒，无需手动介入任何文件操作。

---

### 🎯 关键洞察

**为什么 evolution.json 是关键设计决策**：

原因 → SKILL.md 同时承载「工具说明」和「使用经验」两种性质完全不同的内容，前者应随 GitHub 版本更新，后者属于用户私有资产不应被覆盖。

动作 → 将两类内容物理分离：SKILL.md 只存工具说明，evolution.json 专存进化经验，并在每次 SKILL.md 被覆盖后自动执行经验回注。

结果 → GitHub 版本升级和个人经验积累两条线并行不悖，Skills 既能跟上上游项目迭代，又能保留用户自己调教出来的「肌肉记忆」。

**为什么 github_hash 比版本号更可靠**：GitHub 很多项目不规范打 tag，但每次 commit 都有唯一 hash，用 hash 做版本指纹，覆盖率 100%，不依赖项目是否遵循语义化版本规范。

---

### 📦 配置/工具详表

| 工具名 | 核心功能 | 关键字段/文件 | 注意事项 |
|--------|---------|-------------|---------|
| `github-to-skills` | 将 GitHub 项目打包为带身份 ID 的 Skill | 注入 `github_url`、`github_hash` 到 SKILL.md 头部元数据 | 替代官方 skill-creator 用于 GitHub 类 Skill；自定义 Skill 仍用官方 skill-creator |
| `skill-manager` | 管理所有本地 Skills，版本监控 + 删除 | 读取 SKILL.md 头部 `github_hash`，调用 GitHub API 对比远程 hash | 依赖 `github-to-skills` 生成的身份 ID，无 ID 的 Skill 无法做版本对比 |
| `skill-evolution-manager` | 从对话中提取经验，写入 evolution.json，再注入 SKILL.md | `evolution.json`（经验存档文件） | SKILL.md 被新版本覆盖后需手动或自动触发经验回注；evolution.json 不随 GitHub 更新被覆盖 |
| 官方 `skill-creator` | 创建非 GitHub 来源的自定义 Skill | 标准 SKILL.md 格式 | 不含 github_url/github_hash，skill-manager 无法对其做版本监控 |

---

### 🛠️ 操作流程

1. **创建带身份 ID 的 Skill**
   - 对 GitHub 项目：使用 `github-to-skills` 打包，SKILL.md 头部自动注入 `github_url` 和 `github_hash`
   - 对自定义工作流：继续使用官方 `skill-creator`

2. **日常版本巡检**
   - 打开 OpenCode，执行：`帮我检查一下所有的Skills状态`
   - `skill-manager` 输出表格，列出每个 Skill 的类型、描述、版本状态（最新 / 过期）

3. **执行版本升级**
   - 对状态为「过期」的 Skill，执行：`开始升级`
   - `skill-manager` 自动拉取 GitHub 最新代码，重新构建 SKILL.md

4. **经验沉淀（使用后复盘）**
   - 跑完某个 Skill 任务后，触发 `skill-evolution-manager`
   - 它分析本次对话，提取 Bug 修复记录和改进点，写入该 Skill 目录下的 `evolution.json`
   - 同时将经验注入回 SKILL.md

5. **版本升级后经验回注**
   - SKILL.md 被新版本覆盖后，`evolution.json` 中存储的历史经验自动重新注入 SKILL.md
   - 确保升级后的新版 Skill 依然包含用户积累的所有避坑经验

---

### 💡 具体案例/数据

- **yt-dlp Skill**：第一次运行报错并解决后，通过对话记录让 skill-evolution-manager 自主迭代，将修复经验写入 evolution.json，后续运行自动规避同类错误。
- **company-claude-skills**：作者自建 GitHub 仓库用于演示，skill-manager 扫描后输出状态「过期」，执行升级后自动拉取最新代码重建 SKILL.md，全程几十秒。
- **X 平台阅读量**：上一篇 Skills 相关文章（将 GitHub 压缩成超级技能库）在 X 上接近百万阅读，公众号评论区大量用户提出 Skills 管理和迭代问题，直接催生本文三件套方案。
- **开源仓库**：`https://github.com/KKKKhazix/Khazix-Skills`

---

### 📝 避坑指南

- ⚠️ **不要用官方 skill-creator 打包 GitHub 项目**：生成的 SKILL.md 无 `github_url` 和 `github_hash`，skill-manager 无法识别对应仓库，版本监控功能完全失效。
- ⚠️ **evolution.json 必须与 SKILL.md 同目录存放**：这是经验回注机制的前提，路径错误会导致升级后经验丢失。
- ⚠️ **SKILL.md 被覆盖后需确认经验回注已执行**：升级流程结束后检查 SKILL.md 内容，确认 evolution.json 中的经验条目已成功写入，避免静默失败。
- ⚠️ **自定义 Skill 不要强行用 github-to-skills 打包**：注入无效的 github_url 会导致 skill-manager 版本检查时请求错误地址，产生误报。
- ⚠️ **GitHub API 有请求频率限制**：大量 Skill 同时做版本检查时，未认证请求每小时限 60 次，建议配置 GitHub Token 提升上限。

---

### 🏷️ 行业标签

#Claude-Skills #AI工具链 #自动化管理 #OpenCode #GitHub集成 #知识管理 #自我进化 #提示工程

---

---

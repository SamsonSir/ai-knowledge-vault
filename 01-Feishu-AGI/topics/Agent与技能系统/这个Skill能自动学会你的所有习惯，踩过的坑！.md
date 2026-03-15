# Agent与技能系统

## 77. [2026-02-23]

## 📚 文章 8


> 文档 ID: `VmkQwwvLriSxuek6qybcOgyZn7d`

**来源**: 这个Skill能自动学会你的所有习惯，踩过的坑！ | **时间**: 2026-02-23 | **原文链接**: https://mp.weixin.qq.com/s/2VkqDHQ-...

---

### 📋 核心分析

**战略价值**: Claudeception 是一个 Claude Code 插件，通过 Hook 机制在每次会话中自动提取有价值的工作知识，写入 Skill 文件，让 Claude Code 持续学习你的工作模式，越用越懂你。

**核心逻辑**:

- **原理**：Claude Code 启动时加载所有 Skill 的名称+描述（每个约 100 token），根据当前任务语义匹配并加载对应 Skill。Claudeception 利用这套系统的"可写"特性，把会话中产生的有价值知识自动写成新 Skill 文件。
- **触发条件（5种）**：① 完成调试发现不明显解法；② 通过反复试错找到 workaround；③ 解决根因不明的报错；④ 摸索出项目特有配置方式；⑤ 完成任何需要"真正发现"才能解决的任务。
- **质量门控（4条，必须同时满足）**：① 需要实际探索才能发现（查文档就能知道的不算）；② 对未来任务有帮助（一次性特殊情况不算）；③ 有明确触发条件（能精准匹配类似场景）；④ 已验证有效（猜测方案不算）。作者原话：如果这个知识对六个月后遇到同样问题的人没帮助，就不提取。
- **description 字段是匹配精度的核心**：写 `Helps with database problems` 什么都匹配不上；写 `Fix for PrismaClientKnownRequestError in serverless` 才能精准命中。Claudeception 自动生成的描述按此标准执行。
- **学习内容不只是偏好，而是完整工作模式**：包括写作流程（选题→大纲→正文）、文件命名规范（如 `2026-02-16_AI工具_常青_Claude_标题.md`）、问题排查顺序（搜索报错→检查配置→问AI）、文件目录结构（drafts/images/data）。
- **慢热机制**：前两周几乎无感知，因为它在积累有价值的知识而非记录所有操作。第三周起开始出现"它怎么知道我要什么"的体验。
- **学术支撑**：Voyager（2023，AI游戏中自动积累技能库）、CASCADE（2024，"元技能"概念）、SEAgent（2025，AI通过试错学习软件环境）、Reflexion（2023，自我反思提升AI表现）。
- **Claudeception 本质是"元技能"**：它不只是一个 Skill，而是一个能创造新 Skill 的 Skill，对应 CASCADE 论文中"学习如何学习"的概念。
- **适用人群**：Claude Code 每天使用超过 2 小时的重度用户、有固定工作流程的人、需要统一团队风格的负责人。偶尔使用者体感不明显。
- **GitHub 信息**：作者 blader（同时是 Humanizer 作者），两个项目合计 7800+ Star，Claudeception 本身 1660 Star。

---

### 📦 配置/工具详表

| 模块 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|------|-------------|---------|-----------|
| Skill 文件格式 | YAML 前置元数据 + Markdown 正文，含 name/description/author/version/date | 被 Claude Code 语义匹配加载 | description 必须写具体场景，模糊描述无效 |
| 用户级克隆 | `git clone https://github.com/blader/Claudeception.git ~/.claude/skills/claudeception` | 所有项目通用 | 推荐方式 |
| 项目级克隆 | `git clone https://github.com/blader/Claudeception.git .claude/skills/claudeception` | 仅当前项目生效，可提交 Git | 适合团队协作 |
| 用户级 Hook 脚本 | `mkdir -p ~/.claude/hooks && cp ~/.claude/skills/claudeception/scripts/claudeception-activator.sh ~/.claude/hooks/ && chmod +x ~/.claude/hooks/claudeception-activator.sh` | 每次发消息自动评估是否提取知识 | Windows 不兼容，需转 Node.js 版本 |
| 用户级 settings.json | 见下方代码块 | Hook 生效 | 已有 settings.json 只合并 hooks 字段，不要覆盖 |
| 项目级 Hook 脚本 | `mkdir -p .claude/hooks && cp .claude/skills/claudeception/scripts/claudeception-activator.sh .claude/hooks/ && chmod +x .claude/hooks/claudeception-activator.sh` | 项目级自动评估 | 同上 |
| 验证安装 | `cat ~/.claude/hooks/claudeception-activator.sh` | 能看到脚本内容即正常 | — |
| 查看已学 Skill（用户级） | `ls ~/.claude/skills/claudeception/` | 列出所有已生成 Skill 文件 | 每个文件是独立 .md，可直接删除或手动修改 |
| 查看已学 Skill（项目级） | `ls .claude/skills/claudeception/` | 同上 | — |

---

### 🛠️ 操作流程

**第一步：克隆仓库**

用户级（推荐，一次安装全项目通用）：
```bash
git clone https://github.com/blader/Claudeception.git ~/.claude/skills/claudeception
```

项目级（团队协作，可提交 Git）：
```bash
git clone https://github.com/blader/Claudeception.git .claude/skills/claudeception
```

**第二步：配置 Hook 脚本**

用户级：
```bash
mkdir -p ~/.claude/hooks
cp ~/.claude/skills/claudeception/scripts/claudeception-activator.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/claudeception-activator.sh
```

项目级：
```bash
mkdir -p .claude/hooks
cp .claude/skills/claudeception/scripts/claudeception-activator.sh .claude/hooks/
chmod +x .claude/hooks/claudeception-activator.sh
```

**第三步：写入 settings.json**

用户级 `~/.claude/settings.json`：
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/claudeception-activator.sh"
          }
        ]
      }
    ]
  }
}
```

项目级 `.claude/settings.json`：
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/claudeception-activator.sh"
          }
        ]
      }
    ]
  }
}
```

**第四步：验证安装**
```bash
cat ~/.claude/hooks/claudeception-activator.sh
```
能看到脚本内容即正常。

**第五步：手动触发（可选）**

觉得某次会话特别有价值，想确保被记录：
```
/claudeception
```
或直接说：
```
Save what we just learned as a skill
```

---

### 💡 具体案例/数据

**Skill 文件示例（标准格式）**：
```yaml
---
name: prisma-connection-pool-exhaustion
description: |
  Fix for PrismaClientKnownRequestError: Too many database connections
  in serverless environments (Vercel, AWS Lambda). Use when connection
  count errors appear after ~5 concurrent requests.
author: Claude Code
version: 1.0.0
date: 2024-01-15
---

# Prisma连接池溢出修复

## Problem
Serverless环境下数据库连接数爆了

## Context / Trigger Conditions
并发请求超过5个时出现PrismaClientKnownRequestError

## Solution
1、配置连接池上限
2、添加重试逻辑
3、使用连接代理（如PgBouncer）

## Verification
压测确认连接数稳定在配置上限内
```

**README 内置的 3 个示例 Skill**：

| Skill 名称 | 解决的问题 |
|-----------|----------|
| `nextjs-server-side-error-debugging` | 浏览器控制台看不到的服务端报错 |
| `prisma-connection-pool-exhaustion` | Serverless 环境"连接数太多"的问题 |
| `typescript-circular-dependency` | 检测和修复循环依赖 |

**真实学习效果（第三周）**：
- 说"帮我写篇AI工具测评"，Claude Code 直接输出：按习惯结构列大纲、口语风格正文、素材自动归入对应日期目录、三个数字型标题候选——无需任何额外说明。
- 说"帮我分析最近热点"，Claude Code 自动聚焦 AI 工具领域、从常关注信息源扫描、输出选题评分表格式——零追问。

---

### 📝 避坑指南

- ⚠️ **装上就想看效果**：前两周完全无感知是正常现象，它在积累知识而非立即响应。至少坚持 2-3 周。
- ⚠️ **低估学习深度**：它学的不是"文件放哪个目录"这种简单偏好，而是完整工作模式（流程、命名规范、排查顺序、目录结构）。
- ⚠️ **多项目混用**：同时做多个性质不同的项目会导致模式混乱，建议为每个项目创建独立工作区，使用项目级安装。
- ⚠️ **Windows 脚本不兼容**：自带 `.sh` 脚本仅支持 Mac/Linux，Windows 需将脚本逻辑转换为 Node.js 版本，并修改 settings.json 中的 command 字段。
- ⚠️ **description 写模糊**：`Helps with database problems` 这类描述无法被精准匹配，必须写具体的报错名称、环境、触发条件。
- ⚠️ **已有 settings.json 被覆盖**：只合并 `hooks` 字段，不要整个文件替换。
- ⚠️ **工作流程频繁变动**：Claudeception 需要稳定的模式才能有效学习，工作流程经常变化会降低学习质量。

---

### 🏷️ 行业标签

#ClaudeCode #Claudeception #AI工具 #技能自动化 #工作流优化 #元学习 #开发效率

---

---

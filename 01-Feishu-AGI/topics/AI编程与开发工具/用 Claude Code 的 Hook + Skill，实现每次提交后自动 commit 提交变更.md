# AI编程与开发工具

## 31. [2026-02-18]

## 📒 文章 7


> 文档 ID: `DGJvwkBEriC28ekBsfkc9lJ7nBd`

**来源**: 用 Claude Code 的 Hook + Skill，实现每次提交后自动 commit 提交变更 | **时间**: 2026-02-18 | **原文链接**: https://mp.weixin.qq.com/s/VqoZn7Pq...

---

### 📋 核心分析

**战略价值**: 用 Claude Code 的 Stop Hook 拦截任务结束事件 + Commit Skill 定义提交规范，实现"AI 改完文件就自动提交"，彻底消除手动 commit 遗漏问题。

**核心逻辑**:
- **痛点根源**：Git 追踪写作变更的价值在于细粒度历史，但人工提交频率低，导致多次修改堆成一个大杂烩 commit，失去追踪意义
- **Hook 机制原理**：Claude Code 在会话开始、工具调用前后、任务结束等生命周期节点可挂载脚本，Stop Hook 在任务准备结束时触发，返回 `{"decision": "block"}` 可阻止 Claude 停止并强制它继续执行
- **防无限循环设计**：提交动作本身也会触发 Stop Hook，必须用 `stop_hook_active` 标志位检测二次触发并直接 `exit 0` 放行，否则死循环
- **变更检测三合一**：`git diff --quiet`（已追踪文件修改）+ `git diff --cached --quiet`（已暂存修改）+ `git ls-files --others --exclude-standard`（未追踪新文件），三者都为空才算"干净"
- **Skill 是操作手册**：放在 `.claude/skills/<name>/SKILL.md`，`name` 字段自动注册为 `/slash-command`，可手动触发也可被 Hook 自动调用
- **按主题分组提交**：不用 `git add .`，而是分析文件路径归属（文章/技能/代码/配置），每个主题独立 commit，保证 `git log` 可读
- **中文 commit message 规范**：文章用"添加/润色/更新 + 主题"，代码用"优化/修复 + 功能"，不超过 50 字，杜绝"update files"类垃圾信息
- **明确排除临时文件**：`.bak-*`、`.html.bak-*`、`.DS_Store`、`node_modules/` 默认不提交，避免污染仓库
- **两者职责分离**：Hook 只负责"有没有漏提交"的守门判断，Skill 负责"怎么提交才有意义"的执行逻辑，解耦清晰
- **配置文件位置**：Hook 脚本在 `.claude/hooks/auto-commit.sh`，Skill 在 `.claude/skills/commit/SKILL.md`，Hook 配置在 `.claude/settings.local.json`

---

### 🛠️ 操作流程

**1. 准备阶段：创建目录结构**

```
.claude/
├── hooks/
│   └── auto-commit.sh
├── skills/
│   └── commit/
│       └── SKILL.md
└── settings.local.json
```

**2. 核心执行：写入三个文件**

文件一：`.claude/hooks/auto-commit.sh`

```bash
#!/bin/bash
# Stop hook: 任务完成后自动检测未提交变更并触发 commit skill

INPUT=$(cat)
STOP_HOOK_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false')

# 防止无限循环：commit 后再次触发时直接放行
if [ "$STOP_HOOK_ACTIVE" = "true" ]; then
  exit 0
fi

# 检查是否有未提交的变更
cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || exit 0

if git diff --quiet 2>/dev/null && \
   git diff --cached --quiet 2>/dev/null && \
   [ -z "$(git ls-files --others --exclude-standard 2>/dev/null)" ]; then
  exit 0
fi

# 有未提交变更，阻止 Claude 停止
cat <<'EOF'
{"decision": "block", "reason": "检测到未提交的变更，请调用 /commit 技能提交更新。"}
EOF
```

文件二：`.claude/skills/commit/SKILL.md`

```markdown
---
name: commit
description: 提交当前未 commit 的修改。自动分析变更内容，生成规范的 commit message，支持按目录分组提交或一次性提交所有修改。
---

# Git Commit 技能

## 工作流程

### 步骤一：查看未提交修改
git status --short

分析变更类型：
- M  - 已修改
- ?? - 新文件（未跟踪）
- D  - 已删除
- R  - 重命名

### 步骤二：分析变更内容

根据修改文件路径判断变更类型：

| 路径模式 | 变更类型 |
|----------|----------|
| posts/YYYY-MM-DD/[slug]/ | 文章相关 |
| .claude/skills/ | 技能配置 |
| src/ | 脚本代码 |
| .r2-upload-map/ | 资源映射（通常不单独提交） |
| 其他 | 项目配置 |

### 步骤三：决定提交策略

单一主题修改：一次性提交所有文件

多主题修改：按目录/主题分组提交

分组优先级：
1. 文章目录（每篇文章一个 commit）
2. 技能目录（每个技能一个 commit）
3. 代码变更（合并为一个 commit）
4. 配置文件（合并为一个 commit）

### 步骤四：生成 Commit Message

格式规范：
- 用中文
- 简洁描述变更内容
- 不超过 50 字

常用模板：
- 文章：添加 [文章主题简述]、润色 [文章标题]、更新 [文章标题]
- 技能：添加 [技能名] 技能、更新 [技能名] 技能
- 代码：优化 [功能描述]、修复 [问题描述]
- 配置：更新项目配置

### 步骤五：执行提交

git add <file1> <file2> ...
git commit -m "commit message"

注意：
- 避免使用 git add . 或 git add -A
- 明确指定要提交的文件
- 排除临时文件（.bak-*、.html.bak-*）

### 步骤六：确认结果

git log --oneline -3

## 排除规则

以下文件默认不提交：
- *.bak-* - 备份文件
- .DS_Store - macOS 系统文件
- node_modules/ - 依赖目录
- .r2-upload-map/*.json - 通常随文章一起提交，除非单独要求
```

文件三：`.claude/settings.local.json`（相关部分）

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/auto-commit.sh"
      }]
    }]
  }
}
```

**3. 验证阶段**

```bash
# 给脚本加执行权限
chmod +x .claude/hooks/auto-commit.sh

# 手动测试 hook（模拟无 stop_hook_active 的输入）
echo '{}' | .claude/hooks/auto-commit.sh

# 手动触发 skill
/commit
```

---

### 📦 配置/工具详表

| 模块 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|------|-------------|---------|-----------|
| Stop Hook 注册 | `settings.local.json` 的 `hooks.Stop` 数组 | 任务结束时自动触发脚本 | 用 `settings.local.json` 而非 `settings.json`，避免提交到公共仓库 |
| 无限循环防护 | `jq -r '.stop_hook_active // false'` 读取标志位 | commit 完成后第二次触发直接放行 | 依赖 `jq`，需确保环境已安装 |
| 变更检测 | `git diff` + `git diff --cached` + `git ls-files --others` | 覆盖已修改、已暂存、未追踪三种状态 | 三个命令缺一不可，只用 `git diff` 会漏掉新文件 |
| 阻断信号 | `{"decision": "block", "reason": "..."}` | 阻止 Claude 停止并传递原因 | reason 内容会被 Claude 读取，写清楚让它知道该调用哪个 skill |
| Skill 注册 | `SKILL.md` frontmatter 的 `name: commit` | 自动注册为 `/commit` 命令 | 文件必须放在 `.claude/skills/commit/SKILL.md`，目录名和 name 字段保持一致 |
| 提交文件指定 | `git add <file1> <file2>` 明确列举 | 避免提交临时文件 | 严禁 `git add .`，会把 `.bak-*` 等垃圾文件一起提交 |

---

### 💡 具体案例/数据

执行后 `git log --oneline` 效果对比：

| 之前（手动提交） | 之后（Hook + Skill） |
|----------------|-------------------|
| `a1b2c3d update files` | `42257b3 添加 Amodei NYT 访谈整理文章` |
| `e4f5g6h misc changes` | `c4eee96 添加 Peter Steinberger OpenClaw 访谈整理文章` |
| `h7i8j9k fix` | `e2a01da 润色 Suleyman FT 专访文章` |

---

### 📝 避坑指南

- ⚠️ **`stop_hook_active` 必须处理**：commit 动作结束后会再次触发 Stop Hook，不加标志位判断直接死循环
- ⚠️ **脚本需要执行权限**：`chmod +x .claude/hooks/auto-commit.sh`，否则 Hook 静默失败
- ⚠️ **`jq` 是隐性依赖**：脚本用 `jq` 解析 JSON 输入，CI 或新机器上需确认已安装
- ⚠️ **`$CLAUDE_PROJECT_DIR` 路径含空格时需加引号**：`command` 字段里已用 `\"$CLAUDE_PROJECT_DIR\"` 处理，不要改掉
- ⚠️ **`settings.local.json` vs `settings.json`**：Hook 配置写在 `local` 版本，不会被 git 追踪，避免把个人配置推到远程仓库

---

### 🏷️ 行业标签
#ClaudeCode #GitAutomation #Hook #Skill #写作工作流 #自动化提交

---

---

# Agent与技能系统

## 80. [2026-02-24]

## 📒 文章 7


> 文档 ID: `HYlUwiZdAiJdN4ktbApcL9WJnew`

**来源**: OpenClaw 1184个恶意插件，Claude找出500个零日漏洞，老金开源个安全Skill你直接拿去用 | **时间**: 2026-02-24 | **原文链接**: `https://mp.weixin.qq.com/s/vxQcj921...`

---

### 📋 核心分析

**战略价值**: AI Agent 既是最强安全工具也是最大攻击面——本文用三起真实安全事件佐证，并给出一个可直接部署的 Claude Code 安全扫描 Skill（基于 Semgrep 开源方案）。

**核心逻辑**:

- **Claude Code Security（2026-02-20 上线）**：不是规则匹配，而是像人类安全研究员一样读代码、理解上下文、追踪数据流。测试阶段在生产环境开源代码中找出 500+ 零日漏洞，部分漏洞存在了几十年。消息发布后 CrowdStrike 跌 8%、Okta 跌 9.2%、SailPoint 跌 9.4%。目前仅对 Enterprise 和 Team 客户开放。
- **ClawHavoc 事件**：ClawHub 平台上发现 1184 个恶意 Skill，伪装成正常工具，实际执行数据窃取和恶意指令注入。
- **Cisco 实测数据窃取**：一个精心构造的 WhatsApp 消息即可触发 OpenClaw 读取 `.env` 和 `creds.json` 文件（内含 API 密钥和登录凭证），全程用户无感知。
- **Moltbook 数据库泄露**：OpenClaw 生态内的 Agent 社交网络 Moltbook 直接泄露 35000 个邮箱 + 150 万个 API Token。
- **Claude Desktop 零点击漏洞（LayerX 发现）**：一个恶意 Google 日历事件即可触发远程代码执行，影响超过 10000 个活跃用户。根因是 MCP 架构中扩展直接拥有操作系统级权限，中间无安全边界。
- **Semgrep 作为平替方案**：开源、免费、规则匹配（非 AI 推理）、支持几十种编程语言、覆盖 OWASP Top 10，是 Claude Code Security 不可用时的可行替代。
- **社区响应**：SecureClaw 对 OpenClaw 做了 55 项安全审计，覆盖 OWASP ASI Top 10 全部 10 项；EvoMap 从底层协议重新设计，内置 5 层安全检查，默认 dry-run 模式。
- **核心矛盾**：AI Agent 权限越高、能力越强，攻击面越大。恶意插件、数据泄露、提示词注入、权限滥用是已发生的真实事件，不是理论风险。
- **Skill 触发机制**：Claude Code 用 `description` 字段做语义匹配，说"安全扫描"会遍历所有 Skill 的 description 找最相关的加载，因此 description 里需同时写中英文触发词。

---

### 🛠️ 操作流程

**1. 一键安装（三平台）**

```bash
git clone https://github.com/KimYx0207/SkillSemgrep.git
cd SkillSemgrep
```

Mac / Linux：
```bash
bash install.sh
```

Windows（PowerShell）：
```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

安装脚本自动执行：
1. 检测 Python（未安装会提示下载链接）
2. 检测并安装 Semgrep（未安装自动 `pip install semgrep`）
3. 复制 `SKILL.md` 到 `~/.claude/skills/code-security/`
4. 验证安装成功

装完无需重启 Claude Code，Hot Reloading 自动加载新 Skill。

**2. 手动创建（不跑脚本）**

在 `~/.claude/skills/code-security/` 目录下新建 `SKILL.md`，内容如下：

```markdown
---
name: code-security
description: "Runs Semgrep security scans on the current project to detect vulnerabilities, secrets leakage, and OWASP Top 10 issues. Use when the user asks for security scanning, vulnerability detection, or says 安全扫描, 扫漏洞, 安全检查, 漏洞检测."
version: "1.0"
context: fork
---

# AI代码安全扫描专家

你是代码安全扫描专家，使用Semgrep对当前项目进行安全漏洞检测。

## 前置检查

在执行任何扫描前，先确认Semgrep已安装：
semgrep --version
如果未安装，执行：pip install semgrep

## 扫描模式

1、全面扫描（默认）：semgrep scan --config auto
2、OWASP安全审计：semgrep scan --config "p/security-audit"
3、密钥泄露检测：semgrep scan --config "p/secrets"
4、Python专项：semgrep scan --config "p/python"
5、JS/TS专项：semgrep scan --config "p/javascript"

## 扫描流程

收到用户请求后：
1、确认Semgrep已安装
2、识别项目语言
3、选择合适的规则集
4、执行扫描
5、按严重程度分类（高危/中危/低危）
6、输出结构化报告并给出修复建议
```

**3. 使用方式**

在 Claude Code 中直接说：
- `安全扫描一下这个项目`
- `扫一下有没有漏洞`
- 斜杠命令：`/code-security`

输出：按高危 / 中危 / 低危分类的结构化报告，每个问题附带修复建议。

**4. Skill 部署范围选择**

| 部署位置 | 路径 | 作用范围 |
|---------|------|---------|
| 全局 Skill | `~/.claude/skills/code-security/SKILL.md` | 所有项目可用 |
| 项目级 Skill | `.claude/skills/code-security/SKILL.md` | 仅当前项目可用 |

---

### 📦 配置/工具详表

**SKILL.md YAML 元数据关键字段**

| 字段 | 说明 | 注意事项 |
|-----|------|---------|
| `name` | Skill 唯一标识符 | 用于 `/name` 斜杠命令触发 |
| `description` | 语义匹配核心字段 | 中英文触发词都要写进去，决定 Claude Code 能否正确匹配 |
| `version` | 版本号 | 字符串格式，如 `"1.0"` |
| `context` | 执行上下文 | `fork` 表示独立上下文运行 |

**Semgrep 扫描命令速查**

| 模式 | 命令 | 适用场景 |
|-----|------|---------|
| 全面扫描 | `semgrep scan --config auto` | 默认，自动识别语言 |
| OWASP 安全审计 | `semgrep scan --config "p/security-audit"` | 全面安全合规检查 |
| 密钥泄露检测 | `semgrep scan --config "p/secrets"` | 检查 API Key、Token 硬编码 |
| Python 专项 | `semgrep scan --config "p/python"` | Python 项目 |
| JS/TS 专项 | `semgrep scan --config "p/javascript"` | JavaScript/TypeScript 项目 |

**Semgrep vs Claude Code Security 对比**

| 维度 | Semgrep | Claude Code Security |
|-----|---------|---------------------|
| 检测方式 | 规则匹配 | AI 推理 + 上下文理解 |
| 数据流追踪 | 有限 | 完整 |
| 零日漏洞发现 | 弱 | 强（测试找出 500+ 个） |
| 可用性 | 免费开源，所有人可用 | 仅 Enterprise/Team 客户 |
| 速度 | 快 | 相对慢 |
| 适用阶段 | 日常开发基础扫描 | 深度安全审计 |

---

### 💡 具体案例/数据

- **ClawHavoc 事件**：ClawHub 上 1184 个恶意 Skill，伪装正常工具，实际偷数据 + 注入恶意指令
- **Cisco 实测**：WhatsApp 一条消息 → OpenClaw 自动读取 `.env` + `creds.json` → API 密钥和登录凭证泄露，全程用户无感知
- **Moltbook 泄露**：35000 个邮箱 + 150 万 API Token 直接从数据库泄露
- **Claude Desktop 零点击漏洞**：恶意 Google 日历事件 → 触发远程代码执行 → 影响 10000+ 活跃用户，根因是 MCP 扩展拥有 OS 级权限且无安全边界
- **Claude Code Security 战绩**：500+ 零日漏洞，全部来自生产环境开源代码，部分漏洞存在了几十年

---

### 📝 避坑指南

- ⚠️ 第三方 Skill/插件安装前务必审查来源，ClawHavoc 事件证明恶意 Skill 可完全伪装成正常工具
- ⚠️ `.env` 和 `creds.json` 不要放在 Agent 可访问的工作目录，提示词注入可直接读取这些文件
- ⚠️ MCP 架构扩展默认拥有 OS 级权限，安装任何 MCP 扩展前需评估其实际所需权限范围
- ⚠️ `description` 字段写不清楚会导致 Skill 无法被正确触发，中英文触发词都要覆盖
- ⚠️ Semgrep 是规则匹配，无法发现需要上下文推理才能识别的漏洞，不能替代人工审计或 Claude Code Security

---

### 🔗 相关资源

- 开源 Skill 仓库：`https://github.com/KimYx0207/SkillSemgrep.git`
- 开源知识库（实时更新）：`https://tffyvtlai4.feishu.cn/wiki/OhQ8wqntFihcI1kWVDlcNdpznFf`

---

### 🏷️ 行业标签

#Claude #AIAgent安全 #Semgrep #MCP漏洞 #提示词注入 #零日漏洞 #ClaudeCode #开源工具 #OWASP

---

---

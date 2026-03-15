# Agent与技能系统

## 108. [2026-03-07]

## 📒 文章 7


> 文档 ID: `YK6iwEXSPiDUFBkRl3ScbJ4ZnTg`

**来源**: Agent Skills实战指南：营销增长与SEO优化全攻略 | **时间**: 2026-03-14 | **原文链接**: 无

---

### 📋 核心分析

**战略价值**: Agent Skills 是 Anthropic 提出的开放标准，把「怎么做」的程序性知识打包成可被 AI 代理自动发现和加载的 Markdown 技能包，marketing-skills 库提供 144+ 个营销/SEO 技能，让 AI 代理在实际项目中输出符合专业规范的内容。

**核心逻辑**:

- **起源与标准化时间线**：2025-10-16 Anthropic 正式发布 Agent Skills；2025-12-18 作为开放标准发布，规范托管于 agentskills.io，比 MCP 捐赠给 Linux 基金会（2025-12-09）晚约 10 天，形成「MCP 负责外部连接，Skills 负责程序性知识」的互补架构
- **行业采用现状**：OpenAI（ChatGPT/Codex CLI）、微软（VS Code/GitHub Copilot）、Cursor、Claude Code、OpenCode、Gemini CLI 均已支持；Vercel Labs 开源了 skills CLI，提供 `npx skills add` 安装能力；skills.sh 成为技能发现与排行榜平台
- **Skills vs 其他组件的本质区别**：Prompt 是单次即时指令（会话结束即消失）；Skill 是可版本控制的程序性知识包（「怎么做」）；Tool 是单一可执行函数（产生实际副作用）；MCP 是协议层（工具发现/认证/通信）；RAG 是检索增强（注入上下文但不执行动作）
- **Skills 的渐进披露机制**：启动时只加载 SKILL.md 的 YAML frontmatter（name、description）元数据；激活时才加载正文；references/、scripts/ 目录按需加载——这是它比普通 Markdown 高效的核心原因
- **marketing-skills 库规模**：144+ 个技能，9 大类（SEO、Content、Paid Ads、Pages、Components、Channels、Platforms、Strategies、Analytics），覆盖 40+ 种页面类型，地址：`https://github.com/kostja94/marketing-skills`
- **安全风险不可忽视**：2026 年初安全研究显示，ClawHavoc 在 OpenClaw 生态发现 1,184+ 个恶意 Skill；Snyk ToxicSkills 研究对近 4,000 个 Skill 审计后，36.82% 存在安全缺陷，13.4% 存在严重问题（恶意软件、提示注入、凭证泄露）；攻击者常在 Setup 代码块中嵌入 base64 编码恶意脚本
- **触发机制**：代理启动时加载所有 skill 的 name + description，对话中根据自然语言意图做元数据匹配，无需手动指定技能名；description 中的关键词决定匹配精度
- **项目上下文是输出质量的关键变量**：在 `.cursor/`、`.claude/`、`.lovable/` 等目录放入 `product-marketing-context.md`（含产品定位、目标受众、品牌调性、关键词、竞品），可显著提升输出贴合度，避免泛化输出
- **推广机制**：`npx skills add owner/repo` 执行时 CLI 自动上报匿名安装数据，skills.sh 排行榜按安装量排序，无需单独提交，GitHub 公开仓库含 SKILL.md 即自动纳入生态
- **自建技能最低路径**：Fork `kostja94/marketing-skills` → 阅读 skills-guide → 复制修改相近技能 → 本地验证，无需从零开始

---

### 🎯 关键洞察

**为什么 Skills 比直接写 Prompt 更有价值**：
- Prompt 随会话消失，无法版本控制，团队无法共享；Skill 是文件，可 Git 管理、可 PR review、可 CI 验证
- 渐进披露机制降低 token 消耗：只有被激活的技能才加载全文，144 个技能同时存在但不会撑爆上下文窗口
- 「程序性知识」的本质是把隐性经验显性化：把 SEO 最佳实践、页面转化逻辑、品牌规范写成可复用指令，团队新人和 AI 代理都能执行一致的流程

**Skills 投毒的危害为何比 npm 包投毒更大**：
- Skills 继承代理的完整权限（Shell、文件系统、环境变量、API 密钥），而 npm 包通常在沙箱中运行
- 「Markdown 即安装」的低门槛：SKILL.md 中的 Setup 代码块会被用户或代理直接执行，攻击者无需绕过代码签名
- 发布门槛极低，通常无安全审核，skills.sh 只做常规审计，无法保证全部安全

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| CLI 安装全部技能 | `npx skills add kostja94/marketing-skills` | 安装到平台默认目录（如 `.cursor/skills/`），仓库层级结构扁平化为单层目录名 | 会覆盖已有同名技能 |
| CLI 安装指定技能 | `npx skills add kostja94/marketing-skills --skill robots-txt title-tag meta-description` | 只安装指定的 3 个技能 | 技能名需与目录名一致 |
| 列出可用技能（不安装） | `npx skills add owner/repo --list` | 查看仓库中所有可用技能名 | 不执行安装 |
| 搜索技能 | `npx skills find [关键词]` | 搜索并安装匹配技能 | 需先安装 find-skills 技能才能在对话中触发 |
| Git Submodule 同步 | 见下方操作流程方式一 | 纳入版本管理，可追踪更新历史 | 需手动 cp 到 `.cursor/skills/` |
| 直接 Clone 同步 | 见下方操作流程方式二 | 简单直接 | 需定期手动 pull |
| 一键更新脚本 | 见下方操作流程方式四 | 首次 clone，后续自动 pull + cp | 需提前创建 `.cursor/skills/` 目录 |
| OpenClaw 安装 | `npx skills add kostja94/marketing-skills -a openclaw` | 安装到 `./skills` 或 `~/.openclaw/skills/` | 与其他平台路径不同 |
| 无原生支持平台 | 将 SKILL.md 内容粘贴进对话 | 作为上下文使用 | ChatGPT/Gemini/Claude Web 均适用 |
| 跳过技能介绍 | 对话中说「skip intro」或「just do it」 | 代理直接输出主内容，不先讲背景 | 重复执行同一任务时尤其有用 |
| 手动指定技能（Cursor） | Agent 聊天中输入 `/` 搜索技能名 | 强制走指定流程 | 适合排查技能是否被正确触发 |

---

### 🛠️ 操作流程

**方式一：Git Submodule（适合纳入版本管理）**
```bash
# 首次添加
git submodule add https://github.com/kostja94/marketing-skills.git .cursor/marketing-skills
cp -r .cursor/marketing-skills/skills/* .cursor/skills/

# 更新
cd .cursor/marketing-skills && git pull origin main && cd -
cp -r .cursor/marketing-skills/skills/* .cursor/skills/
```

**方式二：直接 Clone 后定期 pull**
```bash
# 首次
git clone https://github.com/kostja94/marketing-skills.git .cursor/marketing-skills
cp -r .cursor/marketing-skills/skills/* .cursor/skills/

# 更新
cd .cursor/marketing-skills && git pull origin main && cd -
cp -r .cursor/marketing-skills/skills/* .cursor/skills/
```

**方式三：CLI 重新安装（覆盖更新）**
```bash
npx skills add kostja94/marketing-skills
```

**方式四：一键更新脚本（保存为 update-skills.sh）**
```bash
SKILLS_DIR=".cursor/marketing-skills"
TARGET_DIR=".cursor/skills"
if [ ! -d "$SKILLS_DIR" ]; then
  git clone https://github.com/kostja94/marketing-skills.git "$SKILLS_DIR"
fi
cd "$SKILLS_DIR" && git pull origin main && cd -
cp -r "$SKILLS_DIR/skills/"* "$TARGET_DIR/"
echo "Skills updated."
```

**Claude Code 路径差异**：
```bash
# Claude Code 使用 .claude/skills/ 而非 .cursor/skills/
cp -r repo/skills/* .claude/skills/
```

---

### 💡 具体案例/数据

**自然语言触发对照表**：

| 你说的话 | 代理调用的 Skill |
|---------|----------------|
| 帮我做一份 SEO 策略 | `seo-strategy` |
| 优化这个页面的 title 和 meta | `title-tag` + `meta-description` |
| 建一个落地页，要突出产品价值 | `landing-page-generator` |
| 创建落地页，skip intro | `landing-page-generator`（直接输出，不讲背景） |
| 配置 robots.txt | `robots-txt` |
| 做关键词研究 | `keyword-research` |
| 设计 pricing 页面 | `pricing` |

**marketing-skills 9 大类详细清单**：

| 类别 | 目录 | 代表技能 |
|-----|------|---------|
| SEO | `skills/seo/` | robots-txt, sitemap, canonical, title, description, schema, internal-links, keyword-research, parasite-seo, programmatic-seo |
| Content | `skills/content/` | copywriting, video, visual-content, translation |
| Paid Ads | `skills/paid-ads/` | google-ads, meta-ads, linkedin-ads, reddit-ads, tiktok-ads, youtube-ads, native-ads |
| Pages | `skills/pages/` | landing-page, pricing, home, about, faq, blog, changelog, 404, careers（共 40+ 种） |
| Components | `skills/components/` | cta, popup, testimonials, hero, breadcrumb, footer, newsletter-signup |
| Channels | `skills/channels/` | affiliate, email-marketing, influencer, referral, directories, pr |
| Platforms | `skills/platforms/` | x, reddit, linkedin, tiktok, youtube, pinterest, medium, github, grokipedia |
| Strategies | `skills/strategies/` | cold-start, pmf, gtm, product-launch, conversion, retention, pricing-strategy, domain-architecture |
| Analytics | `skills/analytics/` | traffic, tracking, seo-monitoring, ai-traffic, google-search-console |

**安全数据**（2026 年初）：
- ClawHavoc 研究：OpenClaw 生态中发现 **1,184+** 个恶意 Skill
- Snyk ToxicSkills 研究：近 **4,000** 个 Skill 审计结果——**36.82%** 存在安全缺陷，**13.4%** 存在严重问题

---

### 📝 避坑指南

- ⚠️ **安装前必须审查 SKILL.md**：重点看 Setup 代码块，对包含脚本的 Skill 要像对待可执行代码一样谨慎，base64 编码命令是常见恶意手法
- ⚠️ **CLI 安装会覆盖同名技能**：方式三（`npx skills add`）会直接覆盖已有同名技能，自定义修改过的技能会丢失，建议用方式一（Submodule）保留版本历史
- ⚠️ **Claude Code 路径与 Cursor 不同**：Cursor 用 `.cursor/skills/`，Claude Code 用 `.claude/skills/`，混用会导致技能无法被发现
- ⚠️ **没有项目上下文时输出偏通用**：必须在配置目录放入 `product-marketing-context.md`，至少包含产品概览、定位、目标受众、品牌调性，否则 AI 输出质量大打折扣
- ⚠️ **description 关键词决定触发精度**：自建技能时 description 写得模糊，代理匹配会失败或匹配到错误技能
- ⚠️ **SKILL.md 的 name 必须与目录名一致**：不一致会导致代理发现失败
- ⚠️ **skills.sh 安全审计不能完全信任**：平台只做常规审计，无法保证全部安全，优先选择安装量高、来源为官方或知名团队（vercel-labs、microsoft、anthropics）的技能

---

### 🔗 关键链接

- Skills 规范文档：`agentskills.io`
- 技能发现平台：`https://skills.sh`
- 查看自己的 Skills 是否被收录：`https://skills.sh/kostja94`
- marketing-skills 仓库：`https://github.com/kostja94/marketing-skills`
- 平台支持列表：`https://github.com/kostja94/marketing-skills/blob/main/docs/where-to-use-skills.md`
- Agent 生态思考：`https://web.okjike.com/u/C30D9805-A900-46DB-B4A6-655D22A1824D/repost/69a06c7325bae56612854010`

---

### 🏷️ 行业标签
#AgentSkills #营销自动化 #SEO #AIAgent #Claude #Cursor #LLM工具链 #供应链安全 #programmaticSEO #增长黑客

---

---

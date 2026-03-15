# Agent与技能系统

## 64. [2026-02-18]

## 📙 文章 4


> 文档 ID: `D0HzwFPWbiPfJYkel7QcB0MHnhg`

**来源**: Skills商店来了：5万人在用的Top 10热门Skills，我帮你试了一遍 | **时间**: 2026-01-24 | **原文链接**: `https://mp.weixin.qq.com/s/Cv2OtWDq...`

---

### 📋 核心分析

**战略价值**: skills.sh 是 Vercel 出品的 Claude Skills 应用商店，让非开发者也能一键安装社区验证过的 Skills，跳过"自己写 Skill"的门槛直接上手。

**核心逻辑**:

- skills.sh 由 Vercel 创建，是开放的 Skills 索引与分发平台，排行榜按安装量排序，最高单个 Skill 已达 37600+ 安装
- 安装方式统一为一行命令：`npx skills add <仓库名>/<skill名>`，复制粘贴到终端即可
- Top 10 中 7 个开发者专用、3 个全员可用（frontend-design、agent-browser、seo-audit）
- `frontend-design`（Anthropic 官方，7500+ 安装）核心价值是"反套路"：明确禁止 Claude 用 Inter/Roboto/Arial 字体、紫色渐变白底、对称布局，强制它输出有个性的设计
- `agent-browser`（2700+ 安装）是工具型 Skill，赋予 Claude 操控浏览器的能力：自动打开网页、点击、填表、批量截图、保存登录状态，运营/产品/测试均可用
- `seo-audit`（2300+ 安装）是完整 SEO 审计框架，覆盖爬虫可访问性、加载速度、内容优化、内容质量、外链权威性五个维度，输出格式为：问题 → 影响 → 修复方案 → 优先级
- `coreyhaines31/marketingskills` 仓库一次性提供 23 个营销 Skills，覆盖文案、定价、发布策略、A/B 测试、落地页 CRO、邮件序列、付费广告等，对产品/运营/市场比 Top 10 更实用
- `jimliu/baoyu-skills`（宝玉老师 @dotey 的仓库）包含 8 个中文场景 Skills：幻灯片生成、文章配图、封面图、小红书图片、漫画、发微信、发 X、信息图，对中文用户高度友好
- `anthropics/skills` 官方仓库含文档四件套：pdf / docx / pptx / xlsx，全员可用
- 学习 Skill 写法的最佳路径：装几个热门 Skill 后执行 `"帮我读取并解释 ~/.agents/skills/seo-audit/SKILL.md 的实现逻辑"`，Claude 会拆解触发条件、指令组织、分层逻辑，看 3-5 个即可掌握写法

---

### 🎯 关键洞察

**为什么 skills.sh 的排名可信**：37000+ 安装来自真实 vibe coder 群体，他们天天用 Claude Code 做产品，愿意装 = 真有用，社区已完成一轮筛选，无需自己判断。

**agent-browser 的实际场景逻辑**：
- 运营每天登录 5 个平台查数据 → Claude 自动完成登录+截图+整理，保存登录状态下次直接复用
- 产品经理做竞品分析 → Claude 自动打开多个竞品页面、截图、整理成文档

**frontend-design 的底层逻辑**：Claude 本身懂好设计，但默认会"偷懒"走最安全路径（Inter 字体 + 紫色渐变 = 典型 AI 味）。这个 Skill 的价值不是教 Claude 新知识，而是强制它不走捷径。

---

### 📦 配置/工具详表

| Skill / 仓库 | 安装命令 | 适合人群 | 核心功能 |
|---|---|---|---|
| vercel-react-best-practices | `npx skills add vercel-labs/agent-skills` | 前端开发 | React/Next.js 性能优化，57条规则，37600+安装 |
| web-design-guidelines | 同上仓库 | 前端开发 | 检查网页是否符合设计规范，28500+安装 |
| remotion-best-practices | 同上仓库 | 开发者 | 用代码做视频最佳实践，18800+安装 |
| skill-creator | 同上仓库 | 所有人 | Anthropic 官方出品，教你创建 Skill，3700+安装 |
| building-native-ui | 同上仓库 | 移动开发 | Expo 手机 App 开发指南，2700+安装 |
| better-auth-best-practices | 同上仓库 | 后端开发 | 登录认证系统最佳实践，2300+安装 |
| upgrading-expo | 同上仓库 | 移动开发 | Expo 框架升级指南，2200+安装 |
| frontend-design | `npx skills add anthropics/skills` | 所有人 | 反 AI 味设计规范，7500+安装 |
| agent-browser | `npx skills add vercel-labs/agent-skills` | 运营/产品/测试 | 浏览器自动化操作，2700+安装 |
| seo-audit | `npx skills add coreyhaines31/marketingskills --yes` | 运营/独立开发者 | 完整 SEO 审计框架，2300+安装 |
| marketingskills（23个） | `npx skills add coreyhaines31/marketingskills --yes` | 产品/运营/市场 | 文案/定价/发布/A/B测试/CRO/邮件/广告等 |
| baoyu-skills（8个） | `npx skills add jimliu/baoyu-skills --yes` | 中文用户 | 幻灯片/配图/小红书/发微信/发X等 |
| anthropics/skills（文档四件套） | `npx skills add anthropics/skills --yes` | 所有人 | pdf / docx / pptx / xlsx 处理 |

---

### 🛠️ 操作流程

1. **准备阶段**: 确保本地已安装 Node.js（npx 命令依赖），打开终端

2. **按岗位选择安装包**:
   - 开发者：`npx skills add vercel-labs/agent-skills` + `npx skills add anthropics/skills --yes`
   - 产品经理：`npx skills add coreyhaines31/marketingskills --yes` + agent-browser
   - 设计师：frontend-design + web-design-guidelines（均在 vercel-labs/agent-skills 仓库）
   - 运营/市场：`npx skills add coreyhaines31/marketingskills --yes`（23个全装）
   - 中文用户：`npx skills add jimliu/baoyu-skills --yes`

3. **验证安装**: Skills 默认安装到 `~/.agents/skills/` 目录，可用以下命令验证并学习写法：
   ```
   "帮我读取并解释 ~/.agents/skills/seo-audit/SKILL.md 的实现逻辑"
   ```

4. **实际使用示例**:
   - 运营：装 seo-audit → 问 Claude "帮我审计一下我们的官网SEO"
   - 产品：装 pricing-strategy → 问 Claude "帮我分析一下我们产品的定价策略"

5. **学习 Skill 写法**: 装 3-5 个热门 Skill → 让 Claude 逐一解读 SKILL.md → 理解触发条件写法、指令分层逻辑 → 模仿结构打包自己的工作流

---

### 📦 marketingskills 23个 Skills 明细

| Skill | 功能 | 适合谁 |
|---|---|---|
| copywriting | 营销文案写作 | 市场、运营 |
| copy-editing | 文案润色修改 | 市场、运营 |
| pricing-strategy | 定价策略设计 | 产品、创业者 |
| launch-strategy | 产品发布策略 | 产品、市场 |
| seo-audit | SEO诊断 | 运营、独立开发者 |
| ab-test-setup | A/B测试设计 | 产品、运营 |
| page-cro | 落地页转化优化 | 运营、增长 |
| signup-flow-cro | 注册流程优化 | 产品、增长 |
| email-sequence | 邮件营销序列 | 市场、运营 |
| social-content | 社交媒体内容 | 市场、运营 |
| paid-ads | 付费广告投放 | 市场 |
| referral-program | 推荐计划设计 | 增长、产品 |
| marketing-psychology | 营销心理学 | 市场、产品 |

（仓库共 23 个，上表为文章中列出的部分）

---

### 📝 避坑指南

- ⚠️ 别贪多：日常使用选 3-5 个高频 Skill 即可，装太多会增加 Claude 启动时的上下文加载量，影响性能
- ⚠️ 注意来源安全：Skills 可包含可执行脚本，`anthropics/skills`（Anthropic 官方）、`vercel-labs`（Vercel 官方）、`expo/skills` 等框架官方仓库可放心装；个人仓库需谨慎核查
- ⚠️ 最佳实践：与其手动复制安装命令，不如把本文和 skills.sh 网址直接丢给 Claude Code，用自然语言让它帮你选择并安装

---

### 🏷️ 行业标签
#ClaudeSkills #skills.sh #AI工作流 #Vercel #运营工具 #产品工具 #SEO #营销自动化 #浏览器自动化 #中文AI工具

---

---

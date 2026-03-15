# Agent与技能系统

## 24. [2026-01-23]

## 📓 文章 6


> 文档 ID: `LFoEwBlpviExvZkqvbSc8IqBn5g`

**来源**: 卡尔：我至今用到最好的Claude Code Skills第二篇，让Agent全学会你看过的工作流 | **时间**: 2026-03-13 | **原文链接**: `https://mp.weixin.qq.com/s/RpVU-mU8...`

---

### 📋 核心分析

**战略价值**: 9个经过实测的 Claude Code Skills，覆盖动画制作、无限画布、版本管理、动态PPT、Office全家桶、自动技能生成，直接 `npx skills add` 即可复用。

**核心逻辑**:

- **Skills 聚合发现入口**：Vercel 出的聚合站 skills.sh，按安装量排名，可看 24 小时内最火 Skills，安装方式统一为 `npx skills add <项目名>`
- **Remotion（JS/3D 动画）**：`npx skills add remotion-dev/skills`，免费做 JS 动画和 3D 动画，可用于制作文字讲解视频，嵌入 PPT 效果极强
- **Pencil（无限画布）**：无限画布版 CC，兼容 Figma，自带设计规范和示例风格，地址 `https://www.pencil.dev/`，定位为程序员/产品经理的设计工具
- **Skills 版本管理（两个工具组合使用）**：
  - `skills-updater`（@一支烟花）：检查本地 skill 是否有更新，有则自动安装；缺点是会覆盖本地修改版本
  - `Skill Vision Control`（@小耳）：下载新版本时保留旧版本，可对比后手动决定保留哪个，解决了 updater 的冲突问题
  - 安装命令：`npx skills add https://github.com/yizhiyanhua-ai/skills-updater --skill skills-updater`
- **动态PPT（NanaBanana-PPT）**：@歸藏佬出品，分析文档生成 PPT 大纲，用 Banana2 生图，用可灵做页面过渡动画，一键合成含所有转场的 PPT 视频；地址：`https://github.com/op7418/NanoBanana-PPT-Skills`
- **大批量风格化 PPT（notebooklm-skill + Theme Factory 组合）**：
  1. 网页端 notebooklm 生成 PPT 上限 20 页，改用 CC 可突破限制
  2. 先用 notebooklm-skill 生成结构化文档，明确每页讲什么
  3. 再用 Theme Factory 学习目标 PPT 风格（配色/字体对齐）
  4. 每次循环生成 15 张，风格保持一致，可做到 100 页
  5. 安装：`npx skills add https://github.com/pleaseprompto/notebooklm-skill --skill notebooklm`
- **Homunculus（全自动技能生成）**：监测用户行为模式，若连续 3-4 次请求前都做同一动作（如查 API 文档），自动打包成新 Skill；上一篇是手动 brainstorming 生成 Skills，这是升级版全自动方案
- **skill-from-masters（专家方法论转技能）**：新建技能时自动网络搜索领域专家方法论，或抓取高赞 GitHub 项目，转化为新技能；安装：`npx skills add https://github.com/gbsoss/skill-from-masters --skill skill-from-masters`
- **Document Suite（Office 全家桶）**：让 CC 带格式、带公式生成 Word / Excel / PPT / PDF，含金量高

---

### 📦 配置/工具详表

| 技能名 | 安装命令 | 核心功能 | 注意事项/坑 |
|---|---|---|---|
| Remotion | `npx skills add remotion-dev/skills` | JS/3D 动画，可生成讲解视频 | 免费使用 |
| Pencil | 访问 `https://www.pencil.dev/` | 无限画布，兼容 Figma，含设计规范 | 不算纯 Skills，独立产品 |
| skills-updater | `npx skills add https://github.com/yizhiyanhua-ai/skills-updater --skill skills-updater` | 自动检测并更新本地 Skills | 会覆盖本地修改，需配合 Skill Vision Control 使用 |
| Skill Vision Control | — | 更新时保留旧版本，可手动对比选择 | 解决 updater 覆盖冲突问题 |
| NanaBanana-PPT | `https://github.com/op7418/NanoBanana-PPT-Skills` | 文档→PPT大纲→生图→可灵转场→合成视频 | 依赖 Banana2 生图 + 可灵 |
| notebooklm-skill | `npx skills add https://github.com/pleaseprompto/notebooklm-skill --skill notebooklm` | 生成结构化文档，突破 20 页限制 | 需配合 Theme Factory 保持风格 |
| Theme Factory | — | 学习品牌风格（配色/字体），每次生成 15 张保持一致 | 循环使用可做 100 页 |
| Homunculus | — | 监测重复行为，全自动打包成新 Skill | 无需手动触发 |
| skill-from-masters | `npx skills add https://github.com/gbsoss/skill-from-masters --skill skill-from-masters` | 新建技能时自动搜索专家方法论/高赞 GitHub 项目 | — |
| Document Suite | — | 带格式带公式生成 Word/Excel/PPT/PDF | — |

---

### 🛠️ 操作流程

1. **发现 Skills**：访问 skills.sh（Vercel 聚合站），按 24 小时安装量排名筛选，找到目标 Skill 后用 `npx skills add <项目名>` 安装

2. **管理 Skills 版本**：先装 `skills-updater` 做自动更新检测，再装 `Skill Vision Control` 防止覆盖本地修改版本，两者配合使用

3. **批量风格化 PPT 工作流**：
   - Step 1：用 `notebooklm-skill` 生成结构化文档（每页内容明确）
   - Step 2：用 `Theme Factory` 学习目标 PPT 风格
   - Step 3：循环生成，每次 15 张，风格锁定，100 页可做

4. **自动沉淀个人工作流**：开启 `Homunculus`，连续重复 3-4 次的操作会被自动打包成 Skill；或用 `skill-from-masters` 在新建技能时自动引入专家方法论

---

### 📝 避坑指南

- ⚠️ `skills-updater` 自动更新会覆盖你本地修改过的 Skill，必须配合 `Skill Vision Control` 使用，否则本地定制版本会丢失
- ⚠️ 网页端 notebooklm 生成 PPT 上限 20 页，超量需求必须切换到 CC 端用 `notebooklm-skill` 才能突破
- ⚠️ NanaBanana-PPT 依赖外部服务（Banana2 生图 + 可灵动画），使用前确认两个服务账号已就绪

---

### 🏷️ 行业标签

#ClaudeCode #AISkills #自动化工作流 #PPT生成 #动画制作 #OfficeAI #技能管理

---

---

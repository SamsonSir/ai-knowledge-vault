# Agent与技能系统

## 106. [2026-03-07]

## 📘 文章 3


> 文档 ID: `ESFKwcchxi3ubPkNVeZcjuXEnfm`

**来源**: 劝一句：龙虾越火，越应该研究Skill，千万别跑偏！附送乔帮主精选Skills | **时间**: 2026-03-06 | **原文链接**: https://mp.weixin.qq.com/s/mpoOI3gA...

---

### 📋 核心分析

**战略价值**: 龙虾（OpenClaw）爆火背景下，真正的杠杆点不是「装没装龙虾」，而是「有没有打磨好 Skill」——Skill 是 AI Agent 的灵魂，决定 AI 能干什么、干得多好。

**核心逻辑**:
- 龙虾本身只是运行环境，没有 Skill 等于没装 App 的手机，装了也没用
- 当前市场热点：Mac mini 因龙虾卖爆、云主机厂商一键部署、各大模型厂商推出 Coding Plan、腾讯安排 20 名技术人员免费上门安装
- 多数人第一套 Skill 都是「信息抓取采集」——因为 AI 再聪明，得先喂得进东西才行
- Skill 分三条主线：抓取采集 / 内容创作 / 效率工具
- Agent Reach 实现零 API 成本覆盖全网信息源（含小红书、抖音、微信等中文平台）
- Defuddle 解决网页噪音问题，返回干净 Markdown 正文 + 元数据
- YouTube Skill 打通「搜索→下载→字幕提取→内容创作」完整链路
- Anything to NotebookLM 打通「内容获取→NotebookLM 输出」全链路，支持 15+ 格式输入、7 种输出形式
- 宝玉老师 Skill 合集覆盖「图文生成→社交媒体发布」完整自媒体工作流
- Skill 可用 Git 管理并发布到 GitHub，通过 `npx skills add` 一行安装；Skills.sh 已收录 86,000+ 个 Skill，SkillsMP 收录 38w+

---

### 🎯 关键洞察

**为什么 Skill 比装龙虾更重要？**

逻辑链：龙虾是执行引擎 → Skill 是任务定义 → 没有 Skill，引擎空转。
就像 iPhone 发布时 Jobs 说的：真正的革命是 App，不是硬件。

**为什么信息抓取是第一优先级 Skill？**
原因：AI 的输出质量上限 = 输入信息质量上限。抓取能力决定 AI 的「视野」，视野决定判断质量。

**Skill 发现的三层漏斗**：
- Skills.sh（官方目录，质量高，86,000+）→ SkillsMP（社区聚合，38w+，中文界面）→ Find Skills（元 Skill，终端内直接搜索安装）

---

### 📦 配置/工具详表

| Skill 名称 | 仓库/安装命令 | 核心功能 | 前置条件 / 注意事项 |
|-----------|-------------|---------|-----------------|
| Agent Reach | `https://github.com/Panniantong/Agent-Reach` / 让 AI 说「帮我安装 Agent Reach: `https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md`」 | 零 API 成本访问全网：网页、YouTube、Twitter/X、GitHub、Reddit、B站、小红书、抖音、微信公众号、RSS、语义搜索 | 需 Python、yt-dlp、gh CLI；中文平台需 Docker 运行 MCP 服务；内置诊断工具 `agent-reach doctor` |
| Defuddle | `npx skills add joeseesun/defuddle-skill` | 提取网页干净正文，去广告/侧边栏，返回 Markdown + 标题/作者/日期/字数元数据 | Obsidian CEO 原作，作者封装为 Skill |
| YouTube 搜索下载 | `npx skills add joeseesun/yt-search-download` | 全站搜索（按日期/播放量/相关性排序）、频道浏览、多画质下载（最高4K）、MP3提取、SRT+TXT字幕、英文标题自动翻译中文 | 需免费申请 YouTube API Key + `brew install yt-dlp`；需经常更新 yt-dlp；使用纯净度高的 IP |
| Anything to NotebookLM | `git clone https://github.com/joeseesun/anything-to-notebooklm.git && cd anything-to-notebooklm && ./install.sh` | 15+ 格式输入（微信/YouTube/PDF/EPUB/网页/Office/图片/音频）→ 自动生成播客/PPT/思维导图/测验/报告/视频/信息图 | 整合 tenglin 的 NotebookLM-py + 微软 Markitdown |
| 宝玉 Skills 合集 | `npx skills add jimliu/baoyu-skills` | 小红书信息图（多风格×多布局）、通用信息图（20种布局+17种视觉风格）、封面图（5维度设计系统）、幻灯片（14+风格）、漫画/插图、X发布、微信公众号发布、小红书发布、Markdown格式化、图片压缩(WebP/PNG)、DeepL翻译、URL转Markdown | 适合自媒体，覆盖生产到分发全流程 |
| X 长文发布 | `git clone https://github.com/joeseesun/qiaomu-x-article-publisher.git ~/.claude/skills/qiaomu-x-article-publisher && pip install Pillow pyobjc-framework-Cocoa patchright && python auth_manager.py setup` | Markdown 一键发布为 X Articles 草稿，支持完整格式（标题/加粗/斜体/列表/引用/代码块/链接/图片），自动处理图片上传 | 7天免重复认证 |
| Knowledge Site Creator | `npx skills add joeseesun/knowledge-site-creator` | 一句话生成完整学习网站并 Vercel 部署，支持闪卡/渐进学习/测验/索引/进度追踪，PWA+SEO+零前端依赖，原生 HTML/CSS/JS | 极简黄色主题；全程不需写一行代码 |
| Spotify 音乐播放器 | `npx skills add joeseesun/qiaomu-music-player-spotify` | 自然语言控制 Spotify，内置 5,947 种音乐风格数据库，30+ 风格快捷播放，支持搜索/播放/暂停/跳曲/音量/队列/情绪推荐，自动 OAuth token 刷新，零外部依赖（纯 Python 标准库） | 需 Spotify Premium 账号 |
| Design Advisor | `npx skills add joeseesun/qiaomu-design-advisor` | 乔布斯产品直觉 + Rams 功能纯粹主义 UI/UX 顾问，挖掘真实用户需求，审视间距/色温/动画时序，每问题提供三层方案（渐进改进/结构重设计/理想方案） | 触发词：「重新设计」「redesign」「review UI」「优化交互体验」 |
| Skill Publisher | `npx skills add joeseesun/skill-publisher` | 自动完成：验证 SKILL.md 元数据 → 创建 GitHub 仓库 → 推送代码 → 验证可通过 `npx skills add` 安装 | 需 GitHub CLI (`gh`) 已安装并认证 |

---

### 🛠️ 操作流程

**1. 准备阶段：确定你的 Skill 需求**
- 先回答：「你让 AI 帮你干什么？」
- 按三条线选择优先级：信息抓取（Agent Reach / Defuddle / YouTube）→ 内容创作（宝玉合集 / X发布）→ 效率工具（Spotify / Design Advisor）

**2. 核心执行：安装 Skill**
- 标准安装：`npx skills add {作者}/{skill名}`
- Git 安装（需配置）：`git clone {仓库} && cd {目录} && ./install.sh` 或 `pip install` 相关依赖
- 安装 Agent Reach：让 AI 直接读取安装文档 `https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md`

**3. 发现更多 Skill**
- 官方目录：`https://skills.sh/`（86,000+ Skills，支持 Claude Code / Copilot / Cursor / Cline / Gemini 等 20+ 平台）
- 元 Skill 搜索：`npx skills add vercel-labs/skills/find-skills` → 然后用 `npx skills find {关键词}` 搜索
- 中文社区：`https://skillsmp.com/zh`（38w+ Skills，最低 2 stars 质量门槛，从 GitHub 自动同步）

**4. 发布自己的 Skill**
- 用 Git 管理代码，推送到 GitHub（公开或私有库均可）
- 用 Skill Publisher 自动化发布流程：验证元数据 → 创建仓库 → 推送 → 验证安装

---

### 💡 具体案例/数据

- Agent Reach 覆盖平台：网页抓取、YouTube 字幕、Twitter/X 搜索、GitHub、Reddit、B站、小红书、抖音、微信公众号、RSS、语义搜索
- Anything to NotebookLM 输入格式：微信公众号、YouTube、PDF、EPUB、网页、Office 文档、图片、音频（15+ 种）
- Anything to NotebookLM 输出格式：播客、PPT、思维导图、测验、报告、视频、信息图（7 种）
- 宝玉 Skill 合集视觉风格数：通用信息图 20 种布局 + 17 种视觉风格；封面图 5 维度设计系统；幻灯片 14+ 风格预设
- Spotify Skill 音乐风格数据库：5,947 种，分层组织，30+ 风格快捷播放
- Skills.sh 收录量：86,000+ Skills，支持 20+ 平台
- SkillsMP 收录量：38w+ Skills，质量门槛：最低 2 stars

---

### 📝 避坑指南

- ⚠️ YouTube Skill：yt-dlp 需经常更新（`brew upgrade yt-dlp`），否则因 YouTube 反爬更新导致下载失败；同时使用纯净度高的 IP，避免被封
- ⚠️ Agent Reach 中文平台（小红书等）：必须用 Docker 运行 MCP 服务，不能直接裸跑；环境问题用内置 `agent-reach doctor` 诊断
- ⚠️ X 长文发布 Skill：依赖 `pyobjc-framework-Cocoa`，仅限 macOS；需先跑 `python auth_manager.py setup` 完成认证，7天内免重复认证
- ⚠️ Knowledge Site Creator：部署依赖 Vercel，需提前配置好 Vercel CLI 和账号
- ⚠️ Skill Publisher：发布前必须有合规的 SKILL.md 元数据文件，否则验证失败
- ⚠️ 核心认知坑：龙虾装了但没有 Skill，等于空转——先想清楚「让 AI 干什么」，再装对应 Skill，别本末倒置

---

### 🏷️ 行业标签
#ClaudeCode #龙虾OpenClaw #AIAgent #Skill #MCP #信息抓取 #内容创作 #自动化工作流 #NotebookLM #YouTube工具

---

---

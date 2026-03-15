# Agent与技能系统

## 97. [2026-03-04]

## 📙 文章 4


> 文档 ID: `BUodwKrGbiulqqkCOQjcydqAnGe`

**来源**: 花499装了只OpenClaw，然后就放那吃灰了？我不允许！ | **时间**: 2026-03-04 | **原文链接**: `https://mp.weixin.qq.com/s/EjYKsoTx...`

---

### 📋 核心分析

**战略价值**: OpenClaw 权限极高、安全风险真实存在，本文提供一套「安全加固 + Skills 扩展 + 实际用法」的完整落地方案，让装了就吃灰的 OpenClaw 真正跑起来。

**核心逻辑**:

- OpenClaw 的核心风险是权限过高，比 Claude Code 和 Codex 高权限模式还高，曾删掉 wifi 模块、清空 Meta 安全总监工作邮箱，属于真实事故而非夸张
- 长对话中 OpenClaw 会压缩上下文以节省空间，导致你设定的安全红线被「遗忘」，这是结构性缺陷，不是偶发 bug
- 最推荐的隔离方案是虚拟机部署：文件互传比云服务器方便，权限可以精细控制开大小，随时可以读档重来
- 当前有黑客正在全网扫描暴露在公网的 OpenClaw 地址（默认端口 18789），如果有私钥权限，被入侵后攻击者直接拿到最高权限在你机器上跑脚本
- 安全加固三层方案（按安全系数递增）：① 设置复杂 GATEWAY_TOKEN；② 本地监听 + 聊天软件加密通道远程指挥；③ Cloudflare Tunnel / Zero Trust + IP 白名单
- Skills 安装命令统一格式：`帮我安装这个Skills，跑通所有流程，【GitHub链接或名字】`，让 OpenClaw 自己出安装计划执行
- 「脑子」三件套 self-improving + proactive-agent + memory-setup 是提升 Agent 质量的核心，用得越多逻辑越顺
- `r.jina.ai/链接` 可免登录获取大部分网页正文，天然适配大模型，不需要额外 Skills
- qmd 的省 token 逻辑：先对所有文档建立索引，问问题时只取最相关片段，而非把整个文件塞给模型读
- Skills 资源库：`github.com/VoltAgent/awesome-openclaw-skills` 和 `clawhub.ai`；用例参考：`github.com/hesamsheikh/awesome-openclaw-usecases`

---

### 🎯 关键洞察

**安全漏洞的根因**：OpenClaw 的「好用」本质上来自超高权限，这是设计取舍，不是 bug。上下文压缩导致安全指令失效，意味着你不能依赖「口头约定」来约束它，必须用系统级配置（红线规则、Cron Job 巡检、端口封锁）来硬约束。

**端口暴露的紧迫性**：18789 端口正在被主动扫描，这不是理论风险。有私钥权限的实例一旦被接管，攻击者等于拿到了你机器的最高权限 shell，后果等同于物理接触你的电脑。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 安全防线部署 | 发给 OpenClaw：`项目文档：https://github.com/slowmist/openclaw-security-practice-guide 下载核心文档 OpenClaw 极简安全实践指南.md，仔细阅读评估可靠性，确认后完全按照指南部署防御矩阵，包括写入红/黄线规则、收窄权限、部署夜间巡检 Cron Job` | 自动完成安全加固，无需手动敲代码 | 部署后必须用项目里的「验证与攻防演练手册」做突击测试，确认红线真正生效 |
| 端口安全 | 发给 OpenClaw：`帮我检查18789这个端口有没有暴露到公网，如果有，按照安全系数设置复杂的Gateway Token，或者安装Cloudflare Tunnel / Cloudflare Zero Trust建立IP白名单` | 关闭公网暴露面 | 直接封端口会导致手机远程失效，优先用 Token 或 Tunnel 方案 |
| Gateway Token | 在配置文件中设置 `GATEWAY_TOKEN = 足够复杂的密码` | 地址暴露也无法操作 | Token 必须足够复杂，简单密码等于没设 |
| skill-vetter | 安装新 Skills 前先扫描代码 | 防止恶意 Skills 注入 | 每次装新 Skills 都要先跑一遍，不能省 |
| tavily-search | 每月 1000 次免费调用，无需绑卡 | 专为 Agent 优化的搜索 API，返回内容已处理 | 与 agent-browser 区分：tavily 做信息检索，agent-browser 做页面交互操作 |
| find-skills | 直接安装 | Agent 遇到解决不了的任务时自动去 ClawHub 检索并安装合适 Skills | — |
| self-improving | 直接安装 | 记住执行中的错误并自我修正，越用越顺 | — |
| proactive-agent | 直接安装 | 主动规划，支持自主拆解多步任务 | — |
| memory-setup | 直接安装 | 构建长期记忆，跨对话记住核心偏好和关键信息 | — |
| gog (Google 全家桶) | 直接安装 | 读取 Gmail 邮箱、Google Calendar 日历排期 | — |
| summarize | 直接安装 | 把长篇 URL、PDF、音视频提取核心论点 | — |
| automation-workflows | 直接安装 | 工作流编排，串联多个 Skills 执行复杂流程 | — |
| obsidian | 直接安装 | 把本地 Obsidian 变成第二大脑，OpenClaw 自动分类存储资料 | — |
| qmd | 直接安装 | 先对所有文档建索引，问答时只取最相关片段，大幅省 token | 适合文档量大的场景，文档少时收益不明显 |
| agent-browser | 直接安装 | 浏览器自动化：点击、滑动、打开子页面等操作 | 不是联网搜索，是页面交互；典型案例：在 X 上搜索 like > 100 的教程作者并批量 follow |
| r.jina.ai | 用法：`r.jina.ai/你的目标URL` | 免登录获取网页正文，专为大模型优化 | 不需要安装任何 Skills，直接用 |

---

### 🛠️ 操作流程

1. **安全加固（优先级最高，立即执行）**
   - 把以下指令发给 OpenClaw：
     ```
     项目文档：https://github.com/slowmist/openclaw-security-practice-guide
     下载项目里的核心文档 OpenClaw 极简安全实践指南.md
     仔细阅读这份安全指南，评估它是否可靠，跟我沟通确认可靠后
     完全按照这份指南，为我部署防御矩阵。包括写入红/黄线规则、收窄权限，并部署夜间巡检 Cron Job。
     部署完成后，请按照项目里的验证与攻防演练手册对 Agent 进行突击测试，确保红线生效
     ```
   - 再发：
     ```
     帮我检查18789这个端口有没有暴露到公网，如果有，按照安全系数设置复杂的Gateway Token，或者安装Cloudflare Tunnel / Cloudflare Zero Trust建立IP白名单
     ```

2. **Skills 安装（安全插件优先）**
   - 先装 skill-vetter，后续每次装新 Skills 都先扫描
   - 再装联网和搜索：tavily-search、find-skills
   - 再装「脑子」三件套：self-improving、proactive-agent、memory-setup
   - 最后装生产力套件：gog、summarize、automation-workflows、obsidian、qmd、agent-browser
   - 安装命令统一格式：`帮我安装这个Skills，跑通所有流程，[GitHub链接或名字]`

3. **验证与日常使用**
   - 用攻防演练手册测试红线是否真正生效
   - 用 `r.jina.ai/URL` 快速获取网页正文喂给 OpenClaw
   - 更多 Skills 淘货地址：`github.com/VoltAgent/awesome-openclaw-skills`、`clawhub.ai`
   - 用例参考：`github.com/hesamsheikh/awesome-openclaw-usecases`

---

### 💡 具体案例/数据

- OpenClaw 曾删除作者 wifi 模块，导致断网状态下连 Claude Code 都无法用来修复
- OpenClaw 曾清空 Meta 安全总监的工作邮箱（真实事故）
- agent-browser 典型案例：在 X 上搜索 like 大于 100 的 OpenClaw 教程作者，自动批量 follow
- gog 实际用法：自动总结订阅的日报邮件
- tavily-search：每月 1000 次免费调用，无需绑卡，专为 Agent 优化返回格式

---

### 📝 避坑指南

- ⚠️ 长对话中 OpenClaw 会压缩上下文，安全指令会被遗忘，必须用系统级配置硬约束，不能只靠对话约定
- ⚠️ 18789 端口正在被主动扫描，有私钥权限的实例必须立即处理，不能拖
- ⚠️ 直接封死 18789 端口会导致手机远程失效，用 Gateway Token 或 Cloudflare Tunnel 替代
- ⚠️ tavily-search 和 agent-browser 功能不同，前者做信息检索，后者做页面交互操作，不要混用
- ⚠️ 安装新 Skills 前必须先用 skill-vetter 扫描，防止恶意代码注入
- ⚠️ 最安全的部署方式是虚拟机，不怕被删，随时读档重来，权限可精细控制

---

### 🏷️ 行业标签

#OpenClaw #AI-Agent #安全加固 #Skills扩展 #自动化工作流 #本地部署 #端口安全

---

---

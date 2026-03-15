# AI编程与开发工具

## 20. [2026-02-06]

## 📙 文章 4


> 文档 ID: `AWT1wchuliEfeqk451icRIkYnMf`

**来源**: OpenAI 发布 GPT-5.3-Codex，一文详解 | **时间**: 2026-02-06 | **原文链接**: `https://mp.weixin.qq.com/s/39AKSqgZ...`

---

### 📋 核心分析

**战略价值**: GPT-5.3-Codex 是首个参与自身训练的模型，将编码能力与推理能力合并为单一模型，在终端操作、视觉桌面、网络安全等多项 benchmark 上刷新 SOTA，同时速度比前代快 25%、token 消耗更少。

**核心逻辑**:

- **架构合并**：GPT-5.3-Codex = GPT-5.2-Codex 的编码能力 + GPT-5.2 的推理与专业知识能力，合二为一，不再需要在两个模型间切换
- **速度提升**：推理速度比 GPT-5.2-Codex 快 25%，且在多个 benchmark 上 token 消耗低于所有前代模型
- **Terminal-Bench 2.0**：77.3%（GPT-5.2-Codex 是 64.0%，Claude Opus 4.6 刚拿最高分随即被超越），测的是编码 Agent 在终端里的实际操作能力
- **SWE-Bench Pro**：56.8%，比 SWE-bench Verified 更难，跨四种语言，更抗数据污染，准确率与 token 消耗双领先
- **OSWorld-Verified**：64.7%（GPT-5.2-Codex 是 38.2%，人类基准约 72%），视觉桌面操作，从不到人类一半直接跳到接近人类水平
- **GDPval**：70.9%，测 44 个职业的知识工作任务（PPT、表格、分析报告），与 GPT-5.2 持平
- **网络安全 CTF**：77.6%（GPT-5.2 是 67.7%），是 OpenAI Preparedness Framework 下首个被标为 High capability 的网络安全模型
- **自我参与训练**：早期版本的 GPT-5.3-Codex 被用于 debug 自身训练过程、管理自身部署、分析自身评测结果——OpenAI 称其为「第一个参与创造自己的模型」
- **实时交互模式**：不再是「下指令等结果」，模型在工作过程中主动汇报进展和关键决策，用户可中途提问、调整方向
- **网络安全定位升级**：首个被直接训练来识别软件漏洞的模型，部署了 OpenAI 迄今最全面的网络安全安全栈

---

### 🎯 关键洞察

**「用 Codex 训练 Codex」的具体落地方式**（这是本次发布最值得关注的部分）：

- 研究团队用 Codex 监控和 debug 训练过程，追踪训练中的行为模式，分析交互质量差异，并给人类研究员搭建可视化工具来精确理解模型行为变化
- 工程团队用 Codex 优化推理框架，定位上下文渲染 bug，排查缓存命中率低的根因；发布当天 GPT-5.3-Codex 仍在帮团队做 GPU 集群的动态扩缩容和延迟稳定
- Alpha 测试阶段，一个研究员想量化「每轮多做了多少工作」，GPT-5.3-Codex 自己写了几个正则分类器来估算澄清频率、正负反馈、任务进度，跑完所有 session log 后出了一份报告
- 数据科学家与 GPT-5.3-Codex 协作搭建新数据管道和可视化，三分钟内对上千个数据点完成摘要分析

逻辑链：模型能力足够强 → 可以参与自身开发流程 → 加速下一代模型的迭代速度 → 形成正向飞轮。OpenAI 原话：「团队被 Codex 加速自身开发的能力震住了」

**OSWorld 的跨越意义**：38.2% → 64.7% 是一次非线性跳跃，不是渐进改进。视觉桌面操作接近人类水平（72%），意味着「操作电脑」这个任务对模型来说已经不是瓶颈，而是可用能力。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|---|---|---|---|
| 实时交互模式 | Codex app → Settings > General > Follow-up behavior | 模型工作中途可交互，主动汇报进展 | 需在 Settings 手动开启，默认不一定启用 |
| 长上下文 Agent 游戏生成 | skill: `develop web game` + follow-up: `fix the bug` / `improve the game` | 在数百万 token 上下文内自主迭代 | 通用 prompt 即可，无需复杂指令 |
| 网络安全访问 | Trusted Access for Cyber 试点项目 | 加速网络防御研究，高级能力受限访问 | 需申请加入试点，非公开访问 |
| 代码安全扫描 | 与开源项目合作，免费代码扫描 | 已在 Next.js 中发现漏洞（Vercel 已披露） | 上周案例，能力已验证 |
| API 访问 | 准备中，OpenAI 说「soon」 | 程序化调用 GPT-5.3-Codex | 当前不可用，需等待 |

---

### 🛠️ 操作流程

1. **获取客户端**
   - 下载 Codex app（macOS）：`https://persistent.oaistatic.com/codex-app-prod/Codex.dmg`
   - 或使用 CLI、IDE 扩展、web 端，今日起全渠道可用

2. **开启实时交互模式**
   - 路径：Settings > General > Follow-up behavior
   - 开启后模型会在执行过程中主动汇报，可中途干预

3. **长时间 Agent 任务（以游戏生成为例）**
   - 初始 prompt：`develop web game`
   - 迭代 prompt：`fix the bug` / `improve the game`
   - 模型在数百万 token 上下文内自主迭代，无需人工逐步指导

4. **验证生成效果**
   - 赛车游戏 demo：`https://cdn.openai.com/gpt-examples/7fc9a6cb-887c-4db6-98ff-df3fd1612c78/racing_v2.html`
   - 潜水游戏 demo：`https://cdn.openai.com/gpt-examples/7fc9a6cb-887c-4db6-98ff-df3fd1612c78/diving_game.html`
   - Landing page demo（5.3-Codex 版）：`https://cdn.openai.com/gpt-examples/7fc9a6cb-887c-4db6-98ff-df3fd1612c78/gpt53-codex-landing-page.html`

---

### 💡 具体案例/数据

**Landing page 对比（同一 prompt）**：
- GPT-5.3-Codex：自动将年付方案显示为折后月价（折扣感更直观）+ 三条用户评价自动轮播
- GPT-5.2-Codex：常规实现，无上述细节优化
- 结论：相同 prompt 下，5.3-Codex 会主动做产品层面的决策，而不只是完成技术实现

**知识工作 demo（GDPval 对应场景）**：
- 金融顾问 PPT：比较 CD 和可变年金的风险收益
- 零售培训文档
- NPV 分析表格
- 时尚行业 PDF 演示
- 任务由 44 个职业的资深从业者设计，非合成数据

**网络安全实际案例**：
- 上周一名安全研究员用 Codex 在 Next.js 中发现漏洞，Vercel 已完成披露

**资金投入**：在 2023 年 $1M 网安资助计划基础上，追加 10M USD API credits，专门用于开源软件和关键基础设施的安全研究

---

### 📝 避坑指南

- ⚠️ API 访问当前不可用，OpenAI 只说「soon」，需要 API 集成的场景暂时无法使用
- ⚠️ 网络安全高级能力（High capability 标记）需通过 Trusted Access for Cyber 试点申请，不是默认开放
- ⚠️ 实时交互模式需手动在 Settings 开启，默认行为未必是交互模式
- ⚠️ OSWorld 64.7% 接近但未超越人类基准（72%），视觉桌面操作仍有约 7% 的差距，复杂任务不要完全依赖
- ⚠️ GDPval 与 GPT-5.2 持平（70.9%），知识工作类任务并非本次升级的重点，编码和终端操作才是核心提升方向

---

### 🏷️ 行业标签

#GPT-5.3-Codex #OpenAI #编码Agent #Terminal-Bench #SWE-Bench #OSWorld #自我迭代训练 #网络安全 #知识工作自动化 #AGI进展

---

---

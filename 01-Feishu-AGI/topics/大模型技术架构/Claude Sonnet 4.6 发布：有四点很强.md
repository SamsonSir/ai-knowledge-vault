# 大模型技术架构

## 21. [2026-02-18]

## 📗 文章 2


> 文档 ID: `QZCcwpf9Gijo6ak1TXrcpFPunRh`

**来源**: Claude Sonnet 4.6 发布：有四点很强 | **时间**: 2026-02-18 | **原文链接**: `https://mp.weixin.qq.com/s/03vQN6JM...`

---

### 📋 核心分析

**战略价值**: Anthropic 将 Opus 级能力下放至 Sonnet 4.6，价格不变，编程/长上下文/Computer Use/Agent 规划四项核心能力全面升级，是当前性价比最高的 Claude 模型。

**核心逻辑**:

- **跑分逼近 Opus**：SWE-bench Verified 达 80.2%（去年仅顶级模型能到），ARC-AGI-2 达 60.4%，需高强度推理才能完成
- **用户偏好反超上代 Opus**：在 Claude Code 中，70% 用户更偏好 Sonnet 4.6 vs Sonnet 4.5；59% 用户更偏好 Sonnet 4.6 vs 上代 Opus 4.5
- **编程质量提升的具体表现**：改代码前会先认真读上下文、主动合并重复逻辑、减少过度工程化、减少偷懒、减少幻觉、减少虚假"成功"声明
- **合作伙伴实测反馈**：GitHub（复杂代码修复解决率高）、Cursor（长远目标任务和困难问题显著改进）、Cognition（Bug 检测大幅缩小与 Opus 差距）、Replit（性价比惊人）
- **Computer Use 迭代 16 个月**：从 2024 年 10 月首推，OSWorld 基准测试（Chrome/LibreOffice/VS Code 等真实软件操作），复杂电子表格导航、多步骤网页表单填写已接近人类水平；提示注入防护提升至与 Opus 4.6 同等水平
- **百万 token 上下文（Beta）**：可一次性塞入整个代码库或数十篇研究论文，且能有效推理关联，不只是"看到"信息，对长时 Agent 任务尤为关键
- **Vending-Bench Arena 策略优势**：Sonnet 4.6 表现优于 4.5，核心策略是早期投资产能、最后阶段转向盈利
- **视觉/前端输出质量提升**：布局、动画、设计感明显更精致，Triple Whale 的 AJ Orbach 评价"构建前端页面时有完美的设计品味"，适合快速出原型
- **开发者平台同步更新**：自适应思考/扩展思考（根据问题复杂度自动调节思考深度）、上下文压缩（长对话不爆上下文）、网页搜索支持自动写代码过滤结果（更省 token）、代码执行/记忆/工具搜索正式 GA
- **免费用户权益扩大**：文件创建、连接器、技能、上下文压缩功能对免费用户开放

---

### 🎯 关键洞察

Anthropic 的核心策略是「能力下沉」：把 Opus 的能力持续下放到 Sonnet，让更多用户以更低成本享受顶级 AI。Sonnet 4.6 是这一策略的最新体现——Opus 依然是最强推理模型，适合深度代码重构等硬核任务，但 80%+ 的日常场景 Sonnet 4.6 已经够用，且更快。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|---|---|---|---|
| 百万 token 上下文 | TUI: `/model claude-sonnet-4-6[1m]` | 支持整个代码库或数十篇论文一次性输入 | 当前为 Beta 阶段 |
| settings.json 开启 1M | 见下方代码块 | 全局默认使用 1M 上下文版本 | 同时覆盖 Haiku 和 Sonnet 默认模型 |
| 模型 ID | `claude-sonnet-4-6` | 所有 Claude 套餐可用 | 免费/Pro 均可调用 |
| Claude in Excel | MCP 连接器 | 接入 S&P Global、LSEG、PitchBook、Moody's 金融数据 | 金融行业专项利好 |
| 网页搜索工具 | 自动编写并执行代码过滤搜索结果 | 更精准的搜索结果，更省 token | — |

**settings.json 配置代码**：

```json
{
  "env": {
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-sonnet-4-6[1m]",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-6[1m]"
  }
}
```

文件路径：`~/.claude/settings.json`

---

### 🛠️ 操作流程

1. **启用 1M 上下文（Beta）**
   - 方式一（临时）：在 Claude Code TUI 中执行 `/model claude-sonnet-4-6[1m]`
   - 方式二（全局）：编辑 `~/.claude/settings.json`，写入上方配置代码块

2. **切换默认模型**
   - API 调用时 model 参数填 `claude-sonnet-4-6`
   - claude.ai 免费/Pro 用户默认已切换，无需操作

3. **利用网页搜索省 token**
   - 开启网页搜索工具后，模型会自动写代码过滤搜索结果，减少无效内容占用上下文

4. **Computer Use 场景落地**
   - 适用于无 API 的企业软件自动化（填表单、操作 Excel、网页多步骤流程）
   - 当前在复杂电子表格导航、多步骤网页表单已接近人类水平

---

### 💡 具体案例/数据

| 基准测试 | Sonnet 4.6 成绩 | 参照意义 |
|---|---|---|
| SWE-bench Verified | 80.2% | 去年仅顶级模型可达 |
| ARC-AGI-2 | 60.4% | 需高强度推理 |
| Claude Code 用户偏好 vs Sonnet 4.5 | 70% 更偏好 4.6 | — |
| Claude Code 用户偏好 vs Opus 4.5 | 59% 更偏好 4.6 | Sonnet 反超上代 Opus |
| Computer Use 迭代时长 | 16 个月（2024.10 至今） | OSWorld 测试接近人类水平 |

---

### 📝 避坑指南

- ⚠️ 百万 token 上下文目前是 Beta，生产环境谨慎依赖
- ⚠️ Computer Use 在复杂操作上与最熟练人类操作者仍有差距，不适合零容错场景
- ⚠️ Opus 依然是最强推理模型，深度代码重构等硬核任务不要轻易降级到 Sonnet

---

### 🏷️ 行业标签

#Claude #Anthropic #LLM #AgentAI #ComputerUse #编程助手 #长上下文 #开发者工具

---

---

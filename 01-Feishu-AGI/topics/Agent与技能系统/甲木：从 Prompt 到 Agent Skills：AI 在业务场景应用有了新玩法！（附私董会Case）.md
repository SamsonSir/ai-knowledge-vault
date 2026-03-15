# Agent与技能系统

## 15. [2026-01-20]

## 📔 文章 5


> 文档 ID: `KMFHwlIpOicM7bkZm13co2iunsc`

**来源**: 甲木：从 Prompt 到 Agent Skills：AI 在业务场景应用有了新玩法！（附私董会Case） | **时间**: 2026-01-20 | **原文链接**: `https://mp.weixin.qq.com/s/OesAEy9f...`

---

### 📋 核心分析

**战略价值**: Agent Skills 是把"经验流程化、可复用化"的工程实践，解决通用 Agent 上下文膨胀与经验无法共享两大痛点，是 Prompt → Context → Skills 演进链条的最新落地形态。

**核心逻辑**:

- **三代范式演进**：Prompt 时代写"一次性指令"；Context 时代经营"信息场"；Skills 时代打包"能力包"，按需加载，让垂直 Agent 成本大幅降低。
- **Skills 本质定义**：把某个任务的 SOP、工具使用方式、模板材料、注意事项封装成一个能力包，需要时按需加载，让 Agent 稳定复用。Prompt/Context/Skills 对模型而言都是 Token，区别在于工程化管理方式。
- **爆火的两个根因**：① 超级提示词越堆越长，占 token、让模型变笨、难维护；② 经验无法跨同事/项目/对话窗口复用，团队各写各的"轮子"。
- **核心机制——渐进式披露**：Agent 按需分阶段加载信息，而非预先消耗上下文。平时只挂"目录"，需要时翻"正文"，更深资料临时去取。
- **三层信息分级**：Level 1 元数据（name + description，常驻，决定触发时机）→ Level 2 指令正文（SKILL.md 主体，决定触发后怎么做）→ Level 3 资源（scripts/references/assets，决定怎么把事做稳）。
- **SKILL.md 正文工程约束**：建议控制在 500 行以下（约 6000 tokens），复杂内容拆成子文档按需加载，防止模型"疲劳"。
- **Skills 运行环境**：在代码执行环境中运行，具备文件系统访问、bash 命令、代码执行能力，可把"容易出错的重复动作"固化成确定性动作。
- **Skills 的资产属性**：可版本化、可共享、可迭代，类比软件时代的插件/扩展包，通用 Agent 是内核，Skill 是能力扩展。
- **多 Skills 联动**：官方明确支持多 Skills 联用，如"私董会 Skill"+ "会议纪要 Skill"+"报告排版 Skill"+"PPTX Skill"，前者负责洞察决策，后者负责交付传播。
- **国内生态现状**：字节 Trae 率先接入"技能"模块；扣子（Coze）完成 2.0 迭代，支持技能模块，支持 AI 对话创建 skill 或直接上传 skill 文件，主打职场办公。

---

### 🎯 关键洞察

**为什么 description 是 Skill 的命门**：
description 决定触发时机。写成"万能助手"或"任何情况都可用"→ 冲突、误触发、漏触发。必须精确描述"在什么场景下触发"，例如：`在处理 PDF 文件或用户提及 PDF、表单或文档提取时使用`。

**Skills = 把经验产品化**：
过去 SOP 写在飞书/钉钉/企微文档里，靠人执行。现在 SOP 写进 Skill 里，由 Agent 执行。组织知识开始"可运行"。这是 Skills 最深层的价值——不是技巧，是资产。

**垂直 Agent 门槛下降的逻辑链**：
Coze/N8N 类 Workflow 平台对大多数人太难 → Skills 纯靠自然语言编写，更符合大众习惯 → 垂直 Agent 门槛下降 → 带来"领域专家做 Agent"浪潮 → Skill 市场/Agent 市场/企业内部 Skill 商店成为下一波入口。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|---|---|---|---|
| Level 1 元数据 | `name: pdf-processing` + `description: 从 PDF 文件中提取文本和表格...在处理 PDF 文件或用户提及 PDF、表单或文档提取时使用` | 精准触发 Skill | description 写虚 → 误触发/漏触发 |
| Level 2 指令正文 | SKILL.md 主体，含 Overview/Inputs/Workflow/Output Spec/Guardrails/Examples/Resources | 触发后稳定执行 SOP | 正文超 500 行/6000 tokens → 模型疲劳，需拆子文档 |
| Level 3 资源 | `scripts/fill_form.py`、`references/reference1.md`、`assets/`、`examples.md` | 提升确定性/一致性/事实性 | 脚本名必须与正文指令匹配，否则后续步骤无法稳定衔接 |
| 官方 skill-creator | 专门生成 skill 的 skill，从 0 到 1 直接生成 | 快速冷启动 | — |
| 官方最佳实践文档 | `https://platform.claude.com/docs/zh-CN/agents-and-tools/agent-skills/best-practices` | 工程规范参考 | — |
| 字节 Trae | 设置中直接使用"技能"模块 | 国内可用 | — |
| 扣子 Coze | 支持 AI 对话创建 skill / 直接上传 skill 文件 | 国内可用，主打职场办公 | — |
| 私董会 Skill（Coze 商店） | AI教育创业探讨：`https://www.coze.cn/s/uhoqMI7LtV0/` | 直接使用私董会流程 | 需审核通过后可用 |
| 私董会 Skill（Coze 商店） | 个人成长被"还不错"困住：`https://www.coze.cn/s/VOPGa_XQ37k/` | 直接使用私董会流程 | 需审核通过后可用 |

---

### 🛠️ 操作流程

#### 标准 Skill 目录结构

```
skill-name/
├── SKILL.md              # 主要说明（触发时加载）
├── FORMS.md              # 表单填充指南（按需加载）
├── references/           # API 参考（按需加载）
│   └── reference1.md
├── assets/               # 资产（按需加载）
├── examples.md           # 使用示例（按需加载）
└── scripts/
    ├── analyze_form.py   # 实用脚本（执行，不加载）
    ├── fill_form.py      # 表单填充脚本
    └── validate.py       # 验证脚本
```

#### SKILL.md Level 1 元数据模板

```yaml
---
name: pdf-processing          # 动名词形式，指示内容
description: 从 PDF 文件中提取文本和表格、填充表单、合并文档。在处理 PDF 文件或用户提及 PDF、表单或文档提取时使用。
---
```

#### SKILL.md Level 2 指令正文结构

```markdown
# [Skill 名称]

## Overview
本 Skill 解决什么问题，适用什么场景

## Inputs
用户需要提供什么信息，允许哪些格式

## Workflow
1. 步骤一
2. 步骤二
...

## Output Spec
输出结构、字段、格式、质量标准
（示例：输出必须包含 A/B/C 三部分，每部分不超过 X 字，并给出 3 条可执行行动）

## Guardrails
禁止事项、风险提示、合规边界

## Examples
触发示例与输出示例

## Resources
什么时候读参考资料，什么时候跑脚本
```

#### 私董会 Skill 完整执行流程（7步）

1. **Agent 匹配元数据**：看到"私董会""纠结""辞职""项目验证"等关键词，命中 description，触发 `peers-advisory-group` Skill。
2. **加载 SKILL.md 正文**：进入固定开场，确认问题边界，用户补充背景信息。
3. **第一轮提问**：每位幕僚提问 2 个犀利问题，问完必须等用户回答（保证案主参与感和信息完整度的核心机制）。
4. **第二轮提问（黑帽子）**：问"最坏情况""盲点""是不是自己的问题"，把案主从自我叙事里拽出来。
5. **案主反问环节**：定位是"补充信息"而非"求建议"。
6. **幕僚反馈建议**：按模板输出——名言金句、感受、问题定性、经历分享、具体建议。
7. **生成报告**：用户说出收获和总结，触发"杂志风格报告"输出模块，生成 HTML/PDF 完整报告。

---

### 💡 具体案例/数据

**私董会 Skill 三层结构拆解**：

- Level 1：name 用动名词形式（如 `peers-advisory-group`），description 精确描述触发场景
- Level 2：完整流程 SOP——"确认问题 → 三轮提问 → 反馈建议 → 总结"，含背景说明、流程化步骤
- Level 3：references/ 目录下外置——默认幕僚档案、反馈模板、反思模板、报告模板；可扩展 `quality-checklist.md`（输出自检清单）、`red-flags.md`（高风险场景提示，如涉及医疗/法律/投资建议时的边界提示）

**Anthropic 开放标准时间线**：Anthropic 在 2025 年底将 Agent Skills 发布为开放标准，Claude Code、Codex、OpenCode 等平台均已支持接入。

---

### 📝 避坑指南

- ⚠️ **触发描述写太虚**：description 写成"万能助手"或"任何情况都可用"，必然导致冲突、误触发、漏触发。必须精确描述具体触发场景。
- ⚠️ **指令正文过长**：SKILL.md 正文超过 500 行/6000 tokens，模型会"疲劳"，维护成本也急剧上升。复杂内容必须拆成子文档按需加载。
- ⚠️ **步骤缺乏可验收标准**：告诉模型"写得更好一点"无效。必须明确"输出必须包含 A/B/C 三部分，每部分不超过 X 字，并给出 3 条可执行行动"，才能让输出收敛。
- ⚠️ **缺少边界条件处理**：用户输入经常缺字段。必须在 Skill 里明确：缺信息时怎么追问、追问几个、追问顺序是什么。否则模型会直接输出一堆假设。
- ⚠️ **脚本与指令脱节**：scripts/ 里放了脚本，但正文没告诉 Agent 什么时候调用，或脚本名与正文指令名不匹配，导致后续步骤无法稳定衔接。
- ⚠️ **把 Skill 当"更长的 Prompt"**：Skill 应该像一个小产品——用户输入是多变的，边界情况是必然的，交付要可验收。写法应贴近场景 SOP，而非堆砌文字。

---

### 🏷️ 行业标签

#AgentSkills #ContextEngineering #PromptEngineering #AI落地 #SOP工程化 #垂直Agent #Coze扣子 #字节Trae #私董会 #渐进式披露

---

---

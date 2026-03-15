# Agent与技能系统

## 4. [2026-01-07]

## 📘 文章 3


> 文档 ID: `PUUDwvzRHiE9x2kTBkccHmf1nHe`

**来源**: Agent Skills 终极指南：入门、精通、预测 | **时间**: 2026-01-07 | **原文链接**: https://mp.weixin.qq.com/s/jUylk813...

---

### 📋 核心分析

**战略价值**: 用「文档即代码」的零门槛方式，借通用 Agent 内核（Claude Code）挂载垂直 Skill 包，低成本复制出智能上限等同完整 AI 产品的垂直 Agent。

**核心逻辑**:

- **Skill 本质是「工作交接大礼包」**：把任务 SOP、工具使用说明、模板素材、边缘问题处理方案，打包成 Agent 可读的文件夹结构，Agent 拿到后自主理解并执行，无需人工干预。
- **与 MCP 的根本区别**：MCP 是协议层，只管「如何连接外部工具」；Skill 是任务层，定义「如何完整处理一类工作」，包含执行方法 + 工具调用方式 + 知识材料。
- **渐进式披露机制是性能关键**：Level 1（元数据，~100 tokens，始终加载）→ Level 2（SKILL.md 正文，建议 <5000 tokens，触发时加载）→ Level 3（子技能/脚本/资源，按需动态加载，无大小限制）。这意味着一个 Agent 可以同时安装几十个 Skill 而不影响上下文性能。
- **脚本不进 Context Window**：Scripts/ 下的代码由 Agent 在虚拟机中直接调用，只有运行输出才进 Context，节省 tokens、避免出错、提升速度。
- **零代码创建**：最简 Skill 只需一个纯自然语言写成的 SKILL.md（如 brand-guidelines），就能让通用 Agent 变成符合品牌规范的垂直设计 Agent。
- **突破 Workflow 的预设限制**：Workflow 遇到边缘情况（格式不符、字段缺失）直接报错；Skill Agent 能自主调用其他 Skill 或即时编写转换脚本（如 doc2md），借 LLM 推理弥合边缘问题。
- **多 Skill 联用乘数效应**：brand-guidelines + pptx = 自动生成符合品牌规范的 PPT；AI-Partner-Chat + Article-Copilot = 符合个人思考与文风的内容生产；Web Scraping + PDF + Data Analysis + Brand + PPTX = 完整竞品分析报告，N 个 Skill 应对远超 N 的场景。
- **Skills 慢可以是 prompt，快可以是 workflow**：Skill 可设计为引导模型深度推理的长指令文档，也可以直接指向无需推理的可执行脚本，Agent 退化为 hook 角色，性能与传统程序无异。
- **AI Native 产品趋势**：未来笔记类 APP 会内置类 Skill 指引（笔记入库、智能纠错、冗余合并），用同一个多模态输入框，由 Agent 自动判断调用哪个 Skill 处理，实现绝对个性化响应。
- **Skill 生态时间窗口**：Agent Skills 开放标准发布不到 1 个月（截至文章发布 2026-01-07），OpenAI、GitHub、VS Code、Cursor 均已跟进，现在是生态早期红利期。

---

### 🎯 关键洞察

**为什么 Skill 的智能上限能等同完整 AI 产品？**

逻辑链：通用 Agent（Claude Code）本身已具备 LLM 全量推理能力 → Skill 只是给它挂载「垂直领域的知识 + 工具方法」→ Agent 用自己的智力「看着执行」，而非按预设路径走 → 结果：垂直能力 + 通用智能同时具备。

对比传统开发：
- 传统程序/Workflow：开发者智力 → 代码逻辑 → 固定输出（边缘情况报错）
- Skill Agent：领域专家知识 → Skill 文档 → LLM 智力自适应执行（边缘情况自愈）

**AI-Partner Skill 的自适应切片案例**（验证上述逻辑）：
- DailyNotes 按日期标题切分
- 项目笔记按标题级别与语义切分
- 非固定分隔符/字数切分，而是 Agent 动态判断，RAG 质量更高

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| SKILL.md 元数据（Level 1） | `---`<br>`name: pdf`<br>`description: 全面的 PDF 操作工具包，用于提取文本和表格、创建新 PDF、合并/拆分文档以及处理表单。当 Claude 需要填写 PDF 表单或大规模地程序化处理、生成或分析 PDF 文档时使用。`<br>`---` | Agent 启动时自动加载，约 100 tokens，用于隐式匹配触发 | description 写清楚「什么时候用」，影响隐式调用准确率 |
| SKILL.md 正文（Level 2） | Markdown 正文，包含工作流程、最佳实践、指导 | 触发 Skill 时加载，指导 Agent 执行 | 建议 <5000 tokens，超出拆为子技能文档 |
| 子技能文档（Level 3） | 如 `html2pptx.md`，独立放在 Skill 目录下 | 仅在特定子任务时加载，节省上下文 | 适合相对独立、复杂的子流程 |
| Scripts/（Level 3） | 预写好的可执行脚本，如 html 转 pptx 脚本 | Agent 直接调用，脚本本身不进 Context | 只有脚本输出进 Context，节省 tokens |
| 项目级 Skill 目录 | `<项目文件夹>/.claude/skills/<skill包>/` | 仅当前项目可用 | 路径必须正确，安装后需重启 CC |
| 全局 Skill 目录 | `~/.claude/skills/<skill包>/` | 所有项目共享 | 适合通用 Skill（如 brand-guidelines） |
| .skill 格式 | skill-creator 生成的压缩格式 | 直接告诉 CC 文件地址，让 CC 安装 | 与 zip/文件夹格式略有区别，不能直接解压放目录 |
| 官方 Skills 仓库 | https://github.com/anthropics/skills/tree/main | 包含 PDF、brand-guidelines、skill-creator 等官方 Skill | 质量参差，需筛选 |
| 第三方 Skills 市场 | https://skillsmp.com/zh | 聚合第三方 Skill | 缺乏评价和精选体系，难找优质 Skill |
| Skill 规格说明文档 | https://agentskills.io/specification#skill-md-format | 完整 SKILL.md 格式规范 | 精调或手写 Skill 时必读 |
| Agent Skills 开放标准 | https://agentskills.io/home | 跨平台 Skill 标准 | OpenAI/GitHub/VS Code/Cursor 均已跟进 |

---

### 🛠️ 操作流程

#### 使用已有 Skill（Claude Code 版）

1. **安装 Claude Code**
   - 打开终端，按官方指引安装：https://code.claude.com/docs/en/quickstart#native-install-recommended
   - 验证：终端输入 `claude --version`，看到版本号即成功
   - 小白方法：把官方指引文本发给任意 AI，用以下 Prompt 让它手把手教：
     ```
     我是电脑小白，参考以下信息，一步步指导我在【Mac/Windows/Linux】终端中安装该程序：【粘贴官方安装指引文本】
     当我

---

---

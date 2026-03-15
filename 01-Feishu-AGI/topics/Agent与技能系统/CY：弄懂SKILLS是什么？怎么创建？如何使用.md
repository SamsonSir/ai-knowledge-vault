# Agent与技能系统

## 1. [2026-01-02]

## 📗 文章 2


> 文档 ID: `D6mJwq1Pmiaa25kT0I8cJs4AnBc`

**来源**: CY：弄懂SKILLS是什么？怎么创建？如何使用 | **时间**: 2026-01-02 | **原文链接**: https://mp.weixin.qq.com/s/iFM9IyWb...

---

### 📋 核心分析

**战略价值**: Claude Skills 是将通用 LLM 转化为「领域专家数字员工」的 SOP 封装机制，通过渐进式上下文注入实现按需激活、Token 优化与行为确定性。

**核心逻辑**:

- **Skills 本质是 Agent 的「入职手册」**：以文件夹形式打包指令（SKILL.md）、脚本和资源，为 Claude 提供执行特定任务的标准化流程，等同于企业 SOP 减少人为误差的逻辑。
- **4 级激活架构，每级职责分离**：感知（加载 Metadata）→ 触发（语义路由）→ 激活（注入 SOP）→ 执行（程序化编排），每级独立运作，互不污染。
- **Metadata 极度轻量**：每项技能的 Frontmatter 仅占约 100 Tokens，系统启动时全量加载所有技能名称+描述，不浪费上下文。
- **纯语义路由，无硬编码**：Claude 接收用户指令后，依靠 LLM 推理能力自主匹配最相关技能，不依赖算法分发或关键词触发。
- **激活时秘密注入 SOP**：通过 Bash 读取 SKILL.md 正文，注入隐藏消息（`isMeta: true`），同时可动态修改 Allowed Tools 或切换更强模型（如 Claude Opus）。
- **程序化工具调用（PTC）减少幻觉**：复杂逻辑由 Python 脚本在沙盒 VM 中处理，MB 级中间数据不进入对话上下文，模型只接收精炼结果摘要，可减少约 37% Token 消耗并极大降低幻觉率。
- **MCP vs Skills 职责边界清晰**：MCP 负责「数据接入」（连接数据源），Skills 负责「逻辑控制」（教会 Claude 怎么用数据），两者互补而非替代。
- **description 字段是触发的核心**：Claude 完全依赖 description 的语义描述决定何时激活技能，写得越精准，触发越准确。
- **SKILL.md 建议控制在 500 行以内**：超出部分应拆分到独立参考文件，通过 `{baseDir}` 变量引用，保持上下文效率。
- **技能可打包分发**：`.skill` 文件本质是 `.zip` 压缩包，改后缀即可，便于团队共享和复用。

---

### 🎯 关键洞察

**渐进式披露机制**是 Skills 最核心的设计哲学：系统启动时只加载 ~100 Tokens 的 Metadata，任务触发后才将完整 SOP 注入上下文。这解决了「全量加载导致上下文污染」和「按需加载导致感知缺失」之间的矛盾——Claude 始终知道自己有哪些能力，但只在需要时才调用完整指令。

**PTC（程序化工具调用）** 是 Skills 相较于普通 Prompt 的质变点：传统 Prompt 让 LLM 直接处理复杂数据，Skills 让 LLM 编写 Python 脚本交给沙盒执行，LLM 只负责「编排逻辑」而非「处理数据」，这是行为确定性大幅提升的根本原因。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 开启 Skills | Settings > Capabilities > 开启 Skills | 解锁创建和使用入口 | 必须先开启才能看到创建选项 |
| `name` 字段 | 仅限小写字母、数字、连字符，最大 64 字符 | 技能唯一标识符 | 不能有空格或大写字母 |
| `description` 字段 | 详细描述功能及触发场景 | Claude 语义匹配的唯一依据 | 写得模糊 = 触发不准，这是最关键字段 |
| `allowed-tools` 字段 | 如 `Read, Write, Bash` | 激活时无需额外授权直接使用 | 可选，不填则使用默认权限 |
| `model` 字段 | 如 `claude-3-5-sonnet-latest` | 指定该技能运行时的模型 | 可选，可按任务复杂度切换更强模型 |
| SKILL.md 正文长度 | 建议 ≤ 500 行 | 保持上下文效率 | 超出部分拆到独立文件，用 `{baseDir}` 引用 |
| `.skill` 文件格式 | 本质是 `.zip`，改后缀即可 | 便于分发和导入 | 根目录必须包含 SKILL.md |

---

### 🛠️ 操作流程

**方式一：Create with Claude（推荐新手）**

1. 打开 Claude，进入 Skills 创建入口
2. 直接用自然语言描述你想要的技能（如「帮我创建一个公众号对比叙事写作技能」）
3. 与 Claude 对话完善细节，AI 自动生成技能文件
4. 点击「Copy to your skills」完成添加，或下载文件备用

**方式二：Write skill instructions（推荐已有想法者）**

1. 进入编辑界面，填写三个字段：
   - `Name`：如 `contrast-storytelling`
   - `Description`：如「对比叙事法写作技能，用于公众号/自媒体文章创作，当用户需要写对比类文章时触发」
   - `Instructions`：技能的核心理念、写作流程、模板、示例等（即 SKILL.md `---` 下方的正文内容）
2. 保存，系统自动生成 SKILL.md 文件和文件夹结构

**方式三：Upload a skill（适合导入现成技能）**

1. 准备符合以下结构的文件夹：
```
contrast-storytelling/
├── SKILL.md          ← 必须
├── reference.md      ← 可选
└── scripts/          ← 可选
    └── helper.py
```
2. 将文件夹压缩为 `.zip`，可选择改后缀为 `.skill`
3. 在 Skills 入口选择「Upload a skill」上传

**SKILL.md 标准结构模板**：
```yaml
---
name: your-skill-name
description: 详细描述技能功能及触发场景，Claude 依靠此字段决定何时激活
allowed-tools:
  - Read
  - Write
  - Bash
model: claude-3-5-sonnet-latest
---

## 项目概述
简述技能目的

## 具体步骤（SOP）
1. 分析...
2. 执行...
3. 输出...

## 参考资源
详见 {baseDir}/reference.md

## 输出示例
输入：...
输出：...
```

**使用已创建的技能**：

| 平台 | 调用方式 |
|------|---------|
| Claude.ai 网页版 | 自然语言触发（自动）或明确说「使用 contrast-storytelling 技能帮我写一篇文章」 |
| Claude Code | `/contrast-storytelling` 命令直接调用 |

---

### 📝 避坑指南

- ⚠️ `description` 写得太泛会导致技能从不触发或频繁误触发，必须明确描述「什么场景下激活」
- ⚠️ `name` 字段不能包含大写字母、空格或特殊字符，否则无法识别
- ⚠️ SKILL.md 超过 500 行会降低上下文效率，复杂内容必须拆分到 `reference.md` 等独立文件
- ⚠️ Upload 方式要求 SKILL.md 必须在压缩包根目录，不能嵌套在子文件夹内
- ⚠️ `.skill` 和 `.zip` 本质相同，分发时可直接改后缀，无需重新打包

---

### 🏷️ 行业标签
#ClaudeSkills #AIAgent #SOP #PromptEngineering #LLM工程化 #Claude #上下文优化

---

---
